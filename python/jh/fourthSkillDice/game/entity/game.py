class Game:
    __playerDiceGameMap = {}

    def __init__(self, playerCount):
        self.__playerCount = playerCount

    def getPlayerCount(self):
        return self.__playerCount

    def getPlayerDiceGameMap(self):
        return self.__playerDiceGameMap

    def setPlayerIndexListToMap(self, playerIndexList, diceIdList):
                                        # 딕셔너리 컴프리핸션 구조 {key: value for key, value in 반복 가능 객체}
                                        # index를 key로,  diceId를 리스트 형태의 value 로 가짐
                                                                        # zip()은 반복 가능 객체들을 튜플로 반환
        self.__playerDiceGameMap = { index: [diceId] for index, diceId in zip(playerIndexList, diceIdList) }
        print(f"self.__playerDiceGameMap: {self.__playerDiceGameMap}")

    def updatePlayerIndexListToMap(self, playerIndexList, diceIdList):
        for index, diceId in zip(playerIndexList, diceIdList):
            if index in self.__playerDiceGameMap:
                     # __playerDiceGameMap[index]는 diceId 리스트를 참조
                self.__playerDiceGameMap[index].append(diceId)
                    # 위의 if문이 참이면 다시 반복으로 넘어감
                continue
            # if 문이 거짓일 경우, index를 key로 가지는 valuedls 리스트에 diceId를 할당
            self.__playerDiceGameMap[index] = [diceId]

        print(f"self.__playerDiceGameMap: {self.__playerDiceGameMap}")

    def deleteTargetPlayerId(self, targetPlayerId):
        if targetPlayerId in self.__playerDiceGameMap:
            # Map에서 특정 쌍 완전히 제거
            # 정확히는 targetPlayerId를 key로 사용하는 정보를 완전히 제거함
            del self.__playerDiceGameMap[targetPlayerId]

        print(f"저격 이후 self.__playerDiceGameMap: {self.__playerDiceGameMap}")
