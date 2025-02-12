import sys
from dice.entity.dice_kinds import DiceKinds
from dice.entity.dice_skill import DiceSkill
from dice.repository.dice_repository_impl import DiceRepositoryImpl
from game.repository.game_repository_impl import GameRepositoryImpl
from player.repository.player_repository_impl import PlayerRepositoryImpl
from game.service.game_service import GameService


class GameServiceImpl(GameService):
    __instance = None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__gameRepository = GameRepositoryImpl.getInstance()
            cls.__instance.__playerRepository = PlayerRepositoryImpl.getInstance()
            cls.__instance.__diceRepository = DiceRepositoryImpl.getInstance()

        return cls.__instance


    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance


    def __createGamePlayer(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()

        for _ in range(gamePlayerCount):
            self.__playerRepository.createName()


    def startDiceGame(self):
        print("startDiceGame() called!")
        self.__gameRepository.create()

        self.__createGamePlayer()


    def rollFirstDice(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()
        playerIndexList = []
        diceIdList = []

        for playerIndex in range(gamePlayerCount):
            print(f"playerIndex: {playerIndex}")

            diceId = self.__diceRepository.rollDice()
            diceIdList.append(diceId)

            indexedPlayer = self.__playerRepository.findByPlayerId(playerIndex + 1)
            print(f"indexPlayer: {indexedPlayer}")
            playerIndexList.append(playerIndex + 1)
            indexedPlayer.addDiceId(diceId)

        for player in self.__playerRepository.getPlayerList():
            print(f"{player}")

        self.__gameRepository.setPlayerIndexListToMap(playerIndexList,diceIdList)


    def __checkSkillAppliedPlayerIndexList(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()
        skillApliedPlayerList = []

        for playerIndex in range(gamePlayerCount):
            indexedPlayer = self.__playerRepository.findByPlayerId(playerIndex + 1)
            indexedPlayerDiceIdList = indexedPlayer.getDiceIdList()
            indexedPlayerFirstDice = indexedPlayerDiceIdList[0]

            indexedPlayerDice = self.__diceRepository.findByDiceId(indexedPlayerFirstDice)
            if indexedPlayerDice.getDiceNumber() % 2 == 0:
                skillApliedPlayerList.append(playerIndex + 1)

        return skillApliedPlayerList


    def rollSecondDice(self):
        skillAppliedPlayerIndexList = self.__checkSkillAppliedPlayerIndexList()
            # 아래는 player의 firstRollDice 결과가 모두 홀수일 경우
        if len(skillAppliedPlayerIndexList) == 0:
            self.checkWinner()
            sys.exit()

        skillAppliedPlayerLength = len(skillAppliedPlayerIndexList)
        secondDiceIdList = []

        for index in range(skillAppliedPlayerLength):
            secondDiceId = self.__diceRepository.rollDice()
            secondDiceIdList.append(secondDiceId)

            skillApliedPlayerIndex = skillAppliedPlayerIndexList[index]
            skillApliedPlayer = self.__playerRepository.findByPlayerId(skillApliedPlayerIndex)
            skillApliedPlayer.addDiceId(secondDiceId)
            print(f"skillAppliedPlyer: {skillApliedPlayer}")

            secondDice = self.__diceRepository.findByDiceId(secondDiceId)
            secondDice.setDiceKinds(DiceKinds.GENERAL)
            print(f"secondDice: {secondDice}")

        self.__gameRepository.updatePlayerDiceGameMap(
            skillAppliedPlayerIndexList, secondDiceIdList)


    def __stealScore(self, playerIndex):
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()

        for playerId, diceIdList in playerDiceGameMap.items():
            if playerId == playerIndex + 1:
                firstDiceId = diceIdList[0]
                firstDice = self.__diceRepository.findByDiceId(firstDiceId)

                if firstDice:
                    gamePlayerCount = self.__gameRepository.getGamePlayerCount()
                    diceNumber = firstDice.getDiceNumber()
                    firstDice.setDiceNumber(diceNumber + 2 * (gamePlayerCount - 1) )

                continue

            firstDiceId = diceIdList[0]
            firstDice = self.__diceRepository.findByDiceId(firstDiceId)

            if firstDice:
                diceNumber = firstDice.getDiceNumber()
                firstDice.setDiceNumber(diceNumber - 2)


    def playerDiceSumMap(self):
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()

        playerDiceSum = {}

        for playerId, diceIdList in playerDiceGameMap.items():
            diceSum = 0

            for diceId in diceIdList:
                dice = self.__diceRepository.findByDiceId(diceId)

                if dice:
                    diceSum += dice.getDiceNumber()

            playerDiceSum[playerId] = diceSum

        return playerDiceSum


    def printPlayerDiceSum(self):
        playerDiceSumMap = self.playerDiceSumMap()
        for playerId, diceSum in playerDiceSumMap.items():
            print(f"Player: {playerId} Accumulation Score: {diceSum}")


    def __deathShot(self):
        self.playerDiceSumMap()

        deathShotTargetPlayerId = int(input("Choose Player ID that you want Death-Shot: "))
        self.__gameRepository.deletePlayer(deathShotTargetPlayerId)


    def __applySkill(self, playerIndex, secondDice):
        secondDiceNumber = secondDice.getDiceNumber()
        print(f"secondDiceNumber: {secondDiceNumber}")

        if secondDiceNumber == DiceSkill.STEAL_SCORE.value:
            self.__stealScore(playerIndex)

        if secondDiceNumber == DiceSkill.DEATH_SHOT.value:
            self.__deathShot()


    def applySkill(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()

        for playerIndex in range(gamePlayerCount):
            indexedPlayer = self.__playerRepository.findByPlayerId(playerIndex + 1)
            indexedPlayerDiceIdList = indexedPlayer.getDiceIdList()
            indexedPlayerDiceIdListLength = len(indexedPlayerDiceIdList)

            if indexedPlayerDiceIdListLength < 2:
                continue

            indexedPlayerSecondDiceId = indexedPlayerDiceIdList[1]
            secondDice = self.__diceRepository.findByDiceId(indexedPlayerSecondDiceId)

            self.__applySkill(playerIndex, secondDice)


    def printCurrentStatus(self):
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()
        playerDiceNumberList = []

        for playerId, diceIdList in playerDiceGameMap.items():
            player = self.__playerRepository.findByPlayerId(playerId)
            for diceId in diceIdList:
                dice = self.__diceRepository.findByDiceId(diceId)
                playerDiceNumberList.append(dice.getDiceNumber())

            playerDiceSum = 0
            for diceNumber in playerDiceNumberList:
                playerDiceSum += diceNumber

            print(f"Player Information: {player},List of Dice Number: {playerDiceNumberList},"
                  f" Sum of Dice Number: ({playerDiceSum})")
            playerDiceNumberList.clear()


    def checkWinner(self):
        print("checkWinner() called!")

        playerDiceSumMap = self.playerDiceSumMap()

        maxDiceSum = max(playerDiceSumMap.values())
        maxDicePlayerIdList = []
        for playerId, diceSum in playerDiceSumMap.items():
            if diceSum == maxDiceSum:
                maxDicePlayerIdList.append(playerId)

        # maxDicePlayerIdList = [playerId for playerId, diceSum in playerDiceSum.items()
        #                      if diceSum == maxDiceSum]

        if len(maxDicePlayerIdList) > 1:
            print("Draw")
            return

        winnerId = maxDicePlayerIdList[0]
        winner = self.__playerRepository.findByPlayerId(winnerId)
        print(f"Winner: {winner}")



