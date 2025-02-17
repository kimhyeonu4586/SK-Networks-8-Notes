import pandas as pd

from feature_engineering.repository.feature_engineering_repository_impl import FeatureEngineeringRepositoryImpl
from feature_engineering.service.feature_engineering_service import FeatureEngineeringService


class FeatureEngineeringServiceImpl(FeatureEngineeringService):
    __houseData = {
        'date': ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01'],
        'size': [2000, 1500, 1800, 2200, 1600],
        'numberOfRooms': [4, 3, 3, 5, 3],
        'age': [10, 15, 12, 5, 20],
        'price': [500000, 450000, 480000, 600000, 430000]
    }

    def __init__(self):
        self.__featureEngineeringRepository = FeatureEngineeringRepositoryImpl()

    async def featureEngineering(self):
        # pandas를 사용해서 데이터 프레임화(엑셀화)
        dataFrame = pd.DataFrame(self.__houseData)
        # 불 필요한 정보들 제거
        cleanedDataFrame = self.__featureEngineeringRepository.removeUselessInformation(dataFrame)
        # 결측치 제거
        # 값이 없거나 누락 되었거나 잘못된 값이 적혀 있는 경우
        handledDataFrame = self.__featureEngineeringRepository.handleMissingValues(cleanedDataFrame)
        # 훈련(학습) / 테스트(검증) 데이터를 분리
        X_train, X_test, y_train, y_test = (
            self.__featureEngineeringRepository.splitTrainTestData(handledDataFrame))
        # 훈련 데이터를 가지고 실제 학습 진행
        # y = ax + b
        # y = ax^2 + bx + c
        # y = ae^bx + c
        # Fourier Integral(푸리에 적분) 기반인데 이것은 어차피 라이브러리가 알아서 해줌
        featureEngineeringModel = self.__featureEngineeringRepository.trainModel(X_train, y_train)
        # 검증 데이터를 가지고 오차와 예측값을 뽑음
        mseError, y_prediction = self.__featureEngineeringRepository.evaluateModel(
            featureEngineeringModel, X_test, y_test)
        print(f"mseError: {mseError}, y_prediction: {y_prediction}")

        # 실제 검증용 데이터와 예측 데이터를 엑셀화
        comparison = self.__featureEngineeringRepository.compareResult(y_test, y_prediction)
        return {
            "mseError": mseError,
            "comparison": comparison
        }
