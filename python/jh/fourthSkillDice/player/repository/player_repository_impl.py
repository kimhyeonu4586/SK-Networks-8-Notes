from player.entity.player import Player
from player.repository.player_repository import PlayerRepository


class PlayerRepositoryImpl(PlayerRepository):

    __instance = None
    __playerList = [] # player 객체가 둘어감, repository 계충이 entity 계층을 관리


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def __processUserInput(self):
        userInputName = input("생성하고자 하는 이름을 입력하세요: ")
        return userInputName

    def createName(self):
        userInputPlayerName = self.__processUserInput()
        player = Player(userInputPlayerName)

        self.__playerList.append(player)

    def acquirePlayerList(self):
        return self.__playerList

    def findById(self, id):
        for player in self.__playerList:
            if player.getId() == id:
                return player

        return None
    