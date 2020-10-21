from abc import ABCMeta, abstractmethod

class AbstractProtocol(metaclass=ABCMeta):

    TIMEOUT = 15.0

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'node'):
            raise NotImplementedError('Protocol needs the target node info: tuple of (HOST, PORT)')
        return object.__new__(cls)

    @abstractmethod
    def gen_query(self):
        pass

    def sep(self, str1, str2):
        return "%s [SEP] %s\n" % (str1, str2)
