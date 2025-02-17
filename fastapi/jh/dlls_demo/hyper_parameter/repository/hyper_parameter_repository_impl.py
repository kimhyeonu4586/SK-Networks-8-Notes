from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV

from hyper_parameter.repository.hyper_parameter_repository import HyperParameterRepository


class HyperParameterRepositoryImpl(HyperParameterRepository):

    def loadData(self):
        data = load_iris()
        print(f"data: {data}")
        return data.data, data.target

    def splitData(self, dataX, targetY):
        return train_test_split(dataX, targetY, test_size=0.2, random_state=42)

    def defineModel(self):
        return RandomForestClassifier(random_state=42)

    def requestHyperParameterGrid(self):
        return {
            'n_estimators': [50, 100, 150],  # 트리의 개수
            'max_depth': [None, 10, 20, 30], # 최대 깊이
            'min_samples_split': [2, 5, 10], # 노드를 나누는 최소 샘플 수
            'min_samples_leaf': [1, 2, 4],   # 트리는 양 갈래로 나눠지고 마지막에 잎사귀가 있음 (잎사귀 최소 개수)
        }

    def tuningHyperParameter(self, definedModel, hyperParameterGrid, X_train, y_train):
        gridSearch = GridSearchCV(estimator=definedModel, param_grid=hyperParameterGrid,
                                  cv=5, scoring='accuracy', n_jobs=-1)
        gridSearch.fit(X_train, y_train)

        return gridSearch

    def evaluateModel(self, bestModel, X_test, y_test):
        yPrediction = bestModel.predict(X_test)

        return accuracy_score(y_test, yPrediction)
