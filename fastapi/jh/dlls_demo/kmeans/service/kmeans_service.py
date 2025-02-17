from abc import ABC, abstractmethod


class KMeansService(ABC):

    @abstractmethod
    def requestProcess(self):
        pass
