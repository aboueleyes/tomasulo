from abc import ABC, abstractmethod
from typing import Union
from .instruction import Instruction


class HasDependencies(ABC):
    @abstractmethod
    def get_dependencies(self, tag: str) -> list[object]:
        raise NotImplementedError


class InstructionsQueue():
    def __init__(self, instructions: list[Instruction]):
        self.instructions = instructions
        self.current_instruction_index = 0

    def get_next_instruction(self) -> Instruction | None:
        if self.current_instruction_index >= len(self.instructions):
            return None

        instruction = self.instructions[self.current_instruction_index]
        self.current_instruction_index += 1
        return instruction

    def __str__(self) -> str:
        return '\n'.join([str(instruction) for instruction in self.instructions])

    __repr__ = __str__

    def is_empty(self) -> bool:
        return self.current_instruction_index >= len(self.instructions)


class RegisterFile(HasDependencies):
    __shared_instance = None

    @staticmethod
    def get_instance():
        if RegisterFile.__shared_instance is None:
            RegisterFile()
        return RegisterFile.__shared_instance

    def __init__(self):
        if RegisterFile.__shared_instance is not None:
            raise Exception('This class is a singleton!')

        RegisterFile.__shared_instance = self
        self.register_map: dict[str, Union[str, float]] = {
            f'F{i}': 0.0 for i in range(32)}

    def get_register_value(self, register: str) -> Union[str, float]:
        return self.register_map[register]

    def set_register_value(self, register: str, value: Union[str, float]) -> None:
        self.register_map[register] = value

    def get_dependencies(self, tag: str) -> list[str]:
        return [register for register, value in self.register_map.items() if value == tag]
