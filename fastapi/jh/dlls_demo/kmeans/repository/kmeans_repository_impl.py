import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from kmeans.repository.kmeans_repository import KMeansRepository


class KMeansRepositoryImpl(KMeansRepository):
    SAMPLE_COUNT = 100

    def createData(self):
        return {
            'AgeGroup': [],
            'FPS': [],
            'RPG': [],
            'Sports': [],
            'Puzzle': [],
            'MOBA': [],
            'Simulation': []
        }

    # 무엇을 만들던 0 ~ 10 사이의 정규 분포를 만들게 됨 (이상치는 존재함 범주를 벗어나는)
    def __generateDataDistribution(self, base, variation, size):
        return np.clip(np.random.normal(base, variation, size), 0, 10)

    def appendAgeGroup20Data(self, data):
        for _ in range(self.SAMPLE_COUNT):
            data['AgeGroup'].append('20s')
            data['FPS'].append(self.__generateDataDistribution(8, 1.5, 1)[0])
            data['RPG'].append(self.__generateDataDistribution(7, 2, 1)[0])
            data['Sports'].append(self.__generateDataDistribution(6, 1, 1)[0])
            data['Puzzle'].append(self.__generateDataDistribution(4, 2, 1)[0])
            data['MOBA'].append(self.__generateDataDistribution(9, 1.5, 1)[0])
            data['Simulation'].append(self.__generateDataDistribution(5, 2, 1)[0])

        return data

    def appendAgeGroup30Data(self, data):
        for _ in range(self.SAMPLE_COUNT):
            data['AgeGroup'].append('30s')
            data['FPS'].append(self.__generateDataDistribution(7, 2, 1)[0])
            data['RPG'].append(self.__generateDataDistribution(8, 1.5, 1)[0])
            data['Sports'].append(self.__generateDataDistribution(5, 2, 1)[0])
            data['Puzzle'].append(self.__generateDataDistribution(6, 1.5, 1)[0])
            data['MOBA'].append(self.__generateDataDistribution(7, 1, 1)[0])
            data['Simulation'].append(self.__generateDataDistribution(6, 2, 1)[0])

        return data

    def appendAgeGroup40Data(self, data):
        for _ in range(self.SAMPLE_COUNT):
            data['AgeGroup'].append('40s')
            data['FPS'].append(self.__generateDataDistribution(5, 2, 1)[0])
            data['RPG'].append(self.__generateDataDistribution(6, 2, 1)[0])
            data['Sports'].append(self.__generateDataDistribution(7, 1, 1)[0])
            data['Puzzle'].append(self.__generateDataDistribution(8, 1.5, 1)[0])
            data['MOBA'].append(self.__generateDataDistribution(4, 1, 1)[0])
            data['Simulation'].append(self.__generateDataDistribution(8, 1.5, 1)[0])

        return data

    def appendAgeGroup50Data(self, data):
        for _ in range(self.SAMPLE_COUNT):
            data['AgeGroup'].append('50s')
            data['FPS'].append(self.__generateDataDistribution(3, 1.5, 1)[0])
            data['RPG'].append(self.__generateDataDistribution(5, 2, 1)[0])
            data['Sports'].append(self.__generateDataDistribution(8, 1, 1)[0])
            data['Puzzle'].append(self.__generateDataDistribution(9, 1.5, 1)[0])
            data['MOBA'].append(self.__generateDataDistribution(2, 1, 1)[0])
            data['Simulation'].append(self.__generateDataDistribution(9, 1, 1)[0])

        return data

    def prepareData(self, dataFrame):
        return dataFrame[['FPS', 'RPG', 'Sports', 'Puzzle', 'MOBA', 'Simulation']]

    def scaleData(self, data):
        scaler = StandardScaler()
        scaledX = scaler.fit_transform(data)

        return scaler, scaledX

    def trainingKMeans(self, scaledX, dataFrame):
        kmeans = KMeans(n_clusters=4, random_state=42)
        dataFrame['Cluster'] = kmeans.fit_predict(scaledX)

        return kmeans, dataFrame
    