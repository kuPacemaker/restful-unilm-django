from remote import AbstractProtocol
from remote.annotation import terminate
from base import BaseKnowledge

class QAProtocol(AbstractProtocol):
    node = ('117.16.136.170', 3421)

    def __init__(self, bkd: BaseKnowledge, num_case=16, question=None):
        self.bkd = bkd
        self.num_case = num_case
        self.question = question
        self.response_attach_head = 0

    @terminate(AbstractProtocol.TERMINATOR)
    def gen_query(self):
        for i, p in enumerate(self.bkd.all_text()):
            if i % self.num_case == 0:
                if i != 0:
                    yield query
                query = ""

            query += self.sep(p, self.question)
        yield query

    def notify_response(self, response):
        for res in response:
            answer, score = self.detok_score(res)
            self.bkd.attach_aqset(self.response_attach_head, [(answer, self.question, score)])
            self.response_attach_head += 1

    def protocol_reset(self):
        self.response_attach_head = 0