from abc import ABC, abstractmethod


class Instruction(ABC):
    def __init__(self) -> None:
        self.operation = None


class TwoOperandInstruction(Instruction, ABC):
    def __init__(
        self, latency: int, des: str, first_operand: str, second_operand: str
    ) -> None:
        super().__init__()
        self.latency = latency
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
        super().__init__()
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
        from .components import RegisterFile, Memory

        Memory.get_instance().set_memory_value(
            self.address, RegisterFile.get_instance().get_register_value(self.des)
        )
        return 0.0

    def get_buffer(self) -> str:
        return "S"


class InstructionFactory:
    def __init__(self, tokens: list[str], latencies: dict[str, int]) -> None:
        self.tokens = tokens
        self.latencies = latencies
        self.operation = tokens[0]

    def get_instruction(self) -> Instruction:
        match self.operation:
            case "ADD.D":
                return AddInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
            case "SUB.D":
                return SubInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
            case "MUL.D":
                return MulInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
            case "DIV.D":
                return DivInstruction(
                    self.latencies[self.operation],
                    self.tokens[1],
                    self.tokens[2],
                    self.tokens[3],
                )
            case "L.D":
                return LoadInstruction(
                    self.latencies[self.operation], self.tokens[1], int(self.tokens[2])
                )
            case "S.D":
                return StoreInstruction(
                    self.latencies[self.operation], self.tokens[1], int(self.tokens[2])
                )

        raise Exception(f"Invalid operation: {self.operation}")
