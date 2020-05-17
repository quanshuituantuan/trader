import os
from multiprocessing import Process
from monitor import LOFMonitor

def LOF_proc():
    m = LOFMonitor()
    m.run()

if __name__ == '__main__':
    p = Process(target=LOF_proc)
    p.start()
    p.join()
    