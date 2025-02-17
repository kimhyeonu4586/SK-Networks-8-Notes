from abc import ABC, abstractmethod


class ModelRegulationRepository(ABC):

    @abstractmethod
    def loadData(self):
        pass

    @abstractmethod
    def preprocessData(self, x, y, numClasses):
        pass

    @abstractmethod
    def buildModel(self, inputShape, numClasses):
        pass

    @abstractmethod
    def compileModel(self, model):
        pass

    @abstractmethod
    def trainModel(self, buildModel, X_train, y_train):
        pass

    @abstractmethod
    def evaluateModel(self, buildModel, X_test, y_test):
        pass
