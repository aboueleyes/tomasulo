from src.instructions_parser import InstructionParser
from src.tomasulo import Tomasulo
from src.components import Memory, RegisterFile
from src.reservation import ReservationAreas
from src.buffer import BufferAreas
import argparse
import yaml
from rich.console import Console
from time import sleep
import json

console = Console()


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
    # import ipdb
    # ipdb.set_trace()
    Memory.get_instance().set_memory_value(0, 1.0)
    tomo = Tomasulo(instructions=instructions)
    current_cycle = 1
    with console.status("[bold green]Running...") as status:
        while tomo.is_running():
            # console.log(f"Cycle: {current_cycle}")
            # sleep(1)
            tomo.unlock_all_entries()
            tomo.issue_instruction()
            tomo.execute()
            tomo.write_back()
            current_cycle += 1
            print(
                json.dumps(
                    {
                        "buffer": BufferAreas.get_instance().to_json(),
                        "reservation": ReservationAreas.get_instance().to_json(),
                        "memory": Memory.get_instance().to_json(),
                        "registers": RegisterFile.get_instance().to_json(),
                        "cycle": current_cycle,
                    },
                    indent=4,
                )
            )


if __name__ == "__main__":
    main()
