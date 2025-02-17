from model_regulation.repository.model_regulation_repository import ModelRegulationRepository

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

from tensorflow.keras.datasets import mnist

from tensorflow.keras.utils import to_categorical
from tensorflow.keras import  layers, models, regularizers


class ModelRegulationRepositoryImpl(ModelRegulationRepository):

    def loadData(self):
        return mnist.load_data()

    def preprocessData(self, x, y, numClasses):
        x = x.reshape(-1, 28 * 28).astype('float32') / 255.0
        y = to_categorical(y, numClasses)

        return x, y

    def buildModel(self, inputShape, numClasses):
        model = models.Sequential([
            Dense(128, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            layers.Dropout(0.5),
            Dense(64, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            layers.Dropout(0.5),
            Dense(32, activation='relu', kernel_regularizer=regularizers.l2(0.01)),
            layers.Dropout(0.5),
            Dense(10, activation='softmax'),
        ])

        return model

    def compileModel(self, model):
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

    def trainModel(self, buildModel, X_train, y_train):
        buildModel.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

    def evaluateModel(self, buildModel, X_test, y_test):
        loss, accuracy = buildModel.evaluate(X_test, y_test)
        return loss, accuracy