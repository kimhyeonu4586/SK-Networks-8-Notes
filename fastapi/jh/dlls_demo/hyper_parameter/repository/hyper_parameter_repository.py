from abc import ABC, abstractmethod


class HyperParameterRepository(ABC):

    @abstractmethod
    def loadData(self):
        pass

    @abstractmethod
    def splitData(self, data, target):
        pass

    @abstractmethod
    def defineModel(self):
        pass

    @abstractmethod
    def requestHyperParameterGrid(self):
        pass

    @abstractmethod
    def tuningHyperParameter(self, definedModel, hyperParameterGrid, X_train, y_train):
        pass

    @abstractmethod
    def evaluateModel(self, bestModel, X_test, y_test):
        pass