
"""Module to help generic ppol of thread workers.

Reference:

    http://code.activestate.com/recipes/576519-thread-pool-with-same-api-as-multiprocessingpool/
"""
import Queue
import threading

from core import ProgressPrint
from core import logger


logger = logger.setup_logger()


class Job(object):
    def __init__(self,func,args,kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self.out = None

    def process(self):
        self.out = self._func(*self._args,**self._kwargs)


class PoolWorker(threading.Thread):
    _kill_cmd="DIE"
    def __init__(self, work_queue,*args,**kwargs):
        super(PoolWorker, self).__init__(*args,**kwargs)
        self._work_queue = work_queue

    def run(self):
        while True:
            next_job = self._work_queue.get()
            if isinstance(next_job,str) and next_job == self._kill_cmd:
                logger.debug("Recieved Kill cmd.")
                break
            try:
                next_job.process()
            except Exception as e:
                logger.error("Job with %s has errored. %s\n%s",next_job._args,e.message,e.args)
            self._work_queue.task_done()
        logger.debug("Finished Processing.")


class Pool(object):
    def __init__(self,n_workers):

        self._work_queue = Queue.Queue()
        self._workers = []
        self._current_func = None
        for id in xrange(n_workers):
            thr = PoolWorker(self._work_queue)
            thr.start()
            self._workers.append(thr)
        logger.info("Started %s Threads" % n_workers)

    def join(self):
        logger.debug("Waiting for all threads to complete.")
        for thr in self._workers:
            self._work_queue.put("DIE")
        for thr in self._workers:
            thr.join()

    def wait(self):
        logger.debug("Starting Wait to finish current queue.")
        progress = ProgressPrint()
        progress.start()
        self._work_queue.join()
        progress.stop()


    def terminate(self):
        logger.debug("Terminating all threads")
        try:
            while True:
                self._work_queue.get_nowait()
        except Queue.Empty:
            logger.debug("Queue is Empty")

        for thr in self._workers:
            self._work_queue.put("DIE")

    def add_job(self,*args,**kwargs):
        logger.debug("Added new job with %s",args)
        self._work_queue.put(
            Job(self._current_func,args,kwargs)
        )

    def set_job(self,func):
        self._current_func = func
