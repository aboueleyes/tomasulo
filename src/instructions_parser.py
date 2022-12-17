
from .instruction import Instruction, InstructionFactory


class InstructionParser():
    def __init__(self, latencies: dict[str, int]):
        self.instructions: list[Instruction] = []
        self.current_instruction: Instruction | None = None
        self.min_instruction_size = 3
        self.latencies = latencies

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

        self.instructions.append(InstructionFactory(
            line.split(' '), self.latencies).get_instruction())

    def get_instructions(self) -> list[Instruction]:
        return self.instructions

