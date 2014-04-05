import threading
import subprocess
import queue
import logging
import argparse

def pinger(q, fileName):
    logger = logging.getLogger('logName')
    if not logger.hasHandlers():
        hdlr = logging.FileHandler(fileName)
        hdlr.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    while True:
        ip = q.get()
        with open('NUL', 'w') as f:
            returnValue = subprocess.call('ping {0}'.format(ip),
                                           stdout=f, stderr=f)
        if returnValue == 0:
            logger.info(ip)
        q.task_done()

if __name__ == '__main__':
    num_threads = 4
    taskQueue = queue.Queue()

    for i in range(num_threads):
        t = threading.Thread(target=pinger, args=(taskQueue, 'testFile.txt'))
        t.setDaemon(True)
        t.start()
    parser = argparse.ArgumentParser()
    parser.add_argument('ips', type=str, nargs='+', help='ips to ping')
    args = parser.parse_args()
    for i in args.ips:
        taskQueue.put(i)
    taskQueue.join()