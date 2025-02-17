import pandas as pd
from skimage.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from feature_engineering.repository.feature_engineering_repository import FeatureEngineeringRepository


class FeatureEngineeringRepositoryImpl(FeatureEngineeringRepository):

    def removeUselessInformation(self, dataFrame):
        dataFrame['date'] = pd.to_datetime(dataFrame['date'])
        dataFrame['year'] = dataFrame['date'].dt.year
        dataFrame['month'] = dataFrame['date'].dt.month

        cleanedDataFrame = dataFrame.drop(columns=['date'])

        return cleanedDataFrame

    def handleMissingValues(self, dataFrame):
        return dataFrame.fillna(dataFrame.mean())

    def splitTrainTestData(self, dataFrame):
        X = dataFrame.drop(columns=['price'])
        y = dataFrame['price']
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def trainModel(self, X_train, y_train):
        model = LinearRegression()
        model.fit(X_train, y_train)
        return model

    def evaluateModel(self, model, X_test, y_test):
        y_prediction = model.predict(X_test)
        mseError = mean_squared_error(y_test, y_prediction)
        return mseError, y_prediction

    def compareResult(self, y_test, y_prediction):
        return pd.DataFrame({'Actual': y_test, 'Predicted': y_prediction})
