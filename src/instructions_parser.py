
from .reservation import RegisterFile, ReservationArea, ReservationAreas, ReservationEntry, ExecutingInstructionQueue


class InstructionParser():
    def __init__(self):
        self.instructions = []
        self.current_instruction = None
        self.min_instruction_size = 3

    def read_file(self, file_name: str) -> None:
        with open(file_name, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                self._parse_line(line.strip())

    def _get_instruction_size(self, operation: str) -> int | None:
        match operation:
            case 'L.D' | 'S.D':
                return 3
            case 'ADD.D' | 'SUB.D' | 'MUL.D' | 'DIV.D':
                return 4

    def _parse_line(self, line: str) -> None:
        if len(line.split(' ')) < self.min_instruction_size:
            raise Exception('Invalid instruction format')

        operation = line.split(' ')[0]
        instruction_size = self._get_instruction_size(operation)

        if not instruction_size or instruction_size != len(line.split(' ')):
            raise Exception('Invalid instruction format')

        self.instructions.append(line.split(' '))

    def get_instructions(self) -> list[list[str]]:
        return self.instructions


class InstructionsQueue():
    def __init__(self, instructions: list[list[str]]):
        self.instructions = instructions
        self.current_instruction_index = 0

    def get_next_instruction(self) -> list[str] | None:
        if self.current_instruction_index >= len(self.instructions):
            return None

        instruction = self.instructions[self.current_instruction_index]
        self.current_instruction_index += 1
        return instruction


class Tomasulo():
    def __init__(self, instructions: list[list[str]]):
        self.register_file = RegisterFile()
        self.instructions_queue = InstructionsQueue(instructions)
        self.reservation_areas = ReservationAreas().get_reservation_areas()
        self.executing_instructions_queue = ExecutingInstructionQueue()

    def _map_instruction_to_reservation_area(self, instruction: list[str]) -> ReservationArea | None:
        operation = instruction[0]

        match operation:
            case 'ADD.D' | 'SUB.D':
                return self.reservation_areas['A']
            case 'MUL.D' | 'DIV.D':
                return self.reservation_areas['M']
        return None

    def issue_instruction(self) -> None:
        next_instruction = self.instructions_queue.get_next_instruction()

        if not next_instruction:
            return

        reservation_area = self._map_instruction_to_reservation_area(
            next_instruction)

        if not reservation_area:
            raise Exception('Invalid instruction')

        if not reservation_area.has_free_entry():
            self.instructions_queue.current_instruction_index -= 1
            return

        entry = reservation_area.get_next_free_entry()

        entry.set_op(next_instruction[0])
        if type(self.register_file.get_register_value(next_instruction[2])) == float:
            entry.set_vj(float(self.register_file.get_register_value(
                next_instruction[2])))
        else:
            entry.set_qj(str(self.register_file.get_register_value(
                next_instruction[2])))

        if type(self.register_file.get_register_value(next_instruction[3])) == float:
            entry.set_vk(float(self.register_file.get_register_value(
                next_instruction[3])))
        else:
            entry.set_qk(str(self.register_file.get_register_value(
                next_instruction[3])))

        added_tag = reservation_area.add_entry(entry)
        entry.set_busy(True)

        self.register_file.set_register_value(
            next_instruction[1], added_tag)

    def execute(self) -> None:
        for reservation_area in self.reservation_areas.values():
            # print(reservation_area)
            execution_entries_tags = reservation_area.get_all_executable_entry_tags()
            print(execution_entries_tags)
            for tag in execution_entries_tags:
                print("Executing: ", tag)
                entry = reservation_area.get_entry(tag)
                entry.execute()

    def write_back(self) -> None:
        if entry := self.executing_instructions_queue.get_next_writing_back_entry():
            entry.write_back()
