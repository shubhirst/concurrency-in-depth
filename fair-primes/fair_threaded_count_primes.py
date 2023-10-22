import math
import time
import threading
import multiprocessing
import os

MAX_NUM = 10000000
NUM_THREADS = 5

global total_primes
total_primes = 0

global atomic_update_lock
atomic_update_lock = threading.Lock()

global curr_num
curr_num = 1

global atomic_fetch_lock
atomic_fetch_lock = threading.Lock()

def atomic_update_total_primes():
    global atomic_update_lock
    global total_primes
    with atomic_update_lock:
        total_primes += 1

def atomic_fetch_current_num():
    global curr_num
    global atomic_fetch_lock
    with atomic_fetch_lock:
        curr_num += 1
        return curr_num

def is_prime(n):
    if n <= 1:
        return False
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n+1):
        if n % i == 0:
            return False
    return True

def count_primes():
    print(f'{threading.current_thread().name} starting')
    st = time.time()
    while True:
        n = atomic_fetch_current_num()
        if n > MAX_NUM:
            break
        if is_prime(n):
            atomic_update_total_primes()
    print(f'{threading.current_thread().name} took {time.time()-st} seconds]')

if __name__ == '__main__':
    start = time.time()
    batch_size = int(MAX_NUM/NUM_THREADS)
    all_threads = []
    for i in range(NUM_THREADS):
        th = threading.Thread(target=count_primes, name=f'Thread-{i}')
        all_threads.append(th)
    for th in all_threads:
        th.start()
    for th in all_threads:
        th.join()

    print(f'Found {total_primes} primes till {MAX_NUM} in {time.time()-start} seconds')
