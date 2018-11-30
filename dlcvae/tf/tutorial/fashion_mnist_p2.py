# -*- coding: utf-8 -*-

#基本训练

# Tensorflow and tf.keras
import tensorflow as tf
from tensorflow import keras
import os
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

print('Tensorflow Version: %s'%tf.__version__)

#step01:导入Fashion MNIST数据集
fashion_mnist = keras.datasets.fashion_mnist
# 从文件中读取训练标签和图片数据及测试标签和图片，标签和图片的对应关系就是一一对应的。
# 这种一一对应关系建立的工程量大，是需要程序处理还是人工处理，
(train_images, train_lables),(test_images, test_labels) = fashion_mnist.load_data()

dirname = os.path.join('datasets', 'fashion-mnist')
print("文件缓存目录：%s"%dirname)

#自定义实际标签对象名称
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
#step02:探索数据
print('训练数据集维度: %s'%str(train_images.shape))
print('训练数据集数量：%d'%len(train_lables))
print('测试数据集维度: %s'%str(test_images.shape))
print('测试数据集维度: %d'%len(test_labels))

#step03:预处理数据（将图像转换为浮点数，归一化处理）
train_images = train_images / 255.0
test_images = test_images / 255.0

#显示训练集第一张图片
# plt.figure()
# plt.imshow(train_images[0])

#显示训练集前25张图片
# plt.colorbar()
# plt.grid(False)
# plt.figure(figsize=(10,10))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
#     plt.xlabel(class_names[train_lables[i]])
# plt.show()  #显示图片

#step04:构建模型(设置层、编译模型)  构建和训练网络
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),                 #设置
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#step05:训练模型
model.fit(train_images, train_lables, epochs=5)

#step06:评估准确率
# Test accuracy: 0.8727
# Test accuracy: 0.8749
# Test accuracy: 0.8771
test_loss, test_acc = model.evaluate(test_images, test_labels)
print('Test Loss:', test_loss)
print('Test accuracy:', test_acc)

# model_save_path = './fashion.model.h5'
# model.save(model_save_path)                #把模型保存为一个HDF5文件
### 使用save方法保存模型后，下次加载时，按原路径加载配置，此外还需配置模型编译参数，才能预测
# model = keras.models.load_model(model_save_path)    #加载保存的模型
# model.compile(optimizer=tf.train.AdamOptimizer(),           #配置模型编译方法
#               loss='sparse_categorical_crossentropy',
#               metrics=['accuracy'])

#step07:作出预测
predictions = model.predict(test_images)
# print('预测的置信度：%s'%str(predictions))
print('置信度最大值（标签值）：%s'%str(np.argmax(predictions[0])))
print(test_labels[0])


# 绘制成图展示
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  plt.imshow(img, cmap=plt.cm.binary)
  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'

  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)

  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')

i = 0
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions,  test_labels)
plt.show()  # 即使置信度非常高，也有可能预测错误。

i = 12
plt.figure(figsize=(6,3))
plt.subplot(1,2,1)
plot_image(i, predictions, test_labels, test_images)
plt.subplot(1,2,2)
plot_value_array(i, predictions,  test_labels)
plt.show()

# Plot the first X test images, their predicted label, and the true label
# Color correct predictions in blue, incorrect predictions in red
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols                  #15张图像训练
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)

plt.show()

# Grab an image from the test dataset
img = test_images[0]
print('单个图像尺寸：%s'%str(img.shape))

# 添加一个图片进批量处理集合中
img = (np.expand_dims(img,0))
print(img.shape)

predictions_single = model.predict(img)
print('单个图片预测结果集：%s'%str(predictions_single))

plot_value_array(0, predictions_single, test_labels)
_ = plt.xticks(range(10), class_names, rotation=45)

# model.predict返回一组列表，每个列表对应批次数据中的每张图像。（仅）获取批次数据中相应图像的预测结果
print(np.argmax(predictions_single[0]))

# 此案例评价：通过这个案例，了解了Tensorflow中如何使用Keras深度学习框架API，借助图像库matplotlib进行结果展示
# 单个图像如何处理转换为 集合提供给模型预测
#
# 面临的问题：
#       (1) 准备数据方面：如何运用Keras，在此处如何将数据转换为供keras分析的格式，如何将其和标签建立起关系？
#       (2) 探索数据(分析数据)
#       (3) 预处理数据
#       (4) 构建模型(设置层、编译模型)：
#                   4.1 模型是如何构建的？我该怎样知道我需要构建什么样的模型才能满足当前需求？
#                   4.2 层的种类有哪些？该如何决定使用哪种层？每层激活的训练函数该怎样选择？
#                   4.3 编译模型时，优化函数、loss参数及metric该怎样选择更好？
#       (5) 训练模型: 设置epoch的多少该怎样选择？有什么利弊？
#       (6) 评估准确率
#       (7) 作出预测
#