from remote.protocol import AbstractProtocol
from base.models import BaseKnowledge

class QAProtocol(AbstractProtocol):
    node = ('117.16.136.170', 3421)

    def __init__(self, bkd: BaseKnowledge, num_case=16, question=None):
        self.bkd = bkd
        self.num_case = num_case
        self.question = question
        self.response_attach_head = 0

    def gen_query(self):
        for i, p in enumerate(self.bkd.all_text()):
            if i % self.num_case == 0:
                if i != 0:
                    yield (query + self.TERMINATOR)
                query = ""

            query += self.sep(p, self.question)

        yield (query + self.TERMINATOR)

    def notify_response(self, response):
        for res in response:
            self.bkd.attach_aqset(self.response_attach_head, [(res, self.question)])
            self.response_attach_head += 1

    def protocol_reset(self):
        self.response_attach_head = 0

class GQQAProtocol(AbstractProtocol):
    node = ('117.16.136.170', 3421)

    def __init__(self, bkd: BaseKnowledge):
        self.bkd = bkd
        self.questions = None
        self.response_attach_head = 0

    def gen_query(self):
        for passage in self.bkd.passages:
            text = passage.text
            aqset = passage.aqset
            query = ''
            self.questions = list(map(lambda x: x[0], aqset))
            for answer, question in aqset:
                query += self.sep(text, question)
            yield (query + self.TERMINATOR)

    def notify_response(self, response):
        self.bkd.attach_aqset(self.response_attach_head, list(zip(response, self.questions)))
        self.response_attach_head += 1

    def protocol_reset(self):
        self.response_attach_head = 0