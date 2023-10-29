I wrote this program to demo that global variables are not thread safe.
The program declares a global variable `count` and launches 10 threads, each incrementing the variable by one, 1M times.
If the variable `count` was thread-safe, its final value should be 1M*10 i.e.`10M`

I executed the script using Py 3.11, but even over multiple executions I always got the correct value.
```
python3.11 global-thread-unsafe.py

Value of count incremented 1000000 times by 10 threads is 10000000
```

Next I tried Py 3.9 and got values < 10M
```
python3.9 global-thread-unsafe.py

Value of count incremented 1000000 times by 10 threads is 3519031
Traceback (most recent call last):
  File "/Users/shubhirastogi/shubhirastogi-git/concurrency-in-depth/py-global-var-thread-safety/global-thread-unsafe.py", line 47, in <module>
    assert i == 1000000*10 , i
AssertionError: 3519031

--

Value of count incremented 1000000 times by 10 threads is 4310974
Traceback (most recent call last):
  File "/Users/shubhirastogi/shubhirastogi-git/concurrency-in-depth/py-global-var-thread-safety/global-thread-unsafe.py", line 47, in <module>
    assert i == 1000000*10 , i
AssertionError: 4310974
```

The global variable _seems_ thread safe in Py3.11, but not in Py3.9, but Why? Looks at this [SO answer](https://stackoverflow.com/a/70006722)
Let's check the [[byte code]] for the incr function in both versions using the [[dis]] package to generate [[byte code]]. But before that, a few pointers about Python byte code
1. Py byte code ops are atomic
2. A note from SO answer about how GIL switches Py threads
[!NOTE]
> Only a single bytecode instruction is ‘atomic’ in CPython, and a += may not result in a single opcode, even when the values involved are simple integers [SO answer](https://stackoverflow.com/a/1717514)

> += 1 resolves to four opcodes: load i, load 1, add the two, and store it back to i. The Python interpreter switches active threads (by releasing the GIL from one thread so another thread can have it) every 100 opcodes. (Both of these are implementation details.) The race condition occurs when the 100-opcode preemption happens between loading and storing, allowing another thread to start incrementing the counter. When it gets back to the suspended thread, it continues with the old value of "i" and undoes the increments run by other threads in the meantime [SO answer](https://stackoverflow.com/a/1717514)
The above answer is old and this [SO answer](https://stackoverflow.com/a/39353531) mentions that GIL's thread switching criteria changed between Py2 and Py3. Py2 switched threads per 100 byte code instructions, while Py3 switches after some time has passed. This value is 5ms by default and can be changed by `sys.setswitchinterval`
But what explains the difference between 3.9 and 3.11? [SO answer](https://stackoverflow.com/a/70006722)

The main takeaways are:
1. In Py only a single bytecode instruction is atomic. If your function accesses the same variable over multiple byte codes, it's not thread safe
2. GIL switching criteria in terms of num of ops or time elapsed are implementation details and could change. To write a thread safe code you should use locks and not rely on the implementation details.

```
global count
def inc():
    for i in range(100000):
        count+=1
import dis
print(dis.dis(inc))
```

```
# Py3.11
48           0 RESUME                   0

50           2 LOAD_GLOBAL              0 (c)
            14 LOAD_CONST               1 (1)
            16 BINARY_OP               13 (+=)
            20 STORE_GLOBAL             0 (c)
            22 LOAD_CONST               0 (None)
            24 RETURN_VALUE
None

# Py3.9
50            0 LOAD_GLOBAL              0 (c)
              2 LOAD_CONST               1 (1)
              4 INPLACE_ADD
              6 STORE_GLOBAL             0 (c)
              8 LOAD_CONST               0 (None)
             10 RETURN_VALUE
None
```