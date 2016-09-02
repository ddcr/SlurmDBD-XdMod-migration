#!/usr/bin/env python
# @Author: ddcr
# @Date:   2016-08-28 23:42:05
# @Last Modified by:   ddcr
# @Last Modified time: 2016-08-30 16:19:03
from sqlalchemy.orm import scoped_session, sessionmaker
import logging
import sys
from multiprocessing import Manager, cpu_count, Process

from producers import SlurmJobReader
from consumers import create_mysql_pool, batch_insert_xdmod

logger = logging.getLogger('slurm_database_parser')
logger.setLevel(logging.DEBUG)
logging.basicConfig()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def producer_queue(queue, dbreader):
    raise NotImplementedError


def consumer_queue(proc_id, queue):
    # mysql_pool = create_mysql_pool()
    raise NotImplementedError


class SlurmDBD2XModManager(object):
    """See https://pymotw.com/2/multiprocessing/index.html
    mysql -uddcr -pbrigh99 --host=localhost --port=3306
          --socket=/var/lib/mysql/mysql.sock mod_shredder
    """

    def __init__(self):
        self.manager = Manager()
        self.queue = self.manager.Queue()
        self.processor_count = cpu_count()
        self.dbreader = SlurmJobReader()

    def start(self):
        self.producer = Process(target=producer_queue,
                                args=(self.queue, self.dbreader))
        self.producer.start()

        self.consumers = [Process(target=consumer_queue,
                                  args=(i, self.queue,))
                          for i in xrange(self.processor_count)]
        for w in self.consumers:
            w.start()

    def join(self):
        self.producer.join()
        for w in self.consumers:
            w.join()

if __name__ == '__main__':
    try:
        slurmdbd_manager = SlurmDBD2XModManager()
        slurmdbd_manager.start()
        slurmdbd_manager.join()
    except (KeyboardInterrupt, SystemExit):
        logger.info('interruot signal received')
        sys.exit(1)
    except Exception, e:
        raise e
