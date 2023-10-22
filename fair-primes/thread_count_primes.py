import math
import time
import threading
import multiprocessing
import os

MAX_NUM = 1000000
NUM_THREADS = 10

global total_primes
total_primes = 0

global atomic_update_lock
atomic_update_lock = threading.Lock()

def atomic_update_total_primes():
    global atomic_update_lock
    global total_primes
    with atomic_update_lock:
        total_primes += 1

def is_prime(n):
    if n <= 1:
        return False
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n+1):
        if n % i == 0:
            return False
    return True

def count_primes(start, end_exclusive):
    print(f'{threading.current_thread().name} starting')
    st = time.time()
    for i in range(start, end_exclusive):
        if is_prime(i):
            atomic_update_total_primes() + 1
    print(f'{threading.current_thread().name} completed range [{start}, {end_exclusive}) in {time.time()-st} seconds]')

if __name__ == '__main__':
    # print(f'Found {os.cpu_count()} cores on the system')
    # print(f'Process is using {multiprocessing.cpu_count()} cores')
    start = time.time()
    batch_size = int(MAX_NUM/NUM_THREADS)
    all_threads = []
    for i in range(NUM_THREADS-1):
        st = 2 + i * batch_size
        th = threading.Thread(target=count_primes, name=f'Thread-{i}', args=(st, st+batch_size))
        all_threads.append(th)
    th = threading.Thread(target=count_primes,  name=f'Thread-{NUM_THREADS-1}', args=(2 + (NUM_THREADS-1)*batch_size, MAX_NUM))
    all_threads.append(th)
    for th in all_threads:
        th.start()
    for th in all_threads:
        th.join()

    print(f'Found {total_primes} primes till {MAX_NUM} in {time.time()-start} seconds')
