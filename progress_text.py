# -*- coding: utf-8 -*-
import threading
import itertools
import sys

# These dont work in windows :(
# u"🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚"
# u"⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
# u"⟲↺"
class ProgressPrint(threading.Thread):
    progress_symbols = itertools.cycle("<^>_")

    def __init__(self, *args, **kwargs):
        super(ProgressPrint, self).__init__(*args, **kwargs)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            sys.stdout.write("%s" % next(self.progress_symbols))
            sys.stdout.flush()
            sys.stdout.write("\b")

    def stop(self):
        self.event.set()