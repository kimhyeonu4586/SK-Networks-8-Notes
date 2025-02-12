from dice.entity.dice_kinds import DiceKinds
from dice.entity.dice_skill import DiceSkill
from dice.repository.dice_repository_impl import DiceRepositoryImpl
from game.repository.game_repository_impl import GameRepositoryImpl
from game.service.game_service import GameService
from player.repository.player_repository_impl import PlayerRepositoryImpl


class GameServiceImpl(GameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # Service Layer에서 Repository Layer를 연결하는 방법
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
        self.__gameRepository.create()    # game 객체 생성, player 수 생성

        self.__createGamePlayer()       # player 이름 리스트 생성

    def printCurrentStatus(self):
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()
        playerDiceNumberList = [] # 주사위 번호 출력을 위해 잠시 거쳐 가는 용도

        for playerId, diceIdList in playerDiceGameMap.items():
            player = self.__playerRepository.findById(playerId)
            for diceId in diceIdList:
                dice = self.__diceRepository.findById(diceId)
                playerDiceNumberList.append(dice.getDiceNumber())

            print(f"플레이어 정보: {player}, 주사위 눈금 리스트: {playerDiceNumberList}")
            playerDiceNumberList.clear()

    def rollFirstDice(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()
        playerIndexList = []
        diceIdList = []

        # 실제 정말 사용자 숫자만큼 반복을 함 (3명이라 가정)
        # 위 가정의 경우 0, 1, 2로 playerIndex가 설정됨
        for playerIndex in range(gamePlayerCount):
            print(f"playerIndex: {playerIndex}")
            # 기존에는 단순히 굴리기만 했음
            # 혹은 굴리고 Dice 객체 자체를 리턴했음
            # 그러나 Player가 어떤 Dice 객체를 소유하고 있는지 판단할 필요가 생겼음(스킬 부여 때문)
            # 그러므로 rollDice() 이후 생성된 주사위의 고유한 번호(id)를 리턴시켰음
            diceId = self.__diceRepository.rollDice() # rollDice()하고 diceId를 return
            diceIdList.append(diceId)
            # 위의 인덱스는 0부터 시작하지만 Entity 구성의 id가 1부터 시작함
            # 그러므로 발생한 이격을 조정하기 위해 +1을 해서 검색하고 있음
            # findById()를 통해 검색된 Player 객체를 획득
            indexedPlayer = self.__playerRepository.findById(playerIndex + 1) # findById는 player 객체를 리턴
            print(f"indexedPlayer: {indexedPlayer}")

            playerIndexList.append(playerIndex + 1)

            # Player 엔티티에 addDiceId를 구현하여 획득한 주사위의 번호를 설정함
            # 고로 특정 Player가 특정 Dice의 소유권을 확보하게 되었음
            indexedPlayer.addDiceId(diceId) # service 계층이 entity 계층을 관리

        for player in self.__playerRepository.acquirePlayerList():
            print(f"{player}")

        self.__gameRepository.setPlayerIndexListToMap(playerIndexList, diceIdList)

    def __checkSkillAppliedPlayerIndexList(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()
        skillAppliedPlayerList = []
                   # 주사위 숫자가 짝수이면 스킬 적용한다.
        for playerIndex in range(gamePlayerCount):
            indexedPlayer = self.__playerRepository.findById(playerIndex + 1) # +1 은 index는 0부터 시작해서 id와 맞춰 주는것
            indexedPlayerDiceIdList = indexedPlayer.getDiceIdList()
            indexedPlayerFirstDiceId = indexedPlayerDiceIdList[0]

            indexedPlayerDice = self.__diceRepository.findById(indexedPlayerFirstDiceId)
            if indexedPlayerDice.getDiceNumber() % 2 == 0:
                skillAppliedPlayerList.append(playerIndex + 1)

        return skillAppliedPlayerList

    def rollSecondDice(self):
        skillAppliedPlayerIndexList = self.__checkSkillAppliedPlayerIndexList()
        skillAppliedPlayerLength = len(skillAppliedPlayerIndexList)
        secondDiceIdList = []

        for index in range(skillAppliedPlayerLength):
            secondDiceId = self.__diceRepository.rollDice()
            secondDiceIdList.append(secondDiceId)
                    # skill적용된 플레이어 인덱스 == 플레이어 id인, player 객체를 찾아 second_dice_id 추가
            skillAppliedPlayerIndex = skillAppliedPlayerIndexList[index]
            skillAppliedPlayer = self.__playerRepository.findById(skillAppliedPlayerIndex) # Player 객체이다
            skillAppliedPlayer.addDiceId(secondDiceId)
            print(f"skillAppliedPlayer: {skillAppliedPlayer}")

            secondDice = self.__diceRepository.findById(secondDiceId)  # Dice 객체이다
            secondDice.setDiceKinds(DiceKinds.SPECIAL)
            print(f"secondDice: {secondDice}")

        self.__gameRepository.updatePlayerDiceGameMap(
            skillAppliedPlayerIndexList, secondDiceIdList) # DiceId 리스트의 요소더 리스트

        # playerIndex 플레이어의 점수는 올리고, 나머지 플레이어의  dice 숫자 깎음
    def __steelScore(self, playerIndex):
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()

        for playerId, diceIdList in playerDiceGameMap.items():
                  # playerId 는 __counter 여서 1부터, playerIndex는 0부터 여서 Index+1
            if playerId == playerIndex + 1:
                firstDiceId = diceIdList[0]
                firstDice = self.__diceRepository.findById(firstDiceId)

                if firstDice: # 해당 주사위가 있으면
                    gamePlayerCount = self.__gameRepository.getGamePlayerCount()
                    diceNumber = firstDice.getDiceNumber()
                    firstDice.setDiceNumber(diceNumber + 2 * (gamePlayerCount - 1))

                continue # if playerId == playerIndex + 1: 참이면 다시 반복문으로 감

            # 아래는 if playerId == playerIndex + 1: 가 아닌 경우
            # 즉, 이 함수에서 인수로 받은 index에 해당하는 player를 제외한 player 모두
            firstDiceId = diceIdList[0]
            firstDice = self.__diceRepository.findById(firstDiceId)

            if firstDice:
                diceNumber = firstDice.getDiceNumber()
                firstDice.setDiceNumber(diceNumber - 2)

    def __deathShot(self):
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()

        playerDiceSum = {}
           # 플레이어 아이디, 플레이어의 diceId 리스트
        for playerId, diceIdList in playerDiceGameMap.items():
            diceSum = 0

            for diceId in diceIdList:
                dice = self.__diceRepository.findById(diceId)

                if dice:  # 일치하는 dice 객체가 있으면
                    diceSum += dice.getDiceNumber()

            playerDiceSum[playerId] = diceSum

        for playerId, diceSum in playerDiceSum.items():
            print(f"플레이어 {playerId}의 누산 점수: {diceSum}")

        deathShotTargetPlayerId = int(input('누구를 저격하시겠습니까? '))
        self.__gameRepository.deletePlayer(deathShotTargetPlayerId)

    def __applySkill(self, playerIndex, secondDice):
        secondDiceNumber = secondDice.getDiceNumber()
        print(f"secondDiceNumber: {secondDiceNumber}")

        if secondDiceNumber == DiceSkill.STEEL_SCORE.value:
            self.__steelScore(playerIndex)

        if secondDiceNumber == DiceSkill.DEATH_SHOT.value:
            self.__deathShot()

          # __applySkill()을 위한 조건을 검사하는 함수 -> diceId가 두개 아상이어야 함
    def applySkill(self):
        gamePlayerCount = self.__gameRepository.getGamePlayerCount()

        for playerIndex in range(gamePlayerCount):
            indexedPlayer = self.__playerRepository.findById(playerIndex + 1)
            indexedPlayerDiceIdList = indexedPlayer.getDiceIdList()
            indexedPlayerDiceIdListLength = len(indexedPlayerDiceIdList)

            if indexedPlayerDiceIdListLength < 2:
                continue
                        # diceId가 두개인 애들만 반복문을 넘어옴(스킬 적용된 애들)
            indexedPlayerSecondDiceId = indexedPlayerDiceIdList[1] # 0부터 카운트 돼서 1은 2번째 dice
            secondDice = self.__diceRepository.findById(indexedPlayerSecondDiceId)

            self.__applySkill(playerIndex, secondDice)

    def checkWinner(self):
        print("checkWinner() called!")
        game = self.__gameRepository.getGame()
        playerDiceGameMap = game.getPlayerDiceGameMap()

        playerDiceSum = {}

        for playerId, diceIdList in playerDiceGameMap.items():
            diceSum = 0

            for diceId in diceIdList:
                dice = self.__diceRepository.findById(diceId)

                if dice:
                    diceSum += dice.getDiceNumber()

            playerDiceSum[playerId] = diceSum


        maxDiceSum = max(playerDiceSum.values())
        # 리스트 컴프리핸션 사용
        maxDicePlayerList = [playerId for playerId, diceSum in playerDiceSum.items()
                             if diceSum == maxDiceSum]

        # 반복문 사용
        # maxDicePlayerIdList = []
        # for playerId, diceSum in playerDiceSum.items():
        #     if diceSum == maxDiceSum:
        #         maxDicePlayerIdList.append(playerId)
        
        if len(maxDicePlayerList) > 1:
            print("무승부")
            return          # 무승부이면 여기서 종결, return은 함수 실행 즉시 종료하고 반환

        winnerId = maxDicePlayerList[0]
        winner = self.__playerRepository.findById(winnerId)
        print(f"승자: {winner}")
