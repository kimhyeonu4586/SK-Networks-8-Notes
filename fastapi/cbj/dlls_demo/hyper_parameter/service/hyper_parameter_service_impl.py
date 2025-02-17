from hyper_parameter.repository.hyper_parameter_repository_impl import HyperParameterRepositoryImpl
from hyper_parameter.service.hyper_parameter_service import HyperParameterService


class HyperParameterServiceImpl(HyperParameterService):

    def __init__(self):
        self.__hyperParameterRepository = HyperParameterRepositoryImpl()

    async def requestProcess(self):
        data, target = self.__hyperParameterRepository.loadData()
        X_train, X_test, y_train, y_test = self.__hyperParameterRepository.splitData(data, target)
        print(f"================ START ================")
        print(f"X_train: {X_train}, y_train: {y_train}, X_test: {X_test}, y_test: {y_test}")
        print(f"X_train shape: {X_train.shape}")
        print(f"y_train shape: {len(y_train)}")
        print(f"================= END =================")

        definedModel = self.__hyperParameterRepository.defineModel()
        print(f"================ START ================")
        print(f"definedModel: {definedModel}")
        print(f"================= END =================")

        hyperParameterGrid = self.__hyperParameterRepository.requestHyperParameterGrid()
        print(f"================ START ================")
        print(f"hyperParameterGrid: {hyperParameterGrid}")
        print(f"================= END =================")

        gridSearch = self.__hyperParameterRepository.tuningHyperParameter(
            definedModel, hyperParameterGrid, X_train, y_train)
        print(f"================ START ================")
        print(f"최적의 하이퍼 파라미터: {gridSearch.best_params_}")
        print(f"최적의 교차 검증 점수: {gridSearch.best_score_}")
        print(f"================= END =================")

        bestModel = gridSearch.best_estimator_
        testAccuracy = self.__hyperParameterRepository.evaluateModel(bestModel, X_test, y_test)
        print(f"테스트 데이터 정확도:", testAccuracy)
