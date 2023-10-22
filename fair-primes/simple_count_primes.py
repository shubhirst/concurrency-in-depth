import math
import time
from cProfile import Profile
from pstats import SortKey, Stats

MAX_NUM = 10000000

def is_prime(n):
    if n <= 1:
        return False
    sqrt_n = int(math.sqrt(n))
    for i in range(2, sqrt_n+1):
        if n % i == 0:
            return False
    return True

def count_primes(n):
    total_primes = 0
    for i in range(2, n+1):
        if is_prime(i):
            total_primes += 1
    return total_primes

if __name__ == '__main__':
    st = time.time()
    # t1 = time.perf_counter(), time.process_time()
    total_primes = count_primes(MAX_NUM)
    # with Profile() as profile:
    #     total_primes = count_primes(MAX_NUM)
    #     print(Stats(profile).strip_dirs().sort_stats(SortKey.CALLS).print_stats())
    # t2 = time.perf_counter(), time.process_time()
    # print(f'Real time {t2[0] - t1[0]} seconds. CPU time {t2[1] - t1[1]} seconds')
    print(f'Found {total_primes} primes till {MAX_NUM} in {time.time()-st} seconds')
'''
1M - 78498
10M - 664579
'''