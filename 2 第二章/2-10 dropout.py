from tensorflow import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
import os
import sys

def plot_learning_curves(history):

    pd.DataFrame(history.history).plot(figsize=(8,5))
    plt.grid(True)
    plt.gca().set_ylim(0,1)
    plt.show()


fashion_mnist = keras.datasets.fashion_mnist
(x_train_all, y_train_all),(x_test,y_test) = fashion_mnist.load_data()
x_valid,x_train = x_train_all[:5000],x_train_all[5000:]
y_valid,y_train = y_train_all[:5000],y_train_all[5000:]

#数据归一化
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
#x_train: [None, 28, 28] -> [None,784]
x_train_scaled = scaler.fit_transform(x_train.astype(np.float32).reshape(-1, 1)).reshape(-1, 28, 28)
x_valid_scaled = scaler.transform(x_valid.astype(np.float32).reshape(-1,1)).reshape(-1,28,28)
x_test_scaled = scaler.transform(x_test.astype(np.float32).reshape(-1,1)).reshape(-1,28,28)



model = tf.keras.models.Sequential()
model.add(keras.layers.Flatten(input_shape=[28,28]))
for _ in range(20):
    model.add(keras.layers.Dense(100,activation='selu')) #selu是自带归一化的
#使用dropout
    #AlphaDropout: 1、均值和方差不变 2、归一化性质也不变
model.add(tf.keras.layers.AlphaDropout(rate=0.5))
   # model.add(tf.keras.layers.Dropout(rate=0.5))
#批归一化放在激活函数后面
   # model.add(keras.layers.Dense(100,activation='relu'))
   # model.add(keras.layers.BatchNormalization())
"""
    model.add(keras.layers.Dense(100))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Activation('relu'))
"""
model.add(keras.layers.Dense(10,activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
#使用了三个callback：Tensorboard, earlystopping, ModelCheckpoint
#logdir = './callbacks'
logdir = os.path.join("dnn-callbacks")
if not os.path.exists(logdir):
    os.mkdir(logdir)
output_model_file = os.path.join(logdir,"fashion_mnist_model.h5")
print("out:",output_model_file)
callbacks = [
    tf.keras.callbacks.TensorBoard(logdir),
    tf.keras.callbacks.ModelCheckpoint(output_model_file,save_best_only=True),
    tf.keras.callbacks.EarlyStopping(patience=5, min_delta=1e-3)
]
history = model.fit(x_train_scaled, y_train, epochs=10, validation_data=(x_valid_scaled, y_valid),callbacks=callbacks)
model.evaluate(x_test_scaled,y_test)
plot_learning_curves(history)
