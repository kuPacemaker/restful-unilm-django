from abc import ABCMeta, abstractmethod

class AbstractProtocol(metaclass=ABCMeta):

    TIMEOUT = 25.0
    TERMINATOR = '*'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'node'):
            raise NotImplementedError('Protocol needs the target node\'s info: tuple of (HOST, PORT)')
        return object.__new__(cls)

    @abstractmethod
    def gen_query(self):
        pass

    @abstractmethod
    def notify_response(self, response):
        pass

    def parse(self):
        return self.node[0], self.node[1], self.gen_query(), self.TIMEOUT

    @classmethod
    def sep(cls, str1, str2):
        return "%s [SEP] %s\n" % (str1, str2)

    @classmethod
    def detok_score(cls, res):
        detok = [s.strip() for s in res.split(' [SCO] ')]
        return detok[0], float(detok[1])