from abc import ABCMeta, abstractmethod
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
        self.last_unit = units[-1]
        self.link_units()

    def link_units(self):
        for i, unit in enumerate(self.units):
            if i > 0:
                prev_unit.next_unit = unit
            prev_unit = unit

    def start(self, bkd):
        items = bkd.passages
        threads = []

        for unit in reversed(self.units):
            if self.first_unit == unit:
                threads.append(
                    unit.start(unit, items=items, works=len(items))
                )
            else:
                threads.append(
                    unit.start(unit, works=len(items))
                )

        for th in threads:
            th.join()

        return self.last_unit.result_queue

class PipelineUnit(metaclass=ABCMeta):

    def __init__(self):
        self.queue = None
        self.next_unit = None
        self.th = None
        self.result_queue = None
        self.condition = None

    def start(self, items=None, works=None):
        self.queue = deque(items if items is not None else [])
        self.result_queue = deque()
        self.condition = threading.Condition()
        self.th = threading.Thread(target=self.work, name="", args=(self, works))
        self.th.start()
        return self.th

    def work(self, works):
        while works:
            self.condition.acquire()
            self.condition.wait_for(lambda : len(self.queue) > 0)
            item = self.queue.popleft()
            result = self.process(self, item)

            self.result_queue.append(result)
            self.next_unit.enqueue(self.next_unit, item)
            works = works - 1

    def enqueue(self, item):
        self.queue.append(item)
        self.condition.notify()
        self.condition.release()

    @abstractmethod
    def process(self, item):
        pass


class QGUnit(PipelineUnit):

    def process(self, passage):
        pseudo_bkd = BaseKnowledge(passage.text)
        RemoteApi.call(QGProtocol(pseudo_bkd))
        return pseudo_bkd.passages[0]

class QAUnit(PipelineUnit):

    def process(self, passage):
        pseudo_bkd = BaseKnowledge(passage.text)
        RemoteApi.call(GQQAProtocol(pseudo_bkd))
        return pseudo_bkd.passages[0]
        
