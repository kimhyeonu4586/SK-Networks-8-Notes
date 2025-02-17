from abc import ABC, abstractmethod


class GradientDescentRepository(ABC):

    @abstractmethod
    def createDataFrame(self, ageGroups, gameGenre, genrePreferences):
        pass

    @abstractmethod
    def createOneHotEncoder(self):
        pass

    @abstractmethod
    def createLabelEncoder(self):
        pass

    @abstractmethod
    def preprocessDataFrame(self, encoder, labelEncoder, dataFrame):
        pass

    @abstractmethod
    def configModel(self, learningRate, maxIteration):
        pass

    @abstractmethod
    def fitModel(self, X_train, y_train):
        pass

    @abstractmethod
    def predictModel(self, X_test):
        pass
