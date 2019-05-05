import sys
import os
from core import thread_worker
import urllib2
from HTMLParser import HTMLParser


parent_folder = os.path.dirname(__file__)
sys.path.append(parent_folder)


def check_website(url):
    try:
        urllib2.urlopen(url)
    except Exception as e:
        print e


class LinksParser(HTMLParser, object):
    _tag = "a" # <a href=link>name</a>
    _attr = "href"

    def __init__(self):
        super(LinksParser, self).__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == tag:
            for attr in attrs:
                if attr[0] == self._attr:
                    self.links.append(attr[1])



url = "https://start.fedoraproject.org/"

response = urllib2.urlopen(url)
encoding = response.headers.getparam('charset')
html = response.read().decode(encoding)

links_parser = LinksParser()
links_parser.feed(html)
response.close()

# starting the pool
workers_poll = thread_worker.Pool(10)
workers_poll.set_job(check_website)
for link in links_parser.links:
    workers_poll.add_job(link)

workers_poll.wait()

import time
def timer(sec):
    time.sleep(sec)
    print "Finished Sleep."

workers_poll.set_job(timer)

for i in xrange(10):
    workers_poll.add_job(.1)

workers_poll.join()
