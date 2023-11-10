import argparse
from consensus import ConsensusManager

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init_value', dest='init_value', default=0)
    parser.add_argument('-m', '--my_port', dest='my_port', required=True)
    parser.add_argument('-o', '--other_ports', dest='other_ports', nargs="+", required=True)

    params = parser.parse_args()

    print("* start node", params.my_port, "with init value", int(params.init_value))
    print("* others are:", " ".join(params.other_ports))

    consensus_manager = ConsensusManager(int(params.init_value), params.my_port, params.other_ports)
    
    prompt_text = '* Enter a command: \n'
    line = input(prompt_text)
    while line:
        if line.startswith("add"):
            number = int(line.split()[1])
            consensus_manager.add(number)
            print("* commit command:", line, flush=True)
        elif line.startswith("sub"):
            number = int(line.split()[1])
            consensus_manager.sub(number)
            print("* commit command:", line, flush=True)
        elif line.startswith("mul"):
            number = int(line.split()[1])
            consensus_manager.mul(number)
            print("* commit command:", line, flush=True)
        elif line.startswith("get"):
            value = consensus_manager.get()
            print("* current value is:", value)
        try:
            line = input(prompt_text)
        except EOFError:
            return

if __name__ == "__main__":
    main()
