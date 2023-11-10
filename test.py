import unittest
import asyncio.subprocess

PYTHON_ADDR = "python3"
FILE_NAME = "node.py"
run_prefix = PYTHON_ADDR + " " + FILE_NAME

class TestBasics(unittest.IsolatedAsyncioTestCase):
    async def test_add(self):
        print("========== test_add ==========")

        n1 = Node(run_prefix + " -i 0 -m 8001 -o 8002 8003", self)
        n2 = Node(run_prefix + " -i 0 -m 8002 -o 8001 8003", self)
        n3 = Node(run_prefix + " -i 0 -m 8003 -o 8002 8001", self)

        await n1.run()
        await n2.run()
        await n3.run()

        await asyncio.sleep(2)

        await n1.send_command("add 10")
        await n2.send_command("add -5")
        await n3.send_command("add 1")

        await asyncio.sleep(2)

        self.assertEqual(await n1.get_data(), 6)
        self.assertEqual(await n2.get_data(), 6)
        self.assertEqual(await n3.get_data(), 6)

        await n1.terminate()
        await n2.terminate()
        await n3.terminate()
    
    async def test_add_sub_mul(self):
        print("========== test_add_sub_mul ==========")

        n1 = Node(run_prefix + " -i 5 -m 8001 -o 8002 8003", self)
        n2 = Node(run_prefix + " -i 5 -m 8002 -o 8001 8003", self)
        n3 = Node(run_prefix + " -i 5 -m 8003 -o 8002 8001", self)

        await n1.run()
        await n2.run()
        await n3.run()

        await asyncio.sleep(2)

        expected_value = 5

        await n1.send_command("add 10")
        expected_value += 10
        await n2.send_command("sub -5")
        expected_value -= -5
        await n3.send_command("mul 2")
        expected_value *= 2

        await asyncio.sleep(2)

        self.assertEqual(await n1.get_data(), expected_value)
        self.assertEqual(await n2.get_data(), expected_value)
        self.assertEqual(await n3.get_data(), expected_value)

        await n1.terminate()
        await n2.terminate()
        await n3.terminate()
    
    async def test_add_sub_mul_heavy(self):
        print("========== test_add_sub_mul_heavy ==========")
        n1 = Node(run_prefix + " -i 8 -m 8001 -o 8002 8003", self)
        n2 = Node(run_prefix + " -i 8 -m 8002 -o 8001 8003", self)
        n3 = Node(run_prefix + " -i 8 -m 8003 -o 8002 8001", self)

        await n1.run()
        await n2.run()
        await n3.run()

        await asyncio.sleep(2)

        expected_value = 8

        await n1.send_command("add 10")
        expected_value += 10
        await n2.send_command("sub -5")
        expected_value -= -5
        await n3.send_command("mul 2")
        expected_value *= 2

        await n1.send_command("sub 2")
        expected_value -= 2
        await n2.send_command("add -3")
        expected_value += -3
        await n3.send_command("mul 4")
        expected_value *= 4
        
        await n1.send_command("mul 7")
        expected_value *= 7
        await n2.send_command("add -12")
        expected_value += -12
        await n3.send_command("sub 9")
        expected_value -= 9

        await asyncio.sleep(2)

        self.assertEqual(await n1.get_data(), expected_value)
        self.assertEqual(await n2.get_data(), expected_value)
        self.assertEqual(await n3.get_data(), expected_value)

        await n1.terminate()
        await n2.terminate()
        await n3.terminate()

class TestFailure(unittest.IsolatedAsyncioTestCase):
    async def test_failure_and_recovery(self):
        print("========== test_failure_and_recovery ==========")

        n1 = Node(run_prefix + " -i 2 -m 8001 -o 8002 8003", self)
        n2 = Node(run_prefix + " -i 2 -m 8002 -o 8001 8003", self)
        n3 = Node(run_prefix + " -i 2 -m 8003 -o 8002 8001", self)

        await n1.run()
        await n2.run()
        await n3.run()

        await asyncio.sleep(2)

        await n1.send_command("add 5")
        await n2.send_command("sub -5")
        await n3.send_command("mul -4")

        await asyncio.sleep(2)

        self.assertEqual(await n1.get_data(), -48)
        self.assertEqual(await n2.get_data(), -48)
        self.assertEqual(await n3.get_data(), -48)

        await n2.terminate()
        
        await asyncio.sleep(10)

        await n1.send_command("mul 2")
        await n3.send_command("add -4")

        await asyncio.sleep(2)

        self.assertEqual(await n1.get_data(), -100)
        self.assertEqual(await n3.get_data(), -100)

        await n2.run()

        await asyncio.sleep(10)

        self.assertEqual(await n2.get_data(), -100)

        await n1.terminate()
        await n2.terminate()
        await n3.terminate()

class TestWeird(unittest.IsolatedAsyncioTestCase):
    async def test_weird(self): # should pass
        print("========== test_weird ==========")

        n1 = Node(run_prefix + " -i 0 -m 8001 -o 8002 8003", self)
        n2 = Node(run_prefix + " -i 4 -m 8002 -o 8001 8003", self)
        n3 = Node(run_prefix + " -i 0 -m 8003 -o 8002 8001", self)

        await n1.run()
        await n2.run()
        await n3.run()

        await asyncio.sleep(2)

        await n1.send_command("add 10")
        await n2.send_command("add -5")
        await n3.send_command("add 1")

        await asyncio.sleep(2)

        self.assertEqual(await n1.get_data(), 6)
        self.assertEqual(await n2.get_data(), 10)
        self.assertEqual(await n3.get_data(), 6)

        await n1.terminate()
        await n2.terminate()
        await n3.terminate()

class Node:
    def __init__(self, cmd, tester: unittest.TestCase):
        self.cmd = cmd
        self.process = None
        self.tester = tester
    
    async def run(self):
        self.process = await asyncio.create_subprocess_shell(
            self.cmd, shell=True, 
            stdin=asyncio.subprocess.PIPE, 
            stdout=asyncio.subprocess.PIPE)

    async def terminate(self):
        self.process.stdin.close()
        # self.process.stdout.close()
        self.process.terminate()
        await self.process.wait()

    async def send_command(self, command, wait_for_commit=True):
        print("sending command:", command)
        self.process.stdin.write((command+"\n").encode('utf-8') )
        # self.process.stdin.flush()
        if wait_for_commit:
            print("wait for commit:", command)
            await self.read_until_commit_command(command)
    
    async def read_line(self, timeout=5):
        try:
            line = await asyncio.wait_for(self.process.stdout.readline(), timeout=timeout)
            return line.decode().strip()
        except asyncio.TimeoutError:
            self.tester.fail("error: reading line timed out after 5 seconds")
    
    async def read_until_commit_command(self, command):
        line = await self.read_line()
        while not line.startswith("* commit command: {}".format(command)):
            line = await self.read_line()

    async def get_data(self):
        await self.send_command("get", wait_for_commit=False)
        line = await self.read_line()
        while not line.startswith("* current value is:"):
            line = await self.read_line()
        value = int(line.split(":")[1].strip())
        print("got value:", value)
        return value


if __name__ == '__main__':
    unittest.main()
