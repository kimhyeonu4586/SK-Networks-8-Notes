from abc import ABC, abstractmethod


class KMeansRepository(ABC):

    @abstractmethod
    def createData(self):
        pass

    @abstractmethod
    def appendAgeGroup20Data(self, data):
        pass

    @abstractmethod
    def appendAgeGroup30Data(self, data):
        pass

    @abstractmethod
    def appendAgeGroup40Data(self, data):
        pass

    @abstractmethod
    def appendAgeGroup50Data(self, data):
        pass

    @abstractmethod
    def prepareData(self, dataFrame):
        pass

    @abstractmethod
    def scaleData(self, data):
        pass

    @abstractmethod
    def trainingKMeans(self, scaledX, dataFrame):
        pass
