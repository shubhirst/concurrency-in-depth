This exercise started to understand the concept of *fairness* when writing concurrent programs by counting prime numbers less than a given large number three ways. But, due to the GIL in Python, a CPU-intensive multi-threaded program performs no better than a single threaded one
NOTE: counting prime numbers is a CPU intensive program, so any benefits come from using multiple CPU cores. A single-core execution will give no benefits no matter how many threads you use. For eg, if you use Go lang or Java which maps user threads to multiple OS threads and has no limitation like GIL, you'd see benefits only when using > 1 core
1. A single threaded implementation
`python fair-primes/simple_count_primes.py`
```
Found 664579 primes till 10000000 in 49.30896806716919 seconds
```
2. A multi-threaded implementation that distributes load in an *unfair* way.
`python fair-primes/thread_count_primes.py`
```
Thread-0 completed range [2, 1000002) in 16.831796169281006 seconds]
Thread-1 completed range [1000002, 2000002) in 29.705273151397705 seconds]
Thread-2 completed range [2000002, 3000002) in 35.007691860198975 seconds]
Thread-3 completed range [3000002, 4000002) in 39.754003047943115 seconds]
Thread-4 completed range [4000002, 5000002) in 42.31215000152588 seconds]
Thread-6 completed range [6000002, 7000002) in 45.70932197570801 seconds]
Thread-5 completed range [5000002, 6000002) in 45.78259611129761 seconds]
Thread-7 completed range [7000002, 8000002) in 46.852120876312256 seconds]
Thread-8 completed range [8000002, 9000002) in 47.82140898704529 seconds]
Thread-9 completed range [9000002, 10000000) in 47.98166298866272 seconds]
Found 664579 primes till 10000000 in 48.5352680683136 seconds
```
3. A multi-threaded implementation that distributes load in a *fair* way
`python fair-primes/fair_threaded_count_primes.py`
```
Thread-0 starting
Thread-1 starting
Thread-2 starting
Thread-4 starting
Thread-3 starting
Thread-2 took 50.47021698951721 seconds]
Thread-4 took 50.44020700454712 seconds]
Thread-0 took 50.500778913497925 seconds]
Thread-3 took 50.41001772880554 seconds]
Thread-1 took 50.488317012786865 seconds]
Found 664579 primes till 10000000 in 50.501325845718384 seconds
```

The fourth approach uses multiprocessing and we can clearly see the benefits of using multiple threads
`python fair-primes/multi_process_count_primes.py`
```
MainThread completed range [2, 2000002) in 5.197677135467529 seconds]
MainThread completed range [2000002, 4000002) in 8.665852069854736 seconds]
MainThread completed range [4000002, 6000002) in 10.79218578338623 seconds]
MainThread completed range [6000002, 8000002) in 12.374121904373169 seconds]
MainThread completed range [8000002, 10000000) in 13.676573991775513 seconds]
Found 664579.0 primes till 10000000 in 13.787221908569336 seconds
```
