import unittest, time, subprocess
import requests

PYTHON_ADDR = "python3"
FILE_NAME = "node.py"
RUN_PREFIX = PYTHON_ADDR + " " + FILE_NAME

class TestBasics(unittest.TestCase):
    def test_add(self):
        print("========== test_add ==========")

        n1 = Node(RUN_PREFIX + " -i 0 -m 8001 -o 8002 8003", self)
        n2 = Node(RUN_PREFIX + " -i 0 -m 8002 -o 8001 8003", self)
        n3 = Node(RUN_PREFIX + " -i 0 -m 8003 -o 8002 8001", self)
        try:
            n1.run()
            n2.run()
            n3.run()

            time.sleep(5)

            n1.send_command("add", "10")
            n2.send_command("add", "-5")
            n3.send_command("add", "1")

            time.sleep(5)

            self.assertEqual(n1.get_data(), 6)
            self.assertEqual(n2.get_data(), 6)
            self.assertEqual(n3.get_data(), 6)
        finally:
            n1.terminate()
            n2.terminate()
            n3.terminate()
    
    def test_add_sub_mul(self):
        print("========== test_add_sub_mul ==========")

        n1 = Node(RUN_PREFIX + " -i 5 -m 8001 -o 8002 8003", self)
        n2 = Node(RUN_PREFIX + " -i 5 -m 8002 -o 8001 8003", self)
        n3 = Node(RUN_PREFIX + " -i 5 -m 8003 -o 8002 8001", self)
        try:
            n1.run()
            n2.run()
            n3.run()

            time.sleep(5)

            expected_value = 5

            n1.send_command("add", "10")
            expected_value += 10
            n2.send_command("sub", "-5")
            expected_value -= -5
            n3.send_command("mul", "2")
            expected_value *= 2

            time.sleep(5)

            self.assertEqual(n1.get_data(), expected_value)
            self.assertEqual(n2.get_data(), expected_value)
            self.assertEqual(n3.get_data(), expected_value)
        finally:
            n1.terminate()
            n2.terminate()
            n3.terminate()
    
    def test_add_sub_mul_heavy(self):
        print("========== test_add_sub_mul_heavy ==========")
        n1 = Node(RUN_PREFIX + " -i 8 -m 8001 -o 8002 8003", self)
        n2 = Node(RUN_PREFIX + " -i 8 -m 8002 -o 8001 8003", self)
        n3 = Node(RUN_PREFIX + " -i 8 -m 8003 -o 8002 8001", self)

        try:
            n1.run()
            n2.run()
            n3.run()

            time.sleep(5)

            expected_value = 8

            n1.send_command("add", "10")
            expected_value += 10
            n2.send_command("sub", "-5")
            expected_value -= -5
            n3.send_command("mul", "2")
            expected_value *= 2

            n1.send_command("sub", "2")
            expected_value -= 2
            n2.send_command("add", "-3")
            expected_value += -3
            n3.send_command("mul", "4")
            expected_value *= 4
            
            n1.send_command("mul", "7")
            expected_value *= 7
            n2.send_command("add", "-12")
            expected_value += -12
            n3.send_command("sub", "9")
            expected_value -= 9

            time.sleep(5)

            self.assertEqual(n1.get_data(), expected_value)
            self.assertEqual(n2.get_data(), expected_value)
            self.assertEqual(n3.get_data(), expected_value)
        finally:
            n1.terminate()
            n2.terminate()
            n3.terminate()

class TestFailure(unittest.TestCase):
    def test_failure_and_recovery(self):
        print("========== test_failure_and_recovery ==========")

        n1 = Node(RUN_PREFIX + " -i 2 -m 8001 -o 8002 8003", self)
        n2 = Node(RUN_PREFIX + " -i 2 -m 8002 -o 8001 8003", self)
        n3 = Node(RUN_PREFIX + " -i 2 -m 8003 -o 8002 8001", self)
        try:
            n1.run()
            n2.run()
            n3.run()

            time.sleep(5)

            n1.send_command("add", "5")
            n2.send_command("sub", "-5")
            n3.send_command("mul", "-4")

            time.sleep(5)

            self.assertEqual(n1.get_data(), -48)
            self.assertEqual(n2.get_data(), -48)
            self.assertEqual(n3.get_data(), -48)

            n2.terminate()
            
            time.sleep(10)

            n1.send_command("mul", "2")
            n3.send_command("add", "-4")

            time.sleep(5)

            self.assertEqual(n1.get_data(), -100)
            self.assertEqual(n3.get_data(), -100)

            n2.run()

            time.sleep(10)

            self.assertEqual(n2.get_data(), -100)
        finally:
            n1.terminate()
            n2.terminate()
            n3.terminate()

class TestWeird(unittest.TestCase):
    def test_weird(self): # should pass
        print("========== test_weird ==========")

        n1 = Node(RUN_PREFIX + " -i 0 -m 8001 -o 8002 8003", self)
        n2 = Node(RUN_PREFIX + " -i 4 -m 8002 -o 8001 8003", self)
        n3 = Node(RUN_PREFIX + " -i 0 -m 8003 -o 8002 8001", self)
        try:
            n1.run()
            n2.run()
            n3.run()

            time.sleep(5)

            n1.send_command("add", "10")
            n2.send_command("add", "-5")
            n3.send_command("add", "1")

            time.sleep(5)

            self.assertEqual(n1.get_data(), 6)
            self.assertEqual(n2.get_data(), 10)
            self.assertEqual(n3.get_data(), 6)
        finally:
            n1.terminate()
            n2.terminate()
            n3.terminate()

last_port = 14000
def get_a_port():
    global last_port
    last_port += 1
    return last_port

class Node:
    def __init__(self, cmd, tester: unittest.TestCase):
        self.port = get_a_port()
        self.cmd = cmd + " -p {}".format(self.port)
        self.process = None
        self.tester = tester
    
    def run(self):
        self.process = subprocess.Popen(self.cmd.split())

    def terminate(self):
        self.process.terminate()
        time.sleep(1)
        self.process.wait()
    
    def send_command(self, command, value: int):
        print("run command:", command, value)
        r = requests.post('http://127.0.0.1:{}/{}'.format(self.port, command), data={"value": value}, timeout=5)
        self.tester.assertEqual(r.status_code, 200)
        print("commited command:", command, value)
    
    def get_data(self) -> int:
        r = requests.get('http://127.0.0.1:{}/get'.format(self.port), timeout=5)
        self.tester.assertEqual(r.status_code, 200)
        value = int(r.text)
        print("got value:", value)
        return value

if __name__ == '__main__':
    unittest.main()
