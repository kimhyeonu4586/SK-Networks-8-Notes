from abc import ABC, abstractmethod


class ModelRegulationService(ABC):

    @abstractmethod
    def requestProcess(self):
        pass
