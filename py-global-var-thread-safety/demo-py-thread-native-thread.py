import threading
import time

def sleep():
    time.sleep(60)

all_th = [threading.Thread(target=sleep) for i in range(5)]
for th in all_th:
    th.start()
for th in all_th:
    th.join()
'''
#! /bin/bash
ps -ef | grep demo-py-thread-native-thread
ps -efMp <pid from the first command> -- this should display 6 results, one for the main thread and other five for the spawned threads
'''