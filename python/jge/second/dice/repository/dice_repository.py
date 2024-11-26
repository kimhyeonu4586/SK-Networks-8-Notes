from abc import ABC, abstractmethod

#ABC는 Abxtract Class라는 뜻을 가지고 있음
#즉 DiceRepository(ABC)는 '추상화 클래스'라는 뜻을 가짐
#'추상화 클래스' 는 인터페이스들의 집합
#인터페이스란 용어가 와닿지 않을테니 R(궁극기)라고 생각하면됨

#R키는 상징적으로 궁극기 그러나 실제 캐릭터들은 제각각 다른 궁극기들을 펼침
#여기까지 인터페이스라 생각하면됨


class DiceRepository(ABC):
    #@abstractmethod는 ABC 클래스 내에 인터페이스를 선언 할 경우 사용
    @abstractmethod
    def rollDice(self):
        pass #아무것도 하지 않음