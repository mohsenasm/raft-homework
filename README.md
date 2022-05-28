
# Raft Homework

This repo is provided to test your basic knowledge of the *Raft consensus algorithm* and help you to implement and test a basic use case of this algorithm.

## The Node Program

There are two files in this repo, `node.py` and `test.py`.

The `node.py` is a program that could interact with other `node.py`s to maintain an integer and perform some operations on it. This program will get these inputs as command-line arguments:

| Flag | Type | Description |
|------|------|-------------|
| --init_value | Integer | The initial value for the state parameter |
| --my_port | Integer | The port of this node that will be used for communication with other nodes |
| --other_ports | Integers separated by space | The port of the other nodes |

The `node.py` supports these four operations:

| Operation | Operand | Example Command | Meaning |
|----------|----------|---------|------|
| add | An integer | `add -5` | Add the input to the state
| sub | An integer | `sub 22` | Subtract the input from the state
| mul | An integer | `mul 1` | Multiply the input and the state
| get | - | `get` | Print the state


The user can write these commands in the node's stdin and see the output (if any) in the stdout. Users can issue any command to any node.

The requirement is syncing these commands with different instances in an asynchronous and fault resilient way.

## What you need to do

There are some test cases provided in the `test.py` file.

1.  You should use the raft protocol and complete the `TODO` sections in the `node.py` file to pass all test cases.
2.  Explain in the Raft terminology, how nodes interact with each other in the `test_failure_and_recovery` test case.
3.  Explain in the Raft terminology, why `test_weird` passes.


Note that:
+ You can run the test cases with `python3 test.py`.
+ Usage of the third-party packages is permitted.
+ You should not change the `test.py` file unless you need to change the `PYTHON_ADDR` constant.
+ If you need to `print` something, start the line with `*`.
+ You should not store/retrieve anything on/from the persistent storage.
+ You should not use `time.sleep`, in the `node.py` file, if you use the third-party packages.
+ Please Star :star: this repository to make it reach more people :) :heart:.
