from abc import ABC, abstractmethod
from typing import Union
import json


class HasDependencies(ABC):
    @abstractmethod
    def get_dependencies(self, tag: str) -> list[object]:
        raise NotImplementedError


class InstructionsQueue:
    from .instruction import Instruction

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
        return "\n".join([str(instruction) for instruction in self.instructions])

    __repr__ = __str__

    def is_empty(self) -> bool:
        return self.current_instruction_index >= len(self.instructions)

    def to_json(self) -> list[dict[str, object]]:
        return {
            index: {
                "instruction": instruction.string_representation,
                "status": instruction.status,
            }
            for index, instruction in enumerate(self.instructions)
        }


class RegisterFile(HasDependencies):
    __shared_instance = None

    @staticmethod
    def get_instance():
        if RegisterFile.__shared_instance is None:
            RegisterFile()
        return RegisterFile.__shared_instance

    def __init__(self):
        if RegisterFile.__shared_instance is not None:
            raise Exception("This class is a singleton!")

        RegisterFile.__shared_instance = self
        self.register_map: dict[str, Union[str, float]] = {
            f"F{i}": 0.0 for i in range(32)
        }

    def get_register_value(self, register: str) -> Union[str, float]:
        return self.register_map[register]

    def set_register_value(self, register: str, value: Union[str, float]) -> None:
        self.register_map[register] = value

    def get_dependencies(self, tag: str) -> list[str]:
        return [
            register for register, value in self.register_map.items() if value == tag
        ]

    def __str__(self) -> str:
        # print table
        return "\n".join(
            [f"{register} {value}" for register, value in self.register_map.items()]
        )

    def to_json(self) -> dict[str, Union[str, float]]:
        return {
            register: {"Register": register, "value": value}
            for register, value in self.register_map.items()
        }

    def reset(self) -> None:
        self.register_map = {f"F{i}": 0.0 for i in range(32)}


class Memory:
    __shared_instance = None

    @staticmethod
    def get_instance():
        if Memory.__shared_instance is None:
            Memory()
        return Memory.__shared_instance

    def __init__(self):
        if Memory.__shared_instance is not None:
            raise Exception("This class is a singleton!")

        Memory.__shared_instance = self
        self.memory_map: dict[int, Union[str, float]] = {i: 0.0 for i in range(100)}

    def get_memory_value(self, address: int) -> Union[str, float]:
        return self.memory_map[address]

    def set_memory_value(self, address: int, value: Union[str, float]) -> None:
        self.memory_map[address] = value

    def to_json(self) -> dict[int, Union[str, float]]:
        return {
            str(index): {"address": address, "value": value}
            for index, (address, value) in enumerate(self.memory_map.items())
        }

    def reset(self) -> None:
        self.memory_map = {i: 0.0 for i in range(100)}
