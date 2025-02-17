import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

from tensorflow.keras.datasets import mnist

from tensorflow.keras.utils import to_categorical

from mnist.repository.mnist_repository import MnistRepository


class MnistRepositoryImpl(MnistRepository):

    # 데이터를 로드함
    # MNIST를 로드하여 (X_train, y_train), (X_test, y_test)에 각각 배치
    # X 계열은 이미지 데이터(픽셀 값)
    # y 계열은 이미지의 레이블(숫자 0 ~ 9)
    def loadData(self):
        (X_train, y_train), (X_test, y_test) = mnist.load_data()
        return X_train, y_train, X_test, y_test

    # 데이터 전처리
    # 기본적인 RGB는 0 ~ 255에 해당함
    # 그래픽 카드는 이것을 0.0 ~ 1.0 사이로 취급하여 보다 세밀하게 관찰 할 수 있음
    # 고로 위의 값들을 255로 나눠서 0.0 ~ 1.0 사이로 스케일함 (정규화라고도 함)
    # to_categorical이라는 것을 통해서 One-Hot Encoding이라는 것을 진행함
    # 복잡하게 생각할 필요 없이 숫자 3의 경우
    # [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    # 숫자 4의 경우
    # [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
    # 숫자 5의 경우
    # [0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    def preprocessData(self, X_train, y_train, X_test, y_test):
        X_train, X_test = X_train / 255.0, X_test / 255.0
        y_train, y_test = to_categorical(y_train, num_classes=10), to_categorical(y_test, num_classes=10)
        return X_train, y_train, X_test, y_test

    # 딥러닝 모델을 구축함
    # 사실 숫자는 input을 제외하고 마지막 softmax 제외하고 전부 맘대로 멋대로 실험적으로 넣어봐도 무방함
    # 넣어서 잘 되는 것을 찾는 실험적인 영역에 해당함 (사실 이론이 생각 보다 잘 안 쓰임)
    # 추후 살펴보겠지만 데이터 추이가 요동을 치거나 들쭉 날쭉하다면 cosh, sinh 계열을 사용하면 됨
    # 결국 직관력 및 구현력(행동력)의 싸움이 되어버렸음
    # 그리고 여러 실험을 하기 위해 시간이 필요함 (뭐가 잘 되는지 찾아야 하니까)
    def buildModel(self):
        model = Sequential([
            # 입력 이미지를 1차원 벡터로 변환 28x28
            Flatten(input_shape=(28, 28)),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            # 출력층으로 10개의 노드를 가지고 e (익스포넨셜 - 오일러 상수) 계열로 값을 처리함
            # 계산 결과는 0 ~ 1 사이로 수렴하게 되는데
            # 결국 이것을 보고 앞서 One Hot Encoding 했던 내용중 무엇이다를 판정함
            # [0, 0, 0, 0, 0, 1, 0, 0, 0, 0] <<< 이게 숫자 5였음
            # 각 자리별로 계산된 수치값이 존재함
            # 그리고 가장 높은 확률값이 나타나는 것을 선택하게 됨
            # [0.01, 0.01, 0.01, 0.01, 0.01, 0.91, 0.01, 0.01, 0.01, 0.01]
            Dense(10, activation='softmax'),
        ])
        return model

    def compileModel(self, buildModel):
        # Adam 최적화 알고리즘을 사용함 (너무 깊게 파진 맙시다 - 수학 시간이 되니까)
        # categorical_crossentropy는 분류 문제를 계산할 때 사용하는 손실 함수
        # metrics=['accuracy'] 의 경우 학습 과정에서 정확도를 평가
        buildModel.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    # 훈련 데이터들을 가지고 모델을 학습시킴
    # y = ax + b를 찾는 것이라고 하였음
    # 이것을 만들기 위해 전체 데이터를 10번 반복학습 (epochs=10)
    # batch_size=32는 한 번에 데이터 32개를 처리
    # validation_split=0.2 20%의 데이터를 검증용으로 사용함을 의미함
    def trainModel(self, buildModel, X_train, y_train):
        buildModel.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    # 모델 평가
    # _, accuracy 실제로 _에 해당하는 녀석은 손실값
    # 근데 정확도가 궁금해서 그냥 _ 처리
    def evaluateModel(self, buildModel, X_test, y_test):
        _, accuracy = buildModel.evaluate(X_test, y_test)
        return accuracy
