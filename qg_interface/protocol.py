from remote import AbstractRest
from base import BaseKnowledge

class QGProtocol(AbstractRest):
    node = ('http://117.16.137.22', 5000, '/qg')

    def __init__(self, bkd: BaseKnowledge, num_case=None):
        self.bkd = bkd
        self.num_case = num_case if num_case is not None else bkd.prune_nouns_amount()
        self.answers = None
        self.response_attach_head = 0

    def gen_payload(self):
        for passage in self.bkd.passages:
            query = {"messages": []}
            context = passage.text
            self.answers = passage.nouns[:min(len(passage.nouns), self.num_case)]
            for answer in self.answers:
                query["messages"].append(f"answer: {answer} context: {context}")
            print(query)
            yield query

    def notify_response(self, response):
        responses = response.json()["responses"]
        questions = [generated["generated"] for generated in responses]
        self.bkd.attach_aqset(self.response_attach_head, list(zip(self.answers, questions)))
        self.response_attach_head += 1

    def protocol_reset(self):
        self.response_attach_head = 0
