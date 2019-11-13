import sys
import os
import time


import test_base
from core import process_worker


parent_folder = os.path.dirname(__file__)
sys.path.append(parent_folder)


def timer(sec):
    time.sleep(sec)
    print("Finished Sleep.")

# starting the pool
workers_poll = process_worker.Pool(10)


# workers_poll.wait()

workers_poll.set_job(timer, "time")

for i in range(10):
    workers_poll.add_job_data(10, tag="time")

workers_poll.join()