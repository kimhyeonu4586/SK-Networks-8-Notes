from abc import ABC, abstractmethod


class HyperParameterService(ABC):

    @abstractmethod
    def requestProcess(self):
        pass
