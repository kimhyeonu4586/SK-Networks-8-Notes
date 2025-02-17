from abc import ABC, abstractmethod


class MnistRepository(ABC):

    @abstractmethod
    def loadData(self):
        pass

    @abstractmethod
    def preprocessData(self, X_train, y_train, X_test, y_test):
        pass

    @abstractmethod
    def buildModel(self):
        pass

    @abstractmethod
    def compileModel(self, buildModel):
        pass

    @abstractmethod
    def trainModel(self, buildModel, X_train, y_train):
        pass

    @abstractmethod
    def evaluateModel(self, buildModel, X_test, y_test):
        pass