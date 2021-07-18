from abc import ABCMeta, abstractmethod

class AbstractRest(metaclass=ABCMeta):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'node'):
            raise NotImplementedError('Rest needs the target resource\'s info: tuple of (HOST, PORT, RESOURCE)')
        return object.__new__(cls)

    @abstractmethod
    def gen_payload(self):
        pass

    @abstractmethod
    def notify_response(self, response):
        pass

    def base_url(self):
        return f'{self.node[0]}:{self.node[1]}{self.node[2]}'
