import unittest
import subprocess
import time

PYTHON_ADDR = "python3"
FILE_NAME = "node.py"
run_prefix = PYTHON_ADDR + " " + FILE_NAME

class TestBasics(unittest.TestCase):
    def test_add(self):
        print("========== test_add ==========")

        n1 = Node(run_prefix + " -i 0 -m 8001 -o 8002 8003")
        n2 = Node(run_prefix + " -i 0 -m 8002 -o 8001 8003")
        n3 = Node(run_prefix + " -i 0 -m 8003 -o 8002 8001")

        n1.run()
        n2.run()
        n3.run()

        time.sleep(2)

        n1.send_command("add 10")
        n2.send_command("add -5")
        n3.send_command("add 1")

        time.sleep(2)

        self.assertEqual(n1.get_data(), 6)
        self.assertEqual(n2.get_data(), 6)
        self.assertEqual(n3.get_data(), 6)

        n1.terminate()
        n2.terminate()
        n3.terminate()
    
    def test_add_sub_mul(self):
        print("========== test_add_sub_mul ==========")

        n1 = Node(run_prefix + " -i 5 -m 8001 -o 8002 8003")
        n2 = Node(run_prefix + " -i 5 -m 8002 -o 8001 8003")
        n3 = Node(run_prefix + " -i 5 -m 8003 -o 8002 8001")

        n1.run()
        n2.run()
        n3.run()

        time.sleep(2)

        expected_value = 5

        n1.send_command("add 10")
        expected_value += 10
        n2.send_command("sub -5")
        expected_value -= -5
        n3.send_command("mul 2")
        expected_value *= 2

        time.sleep(2)

        self.assertEqual(n1.get_data(), expected_value)
        self.assertEqual(n2.get_data(), expected_value)
        self.assertEqual(n3.get_data(), expected_value)

        n1.terminate()
        n2.terminate()
        n3.terminate()
    
    def test_add_sub_mul_heavy(self):
        print("========== test_add_sub_mul_heavy ==========")
        n1 = Node(run_prefix + " -i 8 -m 8001 -o 8002 8003")
        n2 = Node(run_prefix + " -i 8 -m 8002 -o 8001 8003")
        n3 = Node(run_prefix + " -i 8 -m 8003 -o 8002 8001")

        n1.run()
        n2.run()
        n3.run()

        time.sleep(2)

        expected_value = 8

        n1.send_command("add 10")
        expected_value += 10
        n2.send_command("sub -5")
        expected_value -= -5
        n3.send_command("mul 2")
        expected_value *= 2

        n1.send_command("sub 2")
        expected_value -= 2
        n2.send_command("add -3")
        expected_value += -3
        n3.send_command("mul 4")
        expected_value *= 4
        
        n1.send_command("mul 7")
        expected_value *= 7
        n2.send_command("add -12")
        expected_value += -12
        n3.send_command("sub 9")
        expected_value -= 9

        time.sleep(2)

        self.assertEqual(n1.get_data(), expected_value)
        self.assertEqual(n2.get_data(), expected_value)
        self.assertEqual(n3.get_data(), expected_value)

        n1.terminate()
        n2.terminate()
        n3.terminate()

class TestFailure(unittest.TestCase):
    def test_failure_and_recovery(self):
        print("========== test_failure_and_recovery ==========")

        n1 = Node(run_prefix + " -i 2 -m 8001 -o 8002 8003")
        n2 = Node(run_prefix + " -i 2 -m 8002 -o 8001 8003")
        n3 = Node(run_prefix + " -i 2 -m 8003 -o 8002 8001")

        n1.run()
        n2.run()
        n3.run()

        time.sleep(2)

        n1.send_command("add 5")
        n2.send_command("sub -5")
        n3.send_command("mul -4")

        time.sleep(2)

        self.assertEqual(n1.get_data(), -48)
        self.assertEqual(n2.get_data(), -48)
        self.assertEqual(n3.get_data(), -48)

        n2.terminate()
        
        time.sleep(10)

        n1.send_command("mul 2")
        n3.send_command("add -4")

        time.sleep(2)

        self.assertEqual(n1.get_data(), -100)
        self.assertEqual(n3.get_data(), -100)

        n2.run()

        time.sleep(10)

        self.assertEqual(n2.get_data(), -100)

        n1.terminate()
        n2.terminate()
        n3.terminate()

class TestWeird(unittest.TestCase):
    def test_weird(self): # should pass
        print("========== test_weird ==========")

        n1 = Node(run_prefix + " -i 0 -m 8001 -o 8002 8003")
        n2 = Node(run_prefix + " -i 4 -m 8002 -o 8001 8003")
        n3 = Node(run_prefix + " -i 0 -m 8003 -o 8002 8001")

        n1.run()
        n2.run()
        n3.run()

        time.sleep(2)

        n1.send_command("add 10")
        n2.send_command("add -5")
        n3.send_command("add 1")

        time.sleep(2)

        self.assertEqual(n1.get_data(), 6)
        self.assertEqual(n2.get_data(), 10)
        self.assertEqual(n3.get_data(), 6)

        n1.terminate()
        n2.terminate()
        n3.terminate()

class Node:
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None
    
    def run(self):
        self.process = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def terminate(self):
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.terminate()
        self.process.wait()

    def send_command(self, command, wait_for_commit=True):
        print("sending command:", command)
        self.process.stdin.write((command+"\n").encode('utf-8') )
        self.process.stdin.flush()
        if wait_for_commit:
            print("wait for commit:", command)
            self.read_until_commit_command(command)
    
    def read_until_commit_command(self, command):
        line = self.process.stdout.readline().decode().strip()
        while not line.startswith("* commit command: {}".format(command)):
            line = self.process.stdout.readline().decode().strip()

    def get_data(self):
        self.send_command("get", wait_for_commit=False)
        line = self.process.stdout.readline().decode().strip()
        while not line.startswith("* current value is:"):
            line = self.process.stdout.readline().decode().strip()
        value = int(line.split(":")[1].strip())
        print("got value:", value)
        return value


if __name__ == '__main__':
    unittest.main()
