from remote import AbstractProtocol
from base import BaseKnowledge

class QGProtocol(AbstractProtocol):
    node = ('117.16.136.171', 2593)

    def __init__(self, bkd: BaseKnowledge, num_case=3):
        self.bkd = bkd
        self.num_case = num_case if num_case is not None else 3 + int(3/len(self.bkd.passages))
        self.answers = None
        self.response_attach_head = 0

    def gen_query(self):
        for passage in self.bkd.passages:
            query = ""
            p = passage.text
            self.answers = passage.nouns[:min(len(passage.nouns), self.num_case)]

            for a in self.answers:
                query += self.sep(p, a)

            yield (query + self.TERMINATOR)

    def notify_response(self, response):
        self.bkd.attach_aqset(self.response_attach_head, list(zip(self.answers, response)))
        self.response_attach_head += 1

    def protocol_reset(self):
        self.response_attach_head = 0
