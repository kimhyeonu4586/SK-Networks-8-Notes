from game.entity.game import Game
from game.repository.game_repository import GameRepository


class GameRepositoryImpl(GameRepository):
    __instance = None

    __game = None  # Game 클리스의 인스턴스를 저장하기 위해(계층을 연결하기 위해)사용 -> repository가 entity를 관리

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def create(self):
        while True:
            try:
                playerCount = int(input('몇 명이 플레이 하나요? '))
                if playerCount <= 1:
                    print("플레이어 숫자는 반드시 2명 이상이 필요합니다!")
                    continue

                game = Game(playerCount)
                self.__game = game

                break

            except ValueError:
                print("플레이 인원 수를 숫자로 입력해주세요!")

    def setPlayerIndexListToMap(self, playerIndexList, diceIdList):
        self.__game.setPlayerIndexListToMap(playerIndexList, diceIdList)

    def updatePlayerDiceGameMap(self, skillAppliedPlayerIndexList, secondDiceIdList):
        self.__game.updatePlayerIndexListToMap(skillAppliedPlayerIndexList, secondDiceIdList)

    def deletePlayer(self, tagetPlayerId):
        self.__game.deleteTargetPlayerId(tagetPlayerId)

    def getGamePlayerCount(self):
        return self.__game.getPlayerCount()

    def getGame(self):
        return self.__game
