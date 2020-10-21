from remote.protocol import AbstractProtocol

class QAProtocol(AbstractProtocol):
    node = ('117.16.136.170', 3421)

    def gen_query(self, bkd, question):
        query = ''
        for passage in bkd.passages:
            text = passage.text
            query += sep(text, question)
        return query + self.TERMINATOR
