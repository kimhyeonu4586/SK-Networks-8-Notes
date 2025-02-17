from abc import ABC, abstractmethod


class GradientDescentService(ABC):

    @abstractmethod
    def requestProcess(self):
        pass
