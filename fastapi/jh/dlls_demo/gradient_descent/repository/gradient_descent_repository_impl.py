import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from gradient_descent.repository.gradient_descent_repository import GradientDescentRepository


class GradientDescentRepositoryImpl(GradientDescentRepository):
    PURCHASES = 1000

    def createDataFrame(self, ageGroups, gameGenre, genrePreferences):
        data = []

        for ageGroup in ageGroups:
            genres = np.random.choice(gameGenre, size=self.PURCHASES, p=genrePreferences[ageGroup])

            for genre in genres:
                data.append({
                    "ageGroup": ageGroup,
                    "gameGenre": genre
                })

        return pd.DataFrame(data)

    def createOneHotEncoder(self):
        return OneHotEncoder(sparse_output=False)

    def createLabelEncoder(self):
        return LabelEncoder()

    def preprocessDataFrame(self, encoder, labelEncoder, dataFrame):
        X = encoder.fit_transform(dataFrame[["gameGenre"]])
        y = labelEncoder.fit_transform(dataFrame[["ageGroup"]])

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def configModel(self, learningRate, maxIteration):
        self.learningRate = learningRate
        self.maxIteration = maxIteration
        self.weights = None
        self.bias = None

    def __softmax(self, modelRepresentation):
        expRepresentation = np.exp(modelRepresentation - np.max(modelRepresentation, axis=1, keepdims=True))
        return expRepresentation / np.sum(expRepresentation, axis=1, keepdims=True)

    def fitModel(self, X_train, y_train):
        numberOfSamples, numberOfFeatures = X_train.shape
        numberOfClasses = len(np.unique(y_train))

        self.weights = np.zeros((numberOfFeatures, numberOfClasses))
        self.bias = np.zeros(numberOfClasses)

        yOneHotEncode = np.eye(numberOfClasses)[y_train]

        for _ in range(self.maxIteration):
            # y = ax + b
            linearModel = np.dot(X_train, self.weights) + self.bias
            yPrediction = self.__softmax(linearModel)

            dw = (1 / numberOfSamples) * np.dot(X_train.T, (yPrediction - yOneHotEncode))
            db = (1 / numberOfSamples) * np.sum(yPrediction - yOneHotEncode, axis=0)

            self.weights -= self.learningRate * dw
            self.bias -= self.learningRate * db

    def predictModel(self, X_test):
        linearModel = np.dot(X_test, self.weights) + self.bias
        yPrediction = self.__softmax(linearModel)

        return np.argmax(yPrediction, axis=1)

    def getWeights(self):
        return self.weights