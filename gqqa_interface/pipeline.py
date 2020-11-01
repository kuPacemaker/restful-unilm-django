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
                    unit.start(inputs=inputs, n_works=len(inputs))
                )
            else:
                threads.append(
                    unit.start(n_works=len(inputs))
                )

        for th in threads:
            th.join()

        return self.last_unit.result_queue

class PipelineUnit:

    def __init__(self):
        self.queue = None
        self.result_queue = None
        self.next_unit = None
        self.th = None

    def start(self, inputs=None, n_works=None):
        self.queue = deque(inputs if inputs else [])
        self.result_queue = []
        self.th = threading.Thread(target=self.run, name="", args=(n_works, ))
        self.th.start()
        return self.th

    def run(self, n_works):
        while n_works:
            waiting.wait(lambda: len(self.queue) > 0)

            input = self.queue.popleft()
            result = self.process(input)
            
            if self.next_unit:
                self.next_unit.enqueue(result)
            else:
                self.result_queue.append(result)

            n_works = n_works - 1

    def enqueue(self, input):
        self.queue.append(input)

    def process(self, input):
        raise NotImplementedError


class QGUnit(PipelineUnit):

    def process(self, input):
        passage = input
        pseudo_bkd = BaseKnowledge(passage.text)
        pseudo_bkd.passages = [passage]
        RemoteApi.call(QGProtocol(pseudo_bkd, num_case=3))
        return pseudo_bkd

class QAUnit(PipelineUnit):

    def process(self, input):
        pseudo_bkd = input
        RemoteApi.call(GQQAProtocol(pseudo_bkd))
        return pseudo_bkd.passages[0]
        
