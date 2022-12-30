from src.instructions_parser import InstructionParser
from src.tomasulo import Tomasulo
from src.components import Memory, RegisterFile
from src.reservation import ReservationAreas
from src.buffer import BufferAreas
import argparse
import yaml
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="./sample-instructions.txt")
    args = parser.parse_args()
    # TODO: this default value should be read from a config file
    yaml_file = open("./config.yml")
    instruction_latencies: dict[str, int] = yaml.load(yaml_file, Loader=yaml.FullLoader)

    instructions_parser = InstructionParser(latencies=instruction_latencies)
    instructions_parser.read_file(file_name=args.file)
    instructions = instructions_parser.get_instructions()
    Memory.get_instance().set_memory_value(0, 1.0)
    tomo = Tomasulo(instructions=instructions)
    current_cycle = 1
    out = []

    json_out = lambda current_cycle: {
        "buffer": BufferAreas.get_instance().to_json(),
        "reservation": ReservationAreas.get_instance().to_json(),
        "memory": Memory.get_instance().to_json(),
        "registers": RegisterFile.get_instance().to_json(),
        "cycle": current_cycle,
    }

    while tomo.is_running():
        out.append(json_out(current_cycle))
        tomo.tick()
        current_cycle += 1
    out.append(json_out(current_cycle))
    print(json.dumps(out, indent=4))


if __name__ == "__main__":
    main()
