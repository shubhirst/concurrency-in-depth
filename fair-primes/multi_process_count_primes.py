import math
import time
import threading
import multiprocessing
import os

MAX_NUM = 10000000
NUM_THREADS = 5

def is_prime(n):
    if n <= 1:
        return False
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n+1):
        if n % i == 0:
            return False
    return True

def count_primes(count, start, end_exclusive):
    print(f'{threading.current_thread().name} starting')
    local_count = 0
    st = time.time()
    for i in range(start, end_exclusive):
        if is_prime(i):
            local_count += 1
    count.value = local_count
    print(f'{threading.current_thread().name} completed range [{start}, {end_exclusive}) in {time.time()-st} seconds]')

if __name__ == '__main__':
    start = time.time()
    batch_size = int(MAX_NUM/NUM_THREADS)
    all_processes = []
    all_values = []
    for i in range(NUM_THREADS-1):
        count = multiprocessing.Value('d', 0)
        all_values.append(count)
        st = 2 + i * batch_size
        pr = multiprocessing.Process(target=count_primes, name=f'Thread-{i}', args=(count, st, st+batch_size))
        all_processes.append(pr)
    count = multiprocessing.Value('d', 0)
    all_values.append(count)
    pr = multiprocessing.Process(target=count_primes,  name=f'Thread-{NUM_THREADS-1}', args=(count, 2 + (NUM_THREADS-1)*batch_size, MAX_NUM))
    all_processes.append(pr)
    for pr in all_processes:
        pr.start()
    for pr in all_processes:
        pr.join()
    total_primes = sum([count.value for count in all_values])

    print(f'Found {total_primes} primes till {MAX_NUM} in {time.time()-start} seconds')
