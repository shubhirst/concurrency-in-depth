import threading
import sys
print(sys.getswitchinterval())
# sys.setswitchinterval(sys.getswitchinterval() / 10000.00)
# print(sys.getswitchinterval())
i = 0
n_iter = 10000000
n_threads = 100
def test():
    global i
    # import time
    # st = time.time()
    for x in range(n_iter):
        i += 1
    # print((time.time()-st)*1000)

threads = [threading.Thread(target=test) for t in range(n_threads)]
for t in threads:
    t.start()

for t in threads:
    t.join()

print(f'Value of count incremented {n_iter} times by {n_threads} threads is {i}')
