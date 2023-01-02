import time
from .buffer import BufferArea, BufferAreas
from .reservation import (
    EntryState,
    ReservationArea,
    ReservationAreas,
    ExecutingInstructionQueue,
)
from .instruction import Instruction, OneOperandInstruction, TwoOperandInstruction
from .components import InstructionsQueue, Memory, RegisterFile

import logging
from rich.table import Table
from rich.console import Console

log = logging.getLogger("rich")


class Tomasulo:
    def __init__(self, instructions: list[Instruction], debug: bool = False):
        self.register_file: RegisterFile = RegisterFile.get_instance()  # type: ignore
        self.instructions_queue = InstructionsQueue(instructions)
        self.reservation_areas = (
            ReservationAreas.get_instance().get_reservation_areas()
        )  # type: ignore
        self.buffer_areas = BufferAreas.get_instance().get_buffer_areas()
        self.executing_instructions_queue: ExecutingInstructionQueue = ExecutingInstructionQueue.get_instance()  # type: ignore
        self.debug = debug
        self.current_cycle = 0

    def _map_instruction_to_reservation_area(
        self, instruction: Instruction
    ) -> ReservationArea:
        return self.reservation_areas[instruction.get_reservation_area()]

    def _map_instruction_to_buffer_area(self, instruction: Instruction) -> BufferArea:
        return self.buffer_areas[instruction.get_buffer()]  # type: ignore

    def issue_instruction(self) -> None:
        next_instruction = self.instructions_queue.get_next_instruction()

        if not next_instruction:
            return

        if issubclass(type(next_instruction), OneOperandInstruction):
            buffer_area = self._map_instruction_to_buffer_area(next_instruction)
            if not buffer_area:
                raise Exception("Invalid instruction")

            if not buffer_area.has_free_entry():
                self.instructions_queue.current_instruction_index -= 1
                return
            next_instruction.status = "ISSUED"

            entry = buffer_area.get_next_free_entry()
            entry.set_instruction(next_instruction)
            added_tag = buffer_area.add_entry(entry)
            if next_instruction.operation == "L.D":
                self.register_file.set_register_value(next_instruction.des, added_tag)
        else:
            reservation_area = self._map_instruction_to_reservation_area(
                next_instruction
            )

            if not reservation_area:
                raise Exception("Invalid instruction")

            if not reservation_area.has_free_entry():
                self.instructions_queue.current_instruction_index -= 1
                return

            next_instruction.status = "ISSUED"
            entry = reservation_area.get_next_free_entry()
            # type ignore is needed because mypy doesn't know that issubclass() is true
            entry.set_instruction(next_instruction)  # type: ignore
            added_tag = reservation_area.add_entry(entry)
            self.register_file.set_register_value(next_instruction.des, added_tag)

        entry.set_busy(True)
        entry.locked = True

    def execute(self) -> None:
        for reservation_area in self.reservation_areas.values():
            execution_entries_tags = reservation_area.get_all_executable_entry_tags()
            # log.info(f"Executing {execution_entries_tags}")
            for tag in execution_entries_tags:
                entry = reservation_area.get_entry(tag)
                # log.info(entry)
                if entry.locked:
                    continue
                entry.execute()
                # entry.instruction.status = "EXECUTING"
                # log.info(f"Executing {entry.instruction}")

        for buffer_area in self.buffer_areas.values():
            execution_entries_tags = buffer_area.get_all_executable_entry_tags()
            for tag in execution_entries_tags:
                entry = buffer_area.get_entry(tag)
                if entry.locked:
                    continue
                entry.execute()
                # entry.instruction.status = "EXECUTING"
                # log.info(f"Executing {entry.instruction}")

    def write_back(self) -> None:
        if entry := self.executing_instructions_queue.get_next_writing_back_entry():
            entry.write_back()
            # log.info(f"Writing back {entry.instruction}")

    def is_running(self) -> bool:
        # if self.debug:
        # # time.sleep(0.5)
        # self._print_instructions_queue()
        # # time.sleep(0.5)
        # self._print_reservation_areas()
        # # time.sleep(0.5)
        # self._print_buffer_tables()
        # # time.sleep(0.5)
        # self._print_memory()
        # # time.sleep(0.5)
        # self._print_register_file()

        return (
            not self.instructions_queue.is_empty()
            or any(
                not reservation_area.is_empty()
                for reservation_area in self.reservation_areas.values()
            )
            or any(
                not buffer_area.is_empty() for buffer_area in self.buffer_areas.values()
            )
        )

    def _print_instructions_queue(self):
        table = Table(title="Instructions Queue")
        console = Console()
        table.add_column("Index", style="cyan")
        table.add_column("Instruction", style="green")
        table.add_column("Status", style="green")

        for index, instruction in enumerate(self.instructions_queue.instructions):
            table.add_row(str(index), str(instruction), instruction.status)

        console.print(table)

    def _print_memory(self):
        table = Table(title="Memory")
        console = Console()
        table.add_column("Address", style="cyan")
        table.add_column("Value", style="green")
        for address, value in Memory.get_instance().memory_map.items():
            table.add_row(str(address), str(value)) if value != 0 else None
        console.print(table)

    def _print_register_file(self):
        table = Table(title="Register File")
        console = Console()
        table.add_column("Register", style="cyan")
        table.add_column("Value", style="green")
        for register, value in RegisterFile.get_instance().register_map.items():
            table.add_row(str(register), str(value)) if value != 0 else None
        console.print(table)

    def _print_reservation_areas(self):
        table = Table(title="Reservation Areas")
        console = Console()
        table.add_column("Reservation Area", style="cyan")
        table.add_column("Busy", style="green")
        table.add_column("Vj", style="magenta")
        table.add_column("Vk", style="magenta")
        table.add_column("Qj", style="yellow")
        table.add_column("Qk", style="yellow")
        for reservation_area in self.reservation_areas.values():
            for entry in reservation_area.reservation_area.values():
                table.add_row(
                    entry.tag,
                    str(entry.busy),
                    str(entry.vj),
                    str(entry.vk),
                    str(entry.qj),
                    str(entry.qk),
                )
        console.print(table)

    def _print_buffer_tables(self):
        table = Table(title="Buffer Areas")
        # console = Console()

        table.add_column("Buffer Area", style="yellow")
        table.add_column("Busy", style="green")
        table.add_column("Value", style="magenta")

        for buffer_area in self.buffer_areas.values():
            for entry in buffer_area.buffer_entries.values():
                table.add_row(str(entry.tag), str(entry.busy), str(entry.v))
        # console.print(table)

    def unlock_all_entries(self) -> None:
        for reservation_area in self.reservation_areas.values():
            for entry in reservation_area.reservation_area.values():
                self._update_status(entry)
        for buffer_area in self.buffer_areas.values():
            for entry in buffer_area.buffer_entries.values():
                self._update_status(entry)

    # TODO Rename this here and in `unlock_all_entries`
    def _update_status(self, entry):
        entry.locked = False
        if entry.time == 0 and entry.state == EntryState.EXECUTING:
            entry.set_state(EntryState.WRITING_BACK)
            entry.instruction.status = "WRITING_BACK"
        if entry.time == -5:
            entry.instruction.status = "FINISHED"

    def tick(self) -> None:
        self.unlock_all_entries()
        self.issue_instruction()
        self.execute()
        self.write_back()
        self.current_cycle += 1

    def reset(self) -> None:
        self.executing_instructions_queue.reset()
        ReservationAreas.get_instance().reset()
        BufferAreas.get_instance().reset()
        import os

        os.remove("instructions.txt")
