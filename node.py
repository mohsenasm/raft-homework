# import sys, signal
import argparse

######## TODO: provide methods/functions to use in main function ########
######## intrested methods/functions include: add, sub, mul, get

#########################################################################

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--init_value', dest='init_value', default=0)
    parser.add_argument('-m', '--my_port', dest='my_port', required=True)
    parser.add_argument('-o', '--other_ports', dest='other_ports', nargs="+", 
                        default=["a", "b"], required=True)

    params = parser.parse_args()

    print("* start node", params.my_port, "with init value", int(params.init_value))
    print("* others are:", " ".join(params.other_ports))

    ######## TODO: initialize if needed ########

    ############################################
    
    prompt_text = '* Enter a command: \n'
    line = input(prompt_text)
    while line:
        if line.startswith("add"):
            number = int(line.split()[1])
            ######## TODO: call "add" ########

            ##################################
            print("* commit command:", line, flush=True)
        elif line.startswith("sub"):
            number = int(line.split()[1])
            ######## TODO: call "sub" ########

            ##################################
            print("* commit command:", line, flush=True)
        elif line.startswith("mul"):
            number = int(line.split()[1])
            ######## TODO: call "mul" ########

            ##################################
            print("* commit command:", line, flush=True)
        elif line.startswith("get"):
            ######## TODO: call "get" ########

            ##################################
            pass
        try:
            line = input(prompt_text)
        except EOFError:
            # sys.exit(0)
            return

if __name__ == "__main__":
    # def handler_stop_signals(signum, frame):
    #     sys.exit(0)
    # signal.signal(signal.SIGINT, handler_stop_signals)
    # signal.signal(signal.SIGTERM, handler_stop_signals)

    main()
