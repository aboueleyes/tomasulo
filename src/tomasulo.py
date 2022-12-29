from .buffer import BufferArea, BufferAreas
from .reservation import ReservationArea, ReservationAreas, ExecutingInstructionQueue
from .instruction import Instruction, OneOperandInstruction, TwoOperandInstruction
from .components import InstructionsQueue, RegisterFile


class Tomasulo:
    def __init__(self, instructions: list[Instruction]):
        self.register_file: RegisterFile = RegisterFile.get_instance()  # type: ignore
        self.instructions_queue = InstructionsQueue(instructions)
        self.reservation_areas = (
            ReservationAreas.get_instance().get_reservation_areas()
        )  # type: ignore
        self.buffer_areas = BufferAreas.get_instance().get_buffer_areas()
        self.executing_instructions_queue: ExecutingInstructionQueue = ExecutingInstructionQueue.get_instance()  # type: ignore

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
            for tag in execution_entries_tags:
                entry = reservation_area.get_entry(tag)
                if entry.locked:
                    continue
                entry.execute()

        for buffer_area in self.buffer_areas.values():
            execution_entries_tags = buffer_area.get_all_executable_entry_tags()
            for tag in execution_entries_tags:
                entry = buffer_area.get_entry(tag)
                if entry.locked:
                    continue
                entry.execute()

    def write_back(self) -> None:
        if entry := self.executing_instructions_queue.get_next_writing_back_entry():
            entry.write_back()

    def is_running(self) -> bool:
        print("=====================================")
        print("Reservation areas:")
        for reservation_area in self.reservation_areas.values():
            for k, entry in reservation_area.reservation_area.items():
                if entry.busy:
                    print(k, entry)
        print("=====================================")

        print("************************************")
        print("Buffer areas:")
        for buffer_area in self.buffer_areas.values():
            for k, entry in buffer_area.buffer_entries.items():
                if entry.busy:
                    print(k, entry)
        print("*****************************************")
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

    def unlock_all_entries(self) -> None:
        for reservation_area in self.reservation_areas.values():
            for entry in reservation_area.reservation_area.values():
                entry.locked = False

        for buffer_area in self.buffer_areas.values():
            for entry in buffer_area.buffer_entries.values():
                entry.locked = False
