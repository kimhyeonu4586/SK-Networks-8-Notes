from abc import ABC, abstractmethod


class FeatureEngineeringRepository(ABC):

    @abstractmethod
    def removeUselessInformation(self, dataFrame):
        pass

    @abstractmethod
    def handleMissingValues(self, dataFrame):
        pass

    @abstractmethod
    def splitTrainTestData(self, dataFrame):
        pass

    @abstractmethod
    def trainModel(self, X_train, y_train):
        pass

    @abstractmethod
    def evaluateModel(self, model, X_test, y_test):
        pass

    @abstractmethod
    def compareResult(self, y_test, y_prediction):
        pass
