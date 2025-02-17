from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from ensemble_method.repository.ensemble_method_repository import EnsembleMethodRepository


class EnsembleMethodRepositoryImpl(EnsembleMethodRepository):

    def filterColumns(self, dataFrame, targetColumns):
        return dataFrame[targetColumns]

    def handleMissingValue(self, dataFrame, targetColumn):
        dataFrame[targetColumn] = (
            dataFrame[targetColumn].fillna(dataFrame[targetColumn].median()))

        return dataFrame

    def encodeSexLabel(self, dataFrame):
        encoder = LabelEncoder()
        dataFrame["Sex"] = encoder.fit_transform(dataFrame["Sex"])

        return dataFrame

    def splitTrainTestData(self, dataFrame, whichOneIsYTarget):
        X = dataFrame.drop(whichOneIsYTarget, axis=1)
        y = dataFrame[whichOneIsYTarget]

        return train_test_split(X, y, test_size=0.2, random_state=42)

    def createRandomForestClassifier(self):
        return RandomForestClassifier(n_estimators=100, random_state=42)

    def createGradientBoostClassifier(self):
        return GradientBoostingClassifier(n_estimators=100, random_state=42)

    def createVotingModel(self, randomForestModel, gradientBoostModel):
        return VotingClassifier(
            estimators=[
                ('rf', randomForestModel),
                ('gb', gradientBoostModel)
            ],
            voting='hard'
            # hard는 다수결, soft는 평균 확률
        )

    def trainModel(self, votingModel, randomForestModel, gradientBoostModel,
                   X_train, y_train):

        randomForestModel.fit(X_train, y_train)
        gradientBoostModel.fit(X_train, y_train)
        votingModel.fit(X_train, y_train)

        return votingModel, randomForestModel, gradientBoostModel

    def evaluate(self, votingModel, randomForestModel, gradientBoostModel,
                 X_test):

        randomForestPrediction = randomForestModel.predict(X_test)
        gradientBoostPrediction = gradientBoostModel.predict(X_test)
        votingPrediction = votingModel.predict(X_test)

        return votingPrediction, randomForestPrediction, gradientBoostPrediction

    def accuracyTest(self, predictedVotingModel, predictedRandomForestModel,
                     predictedGradientBoostModel, y_test):

        return {
            "RandomForest Accuracy": accuracy_score(y_test, predictedRandomForestModel),
            "GradientBoost Accuracy": accuracy_score(y_test, predictedGradientBoostModel),
            "Voting Accuracy": accuracy_score(y_test, predictedVotingModel)
        }

