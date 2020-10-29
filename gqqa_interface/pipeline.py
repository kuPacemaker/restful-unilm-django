from ABC import ABCMeta, abstractmethod
from collections import deque
import threading

import remote.api as RemoteApi
from base import BaseKnowledge
from qg_interface.protocol import QGProtocol
from gqqa_interface.protocol import GQQAProtocol

class Pipeline:

    def __init__(self, units):
        self.units = units
        self.first_unit = units[0]
        self.link_units()

    def link_units(self):
        for i, unit in enumerate(i, self.units):
            if i > 0:
                prev_unit.next_unit = unit
            prev_unit = unit

    def start(self, bkd):
        items = bkd.passages
        threads = []

        for unit in reversed(self.units):
            if self.first_unit == unit:
                threads.append(
                    unit.start(items=items, works=len(items))
                )
            else:
                threads.append(
                    unit.start(works=len(items))
                )

        for th in thread:
            th.join()

class PipelineUnit(metaclass=ABCMeta):

    def __init__(self):
        self.queue = None
        self.next_unit = None
        self.th = None
        self.result_queue = deque()

    def start(self, items=None, works=None):
        self.queue = deque(items if itmes is not None else [])
        self.th = threading.Thread(target=self.work, name="", args=(self, works))
        self.th.start()
        return self.th

    def work(self, works):
        while works:
            self.th.wait_for(len(self.queue) > 0)
            
            item = self.queue.popleft()
            result = self.process(item)
            self.result_queue.append(result)
            works = works - 1

            self.next_unit.enqueue(item)

    def enqueue(self, item):
        self.queue.append(item)
        self.th.notify()

    @abstractmethod
    def process(self, item):
        pass


class QGUnit:
    
    def process(self, passage):
        pseudo_bkd = BaseKnowledge(passage)
        RemoteApi.call(QGProtocol(pseudo_bkd))
        return pseudo_bkd.passages[0]

class QAUnit:

    def process(self, passage):
        pseudo_bkd = BaseKnowledge(passage)
        RemoteApi.call(GQQAProtocol(pseudo_bkd))
        return pseudo_bkd.passages[0]
        
