from src.instructions_parser import InstructionParser
from src.tomasulo import Tomasulo
from src.components import Memory
import argparse
import yaml
from rich.console import Console
import logging
from rich.logging import RichHandler
import yaml
from rich.console import Console
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

console = Console()


def main():
    """
    Main function to run the Tomasulo algorithm.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="./sample-instructions.txt")
    args = parser.parse_args()
    # TODO: this default value should be read from a config file
    yaml_file = open("./config.yml")
    instruction_latencies: dict[str, int] = yaml.load(yaml_file, Loader=yaml.FullLoader)

    instructions_parser = InstructionParser(latencies=instruction_latencies)
    instructions_parser.read_file(file_name=args.file)
    instructions = instructions_parser.get_instructions()
    # Memory.get_instance().set_memory_value(0, 1.0)
    tomo = Tomasulo(instructions=instructions, debug=True)

    with console.status("[bold green]Running...") as status:
        while tomo.is_running():
            log.info(f"Cycle: {tomo.current_cycle}")
            # import ipdb; ipdb.set_trace()
            tomo.tick()
            # time.sleep(1.8)
            console.clear()
            if tomo.debug:
                # time.sleep(0.5)
                tomo._print_instructions_queue()
                # time.sleep(0.5)
                tomo._print_reservation_areas()
                # time.sleep(0.5)
                tomo._print_buffer_tables()
                # time.sleep(0.5)
                tomo._print_memory()
                # time.sleep(0.5)
                tomo._print_register_file()
        tomo._print_final_queue()

if __name__ == "__main__":
    main()