from remote.protocol import AbstractProtocol

class QGProtocol(AbstractProtocol):
    node = ('117.16.136.171', 2593)

    def gen_query(self, bkd, num_query=6):
        for passage in bkd.passages:
            query = ''
            text = passage.text
            for noun in passage.nouns[:num_query]:
                query += sep(text, noun)
        return query + self.TERMINATOR
