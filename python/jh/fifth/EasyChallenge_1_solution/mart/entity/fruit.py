from enum import Enum

class Fruit(Enum):
    APPLE = ("사과", 1)
    ORANGE = ("오렌지", 2)

    def __init__(self, label, value):
        self.label = label
        self.value = value

    def __str__(self):
        return self.label
