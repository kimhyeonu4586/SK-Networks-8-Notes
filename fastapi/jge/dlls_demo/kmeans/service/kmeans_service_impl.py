import pandas as pd
from matplotlib import pyplot as plt

from kmeans.repository.kmeans_repository_impl import KMeansRepositoryImpl
from kmeans.service.kmeans_service import KMeansService


class KMeansServiceImpl(KMeansService):

    def __init__(self):
        self.__kMeansRepository = KMeansRepositoryImpl()

    async def requestProcess(self):
        createdData = self.__kMeansRepository.createData()
        addOnCreatedData = self.__kMeansRepository.appendAgeGroup20Data(createdData)
        addOnCreatedData = self.__kMeansRepository.appendAgeGroup30Data(addOnCreatedData)
        addOnCreatedData = self.__kMeansRepository.appendAgeGroup40Data(addOnCreatedData)
        addOnCreatedData = self.__kMeansRepository.appendAgeGroup50Data(addOnCreatedData)

        dataFrame = pd.DataFrame(addOnCreatedData)

        X = self.__kMeansRepository.prepareData(dataFrame)
        scaler, scaledX = self.__kMeansRepository.scaleData(X)

        kmeans, dataFrame = self.__kMeansRepository.trainingKMeans(scaledX, dataFrame)

        print(f"클러스터 중심: {kmeans.cluster_centers_}")
        print(f"클러스터 별 데이터 개수: {dataFrame['Cluster'].value_counts()}")

        # matplotlib은 그래프 그리는 것에 특화되어 있음
        # 사실 PlotRepository.createPlot() 이라는 형태로 재사용성을 높이는 것이 더 좋았다 생각함
        # 여차하면 여기서 리턴하고 PlotService.createPlot()으로 구성하는 것도 좋은 방법이라 봄
        # 혹은 MatplotUtility.createPlot() 형태도 나쁘지는 않았을 것임
        plt.figure(figsize=(8, 6))
        # figsize=(8, 6)은 가로 8, 세로 6인 크기로 그래프를 구성
        plt.scatter(X['FPS'], X['RPG'], c=dataFrame['Cluster'], cmap='viridis', alpha=0.5)
        # X축은 FPS, Y축은 RPG를 의미하여 산점도를 그림
        # scatter가 산점도를 그리는 작업
        # 각각의 데이터들을 그룹화해야하므로 dataFrame['Cluster'] 단위로 색상을 일치시킴
        # 앞서 cluster가 4개 존재했기 때문에 4가지 색상이 나오게 됨
        # viridis의 경우 color map을 그라데이션으로 표현함을 의미합니다.
        # 부가적으로 투명도 50%를 설정해서 산점도의 점들이 겹치는 경우에도 어느 정도 보이도록 구성
        centroids = kmeans.cluster_centers_
        # 클러스터 중심값 4개
        centroids_unscaled = scaler.inverse_transform(centroids)
        # 클러스터 중심을 원래 데이터 스케일로 표현
        # 앞서 scaledX로 0.0 ~ 1.0 사이로 스케일 되었기 때문

        plt.scatter(
            centroids_unscaled[:, 0], centroids_unscaled[:, 1],
            c='red', marker='x', s=200, label='Centroids'
        )
        # 클러스터 중심의 FPS와 RPG 값을 각각 가져옴
        # 중심은 빨간색, marker는 x 표시, 마커의 크기가 s=200,
        # 레이블을 추가하여 x 마커가 centroids 임을 표기
        plt.title("FPS와 RPG기반 K-means 클러스터링")
        plt.xlabel("FPS")
        plt.ylabel("RPG")
        plt.legend()
        plt.show()

