from collections import deque
import threading, waiting

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
        inputs = bkd.passages
        threads = []

        for unit in reversed(self.units):
            if self.first_unit == unit:
                threads.append(
                    unit.start(unit, inputs=inputs, works=len(inputs))
                )
            else:
                threads.append(
                    unit.start(unit, works=len(inputs))
                )

        for th in threads:
            th.join()

        return list(self.last_unit.result_queue)

class PipelineUnit:

    def start(self, inputs=None, works=None):
        self.queue = deque(inputs if inputs is not None else [])
        self.result_queue = deque()
        self.th = threading.Thread(target=self.work, name="", args=(self, works))
        self.th.start()
        return self.th

    def work(self, works):
        while works:
            waiting.wait(lambda: len(self.queue) > 0)
            input = self.queue.popleft()
            result = self.process(self, input)
            self.result_queue.append(result)
            if hasattr(self, 'next_unit'):
                self.enqueue(self.next_unit, result)
            works = works - 1

    def enqueue(self, input):
        self.queue.append(input)

    def process(self, input):
        raise NotImplementedError


class QGUnit(PipelineUnit):

    def process(self, input):
        passage = input
        pseudo_bkd = BaseKnowledge(passage.text)
        RemoteApi.call(QGProtocol(pseudo_bkd, num_case=3))
        return pseudo_bkd

class QAUnit(PipelineUnit):

    def process(self, input):
        pseudo_bkd = input
        RemoteApi.call(GQQAProtocol(pseudo_bkd))
        return pseudo_bkd.passages[0]
        
