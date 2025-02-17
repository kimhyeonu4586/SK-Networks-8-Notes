import matplotlib.pyplot as plt
import pandas as pd

from gradient_descent.repository.gradient_descent_repository_impl import GradientDescentRepositoryImpl
from gradient_descent.service.gradient_descent_service import GradientDescentService


class GradientDescentServiceImpl(GradientDescentService):
    ageGroups = ["20", "30", "40", "50"]
    gameGenre = ["RPG", "FPS", "Simulation", "Adventure", "Puzzle", "Strategy"]

    genrePreferences = {
        "20": [0.4, 0.3, 0.1, 0.1, 0.05, 0.05],
        "30": [0.3, 0.25, 0.2, 0.1, 0.1, 0.05],
        "40": [0.15, 0.2, 0.3, 0.15, 0.1, 0.1],
        "50": [0.1, 0.1, 0.35, 0.2, 0.15, 0.1]
    }

    def __init__(self):
        self.__gradientDescentRepository = GradientDescentRepositoryImpl()

    async def requestProcess(self):
        createdDataFrame = self.__gradientDescentRepository.createDataFrame(
            self.ageGroups, self.gameGenre, self.genrePreferences)

        encoder = self.__gradientDescentRepository.createOneHotEncoder()
        labelEncoder = self.__gradientDescentRepository.createLabelEncoder()

        X_train, X_test, y_train, y_test = (
            self.__gradientDescentRepository.preprocessDataFrame(
                encoder, labelEncoder, createdDataFrame))

        self.__gradientDescentRepository.configModel(0.01, 1000)
        self.__gradientDescentRepository.fitModel(X_train, y_train)
        predictedY = self.__gradientDescentRepository.predictModel(X_test)

        genreLabels = encoder.categories_[0]
        currentWeights = self.__gradientDescentRepository.getWeights()
        weights = pd.DataFrame(currentWeights, index=genreLabels, columns=labelEncoder.classes_)

        print(f"연령대 별 가중치: {weights}")

        topGenrePerAge = weights.apply(lambda x: x.nlargest(3).index.tolist(), axis=0)
        print(f"연령대 별 상위 선호 장르: {topGenrePerAge}")

        plt.figure(figsize=(12, 8))
        for age in labelEncoder.classes_:
            plt.plot(genreLabels, weights[age], label=age)
            
        plt.xlabel("Game Genre")
        plt.ylabel("Preference Score")
        plt.title("Age Group Preference by Game Genre")
        plt.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
