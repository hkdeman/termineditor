from abc import ABCMeta, abstractmethod

class Navigator:
    __metaclass__ = ABCMeta

    @abstractmethod
    def up(self): raise NotImplementedError

    @abstractmethod
    def down(self): raise NotImplementedError

    @abstractmethod
    def left(self): raise NotImplementedError

    @abstractmethod
    def right(self): raise NotImplementedError

    @abstractmethod
    def display(self): raise NotImplementedError

    @abstractmethod
    def run(self): raise NotImplementedError