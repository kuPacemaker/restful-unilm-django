from remote import AbstractProtocol
from base import BaseKnowledge

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
            passage.prev_aqset = aqset
            query = ''

            self.questions = list(map(lambda x: x[1], aqset))
            for answer, question in aqset:
                query += self.sep(text, question)
            yield (query + self.TERMINATOR)

    def notify_response(self, response):
        self.bkd.attach_aqset(self.response_attach_head, list(zip(response, self.questions)))
        self.response_attach_head += 1

    def protocol_reset(self):
        self.response_attach_head = 0