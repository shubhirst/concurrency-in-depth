# a simple queue
import threading
import random
import time
import queue

class Queue:
    def __init__(self) -> None:
        self.q = list()
        self.lock = threading.Lock()

    def enqueue(self, item):
        with self.lock:
            self.q.append(item)

    def dequeue(self):
        with self.lock:
            if len(self.q) == 0:
                raise Exception('Trying to dequeue from an empty queue')
            # time.sleep(0.01)
            item = self.q[0]
            self.q = self.q[1:]
            return item

    def size(self):
        with self.lock:
            return len(self.q)

global n_threads, n_iter
n_threads = 10
n_iter = 1000000
n_items = 1000
def main():
    q = Queue()
    # all_threads = [threading.Thread(target=lambda : [q.enqueue(random.randint(1, 1000)) for _ in range(n_iter)]) for _ in range(n_threads)]
    for _ in range(n_items):
        q.enqueue(random.randint(1, 1000))
    assert q.size() == n_items, q.size()
    # for th in all_threads:
    #     th.start()
    # for th in all_threads:
    #     th.join()
    all_threads = [threading.Thread(target=lambda : q.dequeue()) for _ in range(n_items)]
    for th in all_threads:
        th.start()
    for th in all_threads:
        th.join()
    print(q.size())
    # assert q.size() == n_iter*n_threads, q.size()

if __name__ == '__main__':
    main()
    # import dis
    # l = []
    # def list_append():
    #     l.append(1)
    # dis.dis(list_append)