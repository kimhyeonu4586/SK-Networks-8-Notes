from abc import ABC, abstractmethod

import pandas as pd


class GameSoftwareAnalysisRepository(ABC):

    @abstractmethod
    def loadDataFromFile(self, filePath: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def analyzeAgeGroupData(self, data: pd.DataFrame):
        pass
