from enum import Enum
from typing import Type
from itertools import chain

from .components import HasDependencies, RegisterFile

from .instruction import TwoOperandInstruction


class EntryState(Enum):
    ISSUED = "issued"
    EXECUTING = "executing"
    WRITING_BACK = "writing back"


class ReservationEntry:
    def __init__(self, tag: str):
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.time: int = -1
        self.state = EntryState.ISSUED
        self.output: float | None = None
        self.tag = tag
        self.register_file: RegisterFile = RegisterFile.get_instance()  # type: ignore
        self.instruction: TwoOperandInstruction | None = None
        self.locked: bool = False

    def set_instruction(self, instruction: TwoOperandInstruction) -> None:
        self.instruction = instruction
        self.op = instruction.operation
        if (
            type(self.register_file.get_register_value(instruction.first_operand))
            == float
        ):
            self.vj = float(
                self.register_file.get_register_value(instruction.first_operand)
            )
        else:
            self.qj = self.register_file.get_register_value(instruction.first_operand)
        if (
            type(self.register_file.get_register_value(instruction.second_operand))
            == float
        ):
            self.vk = float(
                self.register_file.get_register_value(instruction.second_operand)
            )
        else:
            self.qk = self.register_file.get_register_value(instruction.second_operand)

        self.time = instruction.latency

    def set_busy(self, busy: bool) -> None:
        self.busy = busy

    def __str__(self) -> str:
        return f"Busy: {self.busy}, Op: {self.op}, Vj: {self.vj}, Vk: {self.vk}, Qj: {self.qj}, Qk: {self.qk}, Time: {self.time}, State: {self.state}, Output: {self.output}, Tag: {self.tag}"

    __repr__ = __str__

    def decrease_time(self) -> None:
        self.time -= 1

    def set_state(self, state: EntryState) -> None:
        self.state = state

    def update(self, tag: str, output: float) -> None:
        if self.qj == tag:
            self.vj = output
            self.qj = None
        if self.qk == tag:
            self.vk = output
            self.qk = None

    def adjust_state(self) -> None:
        if self.time == 0:
            self.set_state(EntryState.WRITING_BACK)
            self.locked = True

    def execute(self) -> None:
        if self.output is None:
            if (
                self.vj is None
                or self.vk is None
                or self.op is None
                or self.instruction is None
            ):
                raise Exception("Invalid operation")

            self.output = self.instruction.calculate(self.vj, self.vk)
        match self.state:
            case EntryState.ISSUED:
                self.set_state(EntryState.EXECUTING)
                self.locked = True
                ExecutingInstructionQueue.get_instance().add_entry(self)  # type: ignore
                self.decrease_time()
                self.adjust_state()

            case EntryState.EXECUTING:
                self.decrease_time()
                self.adjust_state()

    def write_back(self) -> None:
        from .buffer import BufferAreas

        if self.output is None:
            raise Exception("Output not calculated")

        reservation_areas = (
            ReservationAreas.get_instance().get_reservation_areas()
        )  # type: ignore

        buffer_areas = BufferAreas.get_instance().get_buffer_areas()  # type: ignore

        entry_dependencies: list[object] = []

        for reservation_area in chain(
            reservation_areas.values(), buffer_areas.values()
        ):
            entry_dependencies.extend(reservation_area.get_dependencies(self.tag))

        for entry in entry_dependencies:
            entry.update(self.tag, self.output)

        register_dependencies = RegisterFile.get_instance().get_dependencies(
            self.tag
        )  # type: ignore

        for register in register_dependencies:
            RegisterFile.get_instance().register_map[
                register
            ] = self.output  # type: ignore

        self.set_busy(False)

    def to_json(self) -> dict[str, object]:
        return {
            "tag": self.tag,
            "busy": self.busy,
            "op": self.op,
            "vj": self.vj,
            "vk": self.vk,
            "qj": self.qj,
            "qk": self.qk,
            "time": self.time,
            "state": self.state.value,
        }


class ReservationArea(HasDependencies):
    def __init__(self, size: int, tag: str):
        self.size = size
        self.tag = tag
        self.reservation_area: dict[str, ReservationEntry] = {
            f"{tag}{i}": ReservationEntry(f"{tag}{i}") for i in range(1, size + 1)
        }

    def add_entry(self, entry: ReservationEntry) -> str:
        for key, value in self.reservation_area.items():
            if not value.busy:
                self.reservation_area[key] = entry
                return key
        raise Exception("Reservation area is full")

    def __str__(self) -> str:
        return f"{self.tag} {self.reservation_area}"

    __repr__ = __str__

    def get_entry(self, entry_tag: str) -> ReservationEntry:
        return self.reservation_area[entry_tag]

    def delete_entry(self, entry_tag: str) -> None:
        self.reservation_area[entry_tag].set_busy(False)

    def has_free_entry(self) -> bool:
        return any(not value.busy for _, value in self.reservation_area.items())

    def get_next_free_entry(self) -> ReservationEntry:
        for _, value in self.reservation_area.items():
            if not value.busy:
                return value
        raise Exception("Reservation area is full")

    def get_all_executable_entry_tags(self) -> list[str]:
        return [
            key
            for key, value in self.reservation_area.items()
            if value.busy
            and value.vj != None
            and value.vk != None
            and value.state != EntryState.WRITING_BACK
        ]

    def get_all_writing_back_entry_tags(self) -> list[str]:
        return [
            key
            for key, value in self.reservation_area.items()
            if value.busy and value.state == EntryState.WRITING_BACK
        ]

    def get_dependencies(self, entry_tag: str) -> list[ReservationEntry]:
        return [
            value
            for _, value in self.reservation_area.items()
            if value.qj == entry_tag or value.qk == entry_tag
        ]

    def is_empty(self) -> bool:
        return all(not value.busy for _, value in self.reservation_area.items())

    def to_json(self) -> dict[str, dict[str, str]]:
        return {key: value.to_json() for key, value in self.reservation_area.items()}


class ReservationAreas:
    __shared_instance = None

    @staticmethod
    def get_instance():
        if ReservationAreas.__shared_instance is None:
            ReservationAreas()
        return ReservationAreas.__shared_instance

    def __init__(self) -> None:
        if ReservationAreas.__shared_instance is not None:
            raise Exception("This class is a singleton class !")

        ReservationAreas.__shared_instance = self
        self.reservation_areas: dict[str, ReservationArea] = {
            "A": ReservationArea(3, "A"),
            "M": ReservationArea(2, "M"),
        }

    def get_reservation_areas(self) -> dict[str, ReservationArea]:
        return self.reservation_areas

    def to_json(self) -> dict[str, dict[str, dict[str, str]]]:
        return {key: value.to_json() for key, value in self.reservation_areas.items()}

    def reset(self) -> None:
        self.reservation_areas = {
            "A": ReservationArea(3, "A"),
            "M": ReservationArea(2, "M"),
        }


class ExecutingInstructionQueue:
    __shared_instance = None

    def __init__(self) -> None:
        if ExecutingInstructionQueue.__shared_instance is not None:
            raise Exception("This class is a singleton class !")

        ExecutingInstructionQueue.__shared_instance = self
        self.executing_instruction_queue: list[object] = []

    @staticmethod
    def get_instance():
        """Static Access Method"""
        if ExecutingInstructionQueue.__shared_instance is None:
            ExecutingInstructionQueue()
        return ExecutingInstructionQueue.__shared_instance

    def add_entry(self, entry: ReservationEntry) -> None:
        self.executing_instruction_queue.append(entry)

    def get_next_writing_back_entry(self) -> object | None:
        writing_back_entries = list(
            filter(
                lambda entry: entry.state == EntryState.WRITING_BACK
                and not entry.locked,
                self.executing_instruction_queue,
            )
        )
        if not writing_back_entries:
            return None
        # print(f"Writing back {writing_back_entries[-1]}")
        self.executing_instruction_queue.remove(writing_back_entries[-1])
        # print(f"Executing instruction queue {self.executing_instruction_queue}")
        return writing_back_entries.pop()

    def reset(self) -> None:
        self.executing_instruction_queue = []
