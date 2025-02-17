from abc import ABC, abstractmethod


class EnsembleMethodRepository(ABC):

    @abstractmethod
    def filterColumns(self, dataFrame, targetColumns):
        pass

    @abstractmethod
    def handleMissingValue(self, dataFrame, targetColumn):
        pass

    @abstractmethod
    def encodeSexLabel(self, dataFrame):
        pass

    @abstractmethod
    def splitTrainTestData(self, dataFrame, whichOneIsYTarget):
        pass

    @abstractmethod
    def createRandomForestClassifier(self):
        pass

    @abstractmethod
    def createGradientBoostClassifier(self):
        pass

    @abstractmethod
    def createVotingModel(self, randomForestModel, gradientBoostModel):
        pass

    @abstractmethod
    def trainModel(self, votingModel, randomForestModel, gradientBoostModel,
                   X_train, y_train):
        pass

    @abstractmethod
    def evaluate(self, votingModel, randomForestModel, gradientBoostModel,
                 X_test):
        pass

    @abstractmethod
    def accuracyTest(self, predictedVotingModel, predictedRandomForestModel,
                     predictedGradientBoostModel, y_test):
        pass