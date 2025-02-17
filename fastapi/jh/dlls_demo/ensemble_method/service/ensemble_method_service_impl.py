import pandas as pd

from ensemble_method.repository.ensemble_method_repository_impl import EnsembleMethodRepositoryImpl
from ensemble_method.service.ensemble_method_service import EnsembleMethodService


class EnsembleMethodServiceImpl(EnsembleMethodService):
    TITANIC_DATA_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    TARGET_COLUMNS = ["Survived", "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]
    MISSING_VALUES_COLUMN = "Age"
    WHICH_ONE_IS_Y_TARGET = "Survived"

    def __init__(self):
        self.__ensembleMethodRepository = EnsembleMethodRepositoryImpl()

    def __loadTitanicData(self):
        return pd.read_csv(self.TITANIC_DATA_URL)

    async def ensembleMethod(self):
        # 타이타닉 데이터를 로드
        loadedTitanicDataFrame = self.__loadTitanicData()
        # 로드한 데이터 중
        # "Survived", "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"에 해당하는 컬럼들만 추출
        preProcessedDataFrame = self.__ensembleMethodRepository.filterColumns(
            loadedTitanicDataFrame, self.TARGET_COLUMNS)
        # 내용을 보면 Age 값이 누락되어 있는 경우가 존재함
        # 이런 경우 결측치들을 중앙값(median)으로 처리
        # 숫자들이 쭉 열거 되어 있을 때 실제로 정말 가운데 있는 값을 의미함
        # 1, 3, 11, 13, 15인 경우 11
        handledMissingValueDataFrame = self.__ensembleMethodRepository.handleMissingValue(
            preProcessedDataFrame, self.MISSING_VALUES_COLUMN)
        # 성별에 대한 레이블을 처리함
        # 컴퓨터는 숫자만 처리 할 수 있기 때문에 남성, 여성에 대한 정보를 0, 1로 엔코딩
        encodedSexDataFrame = self.__ensembleMethodRepository.encodeSexLabel(
            handledMissingValueDataFrame)
        # 엔코딩 데이터 중 y(생존 여부)를 추론 할 수 있는 훈련 집합과 검증 집합을 분류함
        X_train, X_test, y_train, y_test = (
            self.__ensembleMethodRepository.splitTrainTestData(
                encodedSexDataFrame, self.WHICH_ONE_IS_Y_TARGET))
        # 추론 모델로 Random Forest와 Graident Boost를 선택
        randomForestModel = self.__ensembleMethodRepository.createRandomForestClassifier()
        gradientBoostModel = self.__ensembleMethodRepository.createGradientBoostClassifier()
        # 둘 중 누가 더 좋을지 투표 형식으로 선택하는 Voting Model 구성
        votingModel = self.__ensembleMethodRepository.createVotingModel(
            randomForestModel, gradientBoostModel)
        # 실제 각각의 모델들을 훈련시킴
        trainedVotingModel, trainedRandomForestModel, trainedGradientBoostModel =(
            self.__ensembleMethodRepository.trainModel(
                votingModel, randomForestModel, gradientBoostModel,
                X_train, y_train))
        # 훈련된 모델로 추론을 진행해서 예측치를 뽑음
        predictedVotingModel, predictedRandomForestModel, predictedGradientBoostModel = (
            self.__ensembleMethodRepository.evaluate(
                trainedVotingModel, trainedRandomForestModel, trainedGradientBoostModel,
                X_test))
        # 예측치와 실제 검증 데이터가 얼마나 일치하는지 정확도를 판정
        return self.__ensembleMethodRepository.accuracyTest(
            predictedVotingModel, predictedRandomForestModel, predictedGradientBoostModel,
            y_test)
