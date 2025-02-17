import mnist
from mnist.repository.mnist_repository_impl import MnistRepositoryImpl
from mnist.service.mnist_service import MnistService


class MnistServiceImpl(MnistService):

    def __init__(self):
        self.__mnistRepository = MnistRepositoryImpl()

    async def requestProcess(self):
        X_train, y_train, X_test, y_test = self.__mnistRepository.loadData()
        X_train, y_train, X_test, y_test = self.__mnistRepository.preprocessData(
            X_train, y_train, X_test, y_test)

        buildModel = self.__mnistRepository.buildModel()
        self.__mnistRepository.compileModel(buildModel)
        self.__mnistRepository.trainModel(buildModel, X_train, y_train)
        accuracy = self.__mnistRepository.evaluateModel(buildModel, X_test, y_test)

        return accuracy