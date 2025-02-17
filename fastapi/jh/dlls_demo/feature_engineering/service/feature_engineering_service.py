from abc import ABC, abstractmethod


class FeatureEngineeringService(ABC):

    @abstractmethod
    def featureEngineering(self):
        pass
