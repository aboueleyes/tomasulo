from abc import ABC, abstractmethod
from typing import Optional


class Instruction(ABC):
    def __init__(self, latency: int) -> None:
        self.operation = None
        self.latency = latency
        self.string_representation: Optional[str] = None
        self.status = None
        self.issued_at_cycle = None
        self.executed_at_cycle = None
        self.written_at_cycle = None


class TwoOperandInstruction(Instruction, ABC):
    def __init__(
        self, latency: int, des: str, first_operand: str, second_operand: str
    ) -> None:
        super().__init__(latency)
        self.des = des
        self.first_operand = first_operand
        self.second_operand = second_operand

    def __str__(self) -> str:
        return f" {self.des} {self.first_operand} {self.second_operand}"

    @abstractmethod
    def get_reservation_area(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calculate(self, first_operand: float, second_operand: float) -> float:
        raise NotImplementedError


class AddInstruction(TwoOperandInstruction):
    def __init__(
        self, latency: int, des: str, first_operand: str, second_operand: str
    ) -> None:
        super().__init__(latency, des, first_operand, second_operand)
        self.operation = "ADD.D"

    def __str__(self) -> str:
        return f"{self.operation} {super().__str__()}"

    __repr__ = __str__

    def calculate(self, first_operand: float, second_operand: float) -> float:
        return first_operand + second_operand

    def get_reservation_area(self) -> str:
        return "A"


class SubInstruction(TwoOperandInstruction):
    def __init__(
        self, latency: int, des: str, first_operand: str, second_operand: str
    ) -> None:
        super().__init__(latency, des, first_operand, second_operand)
        self.operation = "SUB.D"

    def __str__(self) -> str:
        return f"{self.operation} {super().__str__()}"

    __repr__ = __str__

    def calculate(self, first_operand: float, second_operand: float) -> float:
        return first_operand - second_operand

    def get_reservation_area(self) -> str:
        return "A"


class MulInstruction(TwoOperandInstruction):
    def __init__(
        self, latency: int, des: str, first_operand: str, second_operand: str
    ) -> None:
        super().__init__(latency, des, first_operand, second_operand)
        self.operation = "MUL.D"

    def __str__(self) -> str:
        return f"{self.operation} {super().__str__()}"

    __repr__ = __str__

    def calculate(self, first_operand: float, second_operand: float) -> float:
        return first_operand * second_operand

    def get_reservation_area(self) -> str:
        return "M"


class DivInstruction(TwoOperandInstruction):
    def __init__(
        self, latency: int, des: str, first_operand: str, second_operand: str
    ) -> None:
        super().__init__(latency, des, first_operand, second_operand)
        self.operation = "DIV.D"

    def __str__(self) -> str:
        return f"{self.operation} {super().__str__()}"

    __repr__ = __str__

    def calculate(self, first_operand: float, second_operand: float) -> float:
        try:
            return first_operand / second_operand
        except ZeroDivisionError:
            return 0.0

    def get_reservation_area(self) -> str:
        return "M"


class OneOperandInstruction(Instruction, ABC):
    def __init__(self, latency: int, des: str, address: int) -> None:
        super().__init__(latency=latency)
        self.latency = latency
        self.des = des
        self.address = address

    def __str__(self) -> str:
        return f" {self.des} {self.des} {self.address}"

    @abstractmethod
    def get_buffer(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def calculate(self) -> float:
        raise NotImplementedError


class LoadInstruction(OneOperandInstruction):
    def __init__(self, latency: int, des: str, address: int) -> None:
        super().__init__(latency, des, address)
        self.operation = "L.D"

    def __str__(self) -> str:
        return f"{self.operation} {super().__str__()}"

    __repr__ = __str__

    def calculate(self) -> float:
        from .components import Memory

        return Memory.get_instance().get_memory_value(self.address)

    def get_buffer(self) -> str:
        return "L"


class StoreInstruction(OneOperandInstruction):
    def __init__(self, latency: int, des: str, address: int) -> None:
        super().__init__(latency, des, address)
        self.operation = "S.D"

    def __str__(self) -> str:
        return f"{self.operation} {super().__str__()}"

    __repr__ = __str__

    def calculate(self) -> float:
        return 0.0

    def get_buffer(self) -> str:
        return "S"


class InstructionFactory:
    def __init__(self, tokens: list[str], latencies: dict[str, int]) -> None:
        self.tokens = tokens
        self.latencies = latencies
        self.operation = tokens[0]

    def get_instruction(self) -> Instruction:
        string_representation = " ".join(self.tokens)
        match self.operation:
            case "ADD.D":
                add_instruction = AddInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
                add_instruction.string_representation = string_representation
                return add_instruction
            case "SUB.D":
                subtract_instruction = SubInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
                subtract_instruction.string_representation = string_representation
                return subtract_instruction
            case "MUL.D":
                multiply_instruction = MulInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
                multiply_instruction.string_representation = string_representation
                return multiply_instruction
            case "DIV.D":
                divide_instruction = DivInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
                divide_instruction.string_representation = string_representation
                return divide_instruction
            case "L.D":
                load_instruction = LoadInstruction(
                    self.latencies[self.operation], self.tokens[1], int(self.tokens[2])
                )
                load_instruction.string_representation = string_representation
                return load_instruction
            case "S.D":
                store_instruction = StoreInstruction(
                    self.latencies[self.operation], self.tokens[1], int(self.tokens[2])
                )
                store_instruction.string_representation = string_representation
                return store_instruction

        raise Exception(f"Invalid operation: {self.operation}")
