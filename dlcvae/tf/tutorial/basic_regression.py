# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf
from tensorflow import keras

import numpy as np

print('Tensorflow Version: %s'%tf.__version__)

#波士顿房价数据集
boston_housing = keras.datasets.boston_housing

(train_data, train_labels), (test_data, test_labels) = boston_housing.load_data()

# Shuffle the training set
order = np.argsort(np.random.random(train_labels.shape))
train_data = train_data[order]
train_labels = train_labels[order]

#样本和特征
# 了解如何探索和清理此类数据是一项需要加以培养的重要技能。
print("Training set: {}".format(train_data.shape))  # 404 examples, 13 features
print("Testing set:  {}".format(test_data.shape))   # 102 examples, 13 features


# 要点：作为建模者兼开发者，需要考虑如何使用这些数据，以及模型预测可能会带来哪些潜在益处和危害。
# 类似这样的模型可能会加深社会偏见，扩大社会差异。某个特征是否与您想要解决的问题相关，或者是否会
# 引入偏见？要了解详情，请参阅机器学习公平性。

print(train_data[0])  # Display sample features, notice the different scales

import pandas as pd

column_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD','TAX', 'PTRATIO', 'B', 'LSTAT']

df = pd.DataFrame(train_data, columns=column_names)
print(df.head())

print(train_labels[0:10])  # Display first 10 entries

#标准化特征
# Test data is *not* used when calculating the mean and std

mean = train_data.mean(axis=0)      #平均值
std = train_data.std(axis=0)        #标准偏差
train_data = (train_data - mean) / std
test_data = (test_data - mean) / std

print(train_data[0])  # First training sample, normalized

#创建模型
def build_model():
  model = keras.Sequential([
    keras.layers.Dense(64, activation=tf.nn.relu, input_shape=(train_data.shape[1],)),
    keras.layers.Dense(64, activation=tf.nn.relu),
    keras.layers.Dense(1)
  ])
  optimizer = tf.train.RMSPropOptimizer(0.001)
  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae'])
  return model

model = build_model()
model.summary()

#训练模型
# Display training progress by printing a single dot for each completed epoch
class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 500
# Store training stats
history = model.fit(train_data, train_labels, epochs=EPOCHS, validation_split=0.2, verbose=0, callbacks=[PrintDot()])

import matplotlib.pyplot as plt


# 此图显示，在大约 200 个周期之后，模型几乎不再出现任何改进
# 如果模型在一定数量的周期之后没有出现任何改进，则自动停止训练。
def plot_history(history):
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [1000$]')
  plt.plot(history.epoch, np.array(history.history['mean_absolute_error']),
           label='Train Loss')
  plt.plot(history.epoch, np.array(history.history['val_mean_absolute_error']),
           label = 'Val loss')
  plt.legend()
  plt.ylim([0, 5])
  plt.show()

plot_history(history)

model = build_model()

# The patience parameter is the amount of epochs to check for improvement
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20)

history = model.fit(train_data, train_labels, epochs=EPOCHS,
                    validation_split=0.2, verbose=0,
                    callbacks=[early_stop, PrintDot()])

plot_history(history)

[loss, mae] = model.evaluate(test_data, test_labels, verbose=0)
print("Testing set Mean Abs Error: ${:7.2f}".format(mae * 1000))

#预测
test_predictions = model.predict(test_data).flatten()

plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [1000$]')
plt.ylabel('Predictions [1000$]')
plt.axis('equal')
plt.xlim(plt.xlim())
plt.ylim(plt.ylim())
_ = plt.plot([-100, 100], [-100, 100])
plt.show()

error = test_predictions - test_labels
plt.hist(error, bins = 50)
plt.xlabel("Prediction Error [1000$]")
_ = plt.ylabel("Count")
plt.show()


# 均方误差 (MSE) 是用于回归问题的常见损失函数（与分类问题不同）。
# 同样，用于回归问题的评估指标也与分类问题不同。常见回归指标是平均绝对误差 (MAE)。
# 如果输入数据特征的值具有不同的范围，则应分别缩放每个特征。
# 如果训练数据不多，则选择隐藏层较少的小型网络，以避免出现过拟合。
# 早停法是防止出现过拟合的实用技术。