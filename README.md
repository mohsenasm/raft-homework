# Raft Homework

Here we have an incomplete implementation of a **distributed calculator**. This program has some HTTP POST APIs to receive `addition`, `subtraction`, and `multiplication` commands, as well as an HTTP GET API to return the current replicated result. It also has a web-based dashboard to facilitate issuing these commands and seeing the result on each node.

The requirement is syncing these commands with the other nodes in an asynchronous and fault-resilient way, with the _Raft consensus algorithm_.

# Demo & Development

You can run the nodes manually and use the web-based dashboards to test your implementation.

```bash
python3 node.py -i 50 -m 10101 -o 10103 10102 -p 9010
python3 node.py -i 50 -m 10102 -o 10103 10101 -p 9020
python3 node.py -i 50 -m 10103 -o 10102 10101 -p 9030
```

![demo](https://github.com/mohsenasm/raft-homework/assets/9164422/fc88ec50-d7db-40ac-8664-573726223dc1)

## What you need to do

This homework has three sections:

1.  You should use the raft protocol and complete the `consensus.py` file to pass all test cases. There is no need to change other files.
     + There are some test cases provided in the `test.py` file. You can run them with `python3 test.py`.
3.  Explain in the Raft terminology, how nodes interact with each other in the `test_failure_and_recovery` test case.
4.  Explain in the Raft terminology, why `test_weird` passes.

Note that:
+ Usage of the third-party packages is permitted.
+ If you want to solve this homework with another programming language, you can write your own `node` program and still use `python3 test.py` to test it. In this case, you should change `RUN_PREFIX` in the `test.py` file to address the executable of your `node` program.
+ You should not change the `test.py` file unless you need to change the `PYTHON_ADDR` or `RUN_PREFIX` constants.
+ You should not store/retrieve anything on/from the persistent storage. All communication between the `nodes` should be network-based.
+ You should not use `time.sleep` in the `consensus.py` file if you use the third-party packages.
+ Please Star :star: this repository to make it reach more people :) :heart:.
