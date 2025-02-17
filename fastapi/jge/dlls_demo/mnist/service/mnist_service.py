from abc import ABC, abstractmethod


class MnistService(ABC):

    @abstractmethod
    def requestProcess(self):
        pass
