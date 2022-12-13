from typing import Union

from enum import Enum
from abc import ABC, abstractmethod


class HasDependencies(ABC):
    @abstractmethod
    def get_dependencies(self, tag: str) -> list[object]:
        raise NotImplementedError


class RegisterFile(HasDependencies):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(RegisterFile, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.register_map: dict[str, Union[str, float]] = {
            f'F{i}': 0.0 for i in range(32)}

    def get_register_value(self, register: str) -> Union[str, float]:
        return self.register_map[register]

    def set_register_value(self, register: str, value: Union[str, float]) -> None:
        self.register_map[register] = value

    def get_dependencies(self, tag: str) -> list[str]:
        return [register for register, value in self.register_map.items() if value == tag]


class ReservationEntryState(Enum):
    ISSUED = 'issued'
    EXECUTING = 'executing'
    WRITING_BACK = 'writing back'


class ReservationEntry():
    def __init__(self, tag: str) -> None:
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.time: int = -1
        self.state = ReservationEntryState.ISSUED
        self.output: float | None = None
        self.tag = tag

    def set_busy(self, busy: bool) -> None:
        self.busy = busy

    def __str__(self) -> str:
        return f'Busy: {self.busy}, Op: {self.op}, Vj: {self.vj}, Vk: {self.vk}, Qj: {self.qj}, Qk: {self.qk}, Time: {self.time}, State: {self.state}, Output: {self.output}, Tag: {self.tag}'

    __repr__ = __str__

    def set_op(self, op: str) -> None:
        self.op = op

    def set_vj(self, vj: float | None) -> None:
        self.vj = vj

    def set_vk(self, vk: float | None) -> None:
        self.vk = vk

    def set_qj(self, qj: str | None) -> None:
        self.qj = qj

    def set_qk(self, qk: str | None) -> None:
        self.qk = qk

    def decrease_time(self) -> None:
        self.time -= 1

    def set_time(self, time: int) -> None:
        self.time = time

    def set_state(self, state: ReservationEntryState) -> None:
        self.state = state

    def adjust_state(self) -> None:
        if self.time == 0:
            self.set_state(ReservationEntryState.WRITING_BACK)

    def execute(self) -> None:
        if self.output is None:
            if self.vj is None or self.vk is None or self.op is None:
                raise Exception('Invalid operation')

            self.output = self._calculate(self.op, self.vj, self.vk)

        match self.state:
            case ReservationEntryState.ISSUED:
                self.set_state(ReservationEntryState.EXECUTING)
                self.set_time(2)  # FIXME: hardcoded
                ExecutingInstructionQueue().add_entry(self)
                print(self)
                self.decrease_time()

            case ReservationEntryState.EXECUTING:
                self.decrease_time()
                self.adjust_state()

    def write_back(self) -> None:
        if self.output is None:
            raise Exception('Output not calculated')

        reservation_areas = ReservationAreas().get_reservation_areas()
        entry_dependencies: list[ReservationEntry] = []
        for _, reservation_area in reservation_areas.items():
            entry_dependencies.extend(
                reservation_area.get_dependencies(self.tag))

        register_dependencies = RegisterFile().get_dependencies(self.tag)
        for entry in entry_dependencies:
            if entry.qj == self.tag:
                entry.set_vj(self.output)
                entry.set_qj(None)
            if entry.qk == self.tag:
                entry.set_vk(self.output)
                entry.set_qk(None)

        for register in register_dependencies:
            RegisterFile().register_map[register] = self.output

    @ staticmethod
    def _calculate(operation: str, *args: float) -> float:
        match operation:
            case 'ADD.D':
                return args[0] + args[1]
            case 'SUB.D':
                return args[0] - args[1]
            case 'MUL.D':
                return args[0] * args[1]
            case 'DIV.D':
                try:
                    return args[0] / args[1]
                except ZeroDivisionError:
                    return -1.0

        raise Exception('Invalid operation')


class ReservationArea(HasDependencies):
    def __init__(self, size: int, tag: str):
        self.size = size
        self.tag = tag
        self.reservation_area: dict[str, ReservationEntry] = {
            f'{tag}{i}': ReservationEntry(f'{tag}{i}') for i in range(1, size + 1)}

    def add_entry(self, entry: ReservationEntry) -> str:
        for key, value in self.reservation_area.items():
            if not value.busy:
                self.reservation_area[key] = entry
                return key
        raise Exception('Reservation area is full')

    def __str__(self) -> str:
        return f'{self.tag} {self.reservation_area}'

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
        raise Exception('Reservation area is full')

    def get_all_executable_entry_tags(self) -> list[str]:
        return [key for key, value in self.reservation_area.items(
        ) if value.busy and value.vj != None and value.vk != None and value.state != ReservationEntryState.WRITING_BACK]

    def get_all_writing_back_entry_tags(self) -> list[str]:
        return [key for key, value in self.reservation_area.items(
        ) if value.busy and value.state == ReservationEntryState.WRITING_BACK]

    def get_dependencies(self, entry_tag: str) -> list[ReservationEntry]:
        return [value for _, value in self.reservation_area.items() if value.qj == entry_tag or value.qk == entry_tag]


class ReservationAreas():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ReservationAreas, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.reservation_areas: dict[str, ReservationArea] = {
            'A': ReservationArea(3, 'A'),
            'M': ReservationArea(2, 'M'),
        }

    def get_reservation_areas(self) -> dict[str, ReservationArea]:
        return self.reservation_areas


class ExecutingInstructionQueue():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ExecutingInstructionQueue, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.executing_instruction_queue: list[ReservationEntry] = []

    def add_entry(self, entry: ReservationEntry) -> None:
        self.executing_instruction_queue.append(entry)

    def get_next_writing_back_entry(self) -> ReservationEntry | None:
        writing_back_entries = list(
            filter(lambda entry: entry.state == ReservationEntryState.WRITING_BACK, self.executing_instruction_queue))
        return writing_back_entries.pop() if writing_back_entries else None
