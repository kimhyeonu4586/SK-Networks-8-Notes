from model_regulation.repository.model_regulation_repository_impl import ModelRegulationRepositoryImpl
from model_regulation.service.model_regulation_service import ModelRegulationService


class ModelRegulationServiceImpl(ModelRegulationService):

    NUMBER_OF_MNIST_CLASSES = 10

    def __init__(self):
        self.__modelRegulationRepository = ModelRegulationRepositoryImpl()

    async def requestProcess(self):
        # loadData에서 리턴 할 때 아래와 같은 형태로 리턴 되기 때문에 주의 필요함
        (X_train, y_train), (X_test, y_test) = self.__modelRegulationRepository.loadData()
        preProcessedTrainX, preProcessedTrainY = self.__modelRegulationRepository.preprocessData(
            X_train, y_train, self.NUMBER_OF_MNIST_CLASSES)
        preProcessedTestX, preProcessedTestY = self.__modelRegulationRepository.preprocessData(
            X_test, y_test, self.NUMBER_OF_MNIST_CLASSES)

        model = self.__modelRegulationRepository.buildModel((28 * 28,), self.NUMBER_OF_MNIST_CLASSES)
        self.__modelRegulationRepository.compileModel(model)
        self.__modelRegulationRepository.trainModel(model, preProcessedTrainX, preProcessedTrainY)
        loss, accuracy = self.__modelRegulationRepository.evaluateModel(model, preProcessedTestX, preProcessedTestY)
        print(f"loss: {loss}, accuracy: {accuracy}")

        return {
            "loss": loss,
            "accuracy": accuracy
        }