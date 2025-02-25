from abc import ABC, abstractmethod


class GameSoftwareAnalysisService(ABC):

    @abstractmethod
    def requestAnalysis(self, filePath: str):
        pass
