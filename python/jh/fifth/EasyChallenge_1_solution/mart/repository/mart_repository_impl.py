from mart.entity.mart import Mart
from mart.repository.mart_repository import MartRepository


class MartRepositoryImpl(MartRepository):
    __instance = None

    __mart = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__mart = Mart()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self, fruitName, fruitCount):
        self.__mart.updateFruit(fruitName, fruitCount)

    def mapList(self):
        return self.__mart.getFruitMap()

    def update(self, fruitName, quantity):
        #fruitMap = self.mapList()
        self.__mart.updateFruit(fruitName, quantity)
