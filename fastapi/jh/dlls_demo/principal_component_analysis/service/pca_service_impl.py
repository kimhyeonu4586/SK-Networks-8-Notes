from principal_component_analysis.repository.pca_repository_impl import PrincipalComponentAnalysisRepositoryImpl
from principal_component_analysis.service.pca_service import PrincipalComponentAnalysisService


class PrincipalComponentAnalysisServiceImpl(PrincipalComponentAnalysisService):

    def __init__(self):
        self.principalComponentAnalysisRepository = PrincipalComponentAnalysisRepositoryImpl()

    def pcaAnalysis(self):
        print("service -> pcaAnalysis()")

        # 샘플 개수 333, 특성 개수 5, 컴포넌트 2의 형태인 PCA 샘플 데이터 추출
        numberOfPoints, numberOfFeatures, numberOfComponents = (
            self.principalComponentAnalysisRepository.createPCASample())

        # 모든 특성에 해당하는 확률 분포 함수의 평균 값을 0으로 맞춤
        mean = self.principalComponentAnalysisRepository.configZeroMean(numberOfFeatures)
        covariance = self.principalComponentAnalysisRepository.configCovariance(numberOfFeatures)

        # 다변량 정규 분포
        createdMultiVariateData = (
            self.principalComponentAnalysisRepository.createMultiVariateNormalDistribution(
                                                            mean, covariance, numberOfPoints))
        print(f"createdMultiVariateData: {createdMultiVariateData}")

        createdDataFrame = self.principalComponentAnalysisRepository.createDataFrame(
                                            createdMultiVariateData, numberOfFeatures)

        pca = self.principalComponentAnalysisRepository.readyForAnalysis(numberOfComponents)
        principalComponentList = self.principalComponentAnalysisRepository.fitTransform(
                                                                    pca, createdDataFrame)
        print(f"principalComponentList: {principalComponentList}")

        originalData = createdDataFrame.values.tolist()
        pcaData = principalComponentList.tolist()
        explainedVarianceRatio = pca.explained_variance_ratio_.tolist()

        return originalData, pcaData, explainedVarianceRatio
