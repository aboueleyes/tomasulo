from itertools import chain
from .components import HasDependencies
from .instruction import OneOperandInstruction
from .reservation import EntryState, ExecutingInstructionQueue


class BufferEntry:
    def __init__(self, tag: str) -> None:
        from .components import RegisterFile

        self.busy = False
        self.address = None
        self.v = None
        self.q = None
        self.output = None
        self.state = EntryState.ISSUED
        self.instruction: OneOperandInstruction = None
        self.time: int = -1
        self.locked: bool = False
        self.tag: str = tag
        self.register_file = RegisterFile.get_instance()  # type: ignore

    def set_instruction(self, instruction: OneOperandInstruction) -> None:
        self.instruction = instruction
        self.address = instruction.address
        self.time = instruction.latency

        if instruction.operation == "S.D":
            if type(self.register_file.get_register_value(instruction.des)) == float:
                self.v = float(self.register_file.get_register_value(instruction.des))
            else:
                self.q = self.register_file.get_register_value(instruction.des)

    def set_busy(self, busy: bool) -> None:
        self.busy = busy

    def __str__(self) -> str:
        return f"Busy: {self.busy}, Address: {self.address}, V: {self.v}, Q: {self.q}, Time: {self.time}, State: {self.state}, Output: {self.output}, Tag: {self.tag} is locked: {self.locked}"

    __repr__ = __str__

    def decrease_time(self) -> None:
        self.time -= 1

    def set_state(self, state: EntryState) -> None:
        self.state = state

    def update(self, tag: str, output: float) -> None:
        if self.q == tag:
            self.v = output
            self.q = None

    def adjust_state(self) -> None:
        if self.time == 0:
            self.set_state(EntryState.WRITING_BACK)
            self.locked = True

    def execute(self) -> None:
        if self.output is None:
            self.output = self.instruction.calculate()

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
        from .reservation import ReservationAreas
        from .components import RegisterFile, Memory

        if self.output is None:
            raise Exception("Output is None")

        if self.instruction.operation == "S.D":
            Memory.get_instance().set_memory_value(self.address, self.v)
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
            "busy": self.busy,
            "address": self.address,
            "v": self.v,
            "q": self.q,
            "output": self.output,
            "state": self.state.value,
            "time": self.time,
            "locked": self.locked,
            "tag": self.tag,
            "op": self.instruction.operation if self.instruction else None,
        }


class BufferArea(HasDependencies):
    def __init__(self, size: int, tag: str) -> None:
        self.size = size
        self.buffer_entries: dict[str, BufferEntry] = {
            f"{tag}{i}": BufferEntry(f"{tag}{i}") for i in range(1, size + 1)
        }
        self.tag = tag

    def add_entry(self, entry: BufferEntry) -> str:
        for key, value in self.buffer_entries.items():
            if not value.busy:
                self.buffer_entries[key] = entry
                return key

        raise Exception("Buffer is full")

    def __str__(self) -> str:
        return f"{self.tag} Buffer: {self.buffer_entries}"

    __repr__ = __str__

    def get_entry(self, key: str) -> BufferEntry:
        return self.buffer_entries[key]

    def delete_entry(self, key: str) -> None:
        self.buffer_entries[key].set_busy(False)

    def has_free_entry(self) -> bool:
        return any(not value.busy for value in self.buffer_entries.values())

    def get_next_free_entry(self) -> BufferEntry:
        for value in self.buffer_entries.values():
            if not value.busy:
                return value

        raise Exception("Buffer is full")

    def get_all_executable_entry_tags(self) -> list[str]:
        return [
            key
            for key, value in self.buffer_entries.items()
            if value.busy
            and value.state != EntryState.WRITING_BACK
            and (
                value.instruction.operation == "S.D"
                and value.v is not None
                or value.instruction.operation != "S.D"
            )
        ]

    def get_all_writing_back_entry_tags(self) -> list[str]:
        return [
            key
            for key, value in self.buffer_entries.items()
            if value.busy and value.state == EntryState.WRITING_BACK
        ]

    def get_dependencies(self, tag: str) -> list[BufferEntry]:
        return [
            value
            for key, value in self.buffer_entries.items()
            if value.busy and value.q == tag
        ]

    def is_empty(self) -> bool:
        return not any(value.busy for value in self.buffer_entries.values())

    def to_json(self) -> dict[str, object]:
        return {
            "tag": self.tag,
            "buffer_entries": {
                key: value.to_json() for key, value in self.buffer_entries.items()
            },
        }


class BufferAreas:
    __shared_instance = None

    @staticmethod
    def get_instance() -> None:
        if BufferAreas.__shared_instance is None:
            BufferAreas()

        return BufferAreas.__shared_instance

    def __init__(self) -> None:
        if BufferAreas.__shared_instance is not None:
            raise Exception("This class is a singleton!")

        BufferAreas.__shared_instance = self
        self.buffer_areas: dict[str, BufferArea] = {
            "L": BufferArea(3, "L"),
            "S": BufferArea(3, "S"),
        }

    def __str__(self) -> str:
        return f"Buffer Areas: {self.buffer_areas}"

    __repr__ = __str__

    def get_buffer_areas(self) -> dict[str, BufferArea]:
        return self.buffer_areas

    def to_json(self) -> dict[str, object]:
        return ({key: value.to_json() for key, value in self.buffer_areas.items()},)
