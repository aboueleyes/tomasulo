from src.instructions_parser import InstructionParser, Tomasulo


def main():
    instructions_parser = InstructionParser()
    instructions_parser.read_file(file_name='./sample-instructions.txt')
    instructions = instructions_parser.get_instructions()
    # import ipdb; ipdb.set_trace()
    tomo = Tomasulo(instructions=instructions)
    for i in range(10):
        tomo.issue_instruction()
        # if i == 1:
        #     import ipdb
        #     ipdb.set_trace()
        tomo.execute()
        tomo.write_back()


if __name__ == '__main__':
    main()
