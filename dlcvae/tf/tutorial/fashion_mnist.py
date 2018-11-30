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
(train_images, train_lables),(test_images, test_labels) = fashion_mnist.load_data()

dirname = os.path.join('datasets', 'fashion-mnist')
print("文件缓存目录：%s"%dirname)

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
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

#step05:训练模型
model.fit(train_images, train_lables, epochs=5)

model_weights_save_path = './fashion.weight'
model_save_path = './fashion.model'

model.save_weights(model_weights_save_path)     #把模型参数保存为一个HDF5文件
model.save(model_save_path)                #把模型保存为一个HDF5文件


# model = keras.models.load_model(model_file_save_path)

#step06:评估准确率
# Test accuracy: 0.8727
# Test accuracy: 0.8749
# test_loss, test_acc = model.evaluate(test_images, test_labels)
# print('Test Loss:', test_loss)
# print('Test accuracy:', test_acc)

#step07:作出预测
# predictions = model.predict(test_images)
# print('预测的置信度：%s'%str(predictions))
# print('置信度最大值（标签值）：%s'%str(np.argmax(predictions[0])))
# print(test_labels[0])


# def plot_image(i, predictions_array, true_label, img):
#   predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
#   plt.grid(False)
#   plt.xticks([])
#   plt.yticks([])
#
#   plt.imshow(img, cmap=plt.cm.binary)
#
#   predicted_label = np.argmax(predictions_array)
#   if predicted_label == true_label:
#     color = 'blue'
#   else:
#     color = 'red'
#
#   plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
#                                 100*np.max(predictions_array),
#                                 class_names[true_label]),
#                                 color=color)
#
# def plot_value_array(i, predictions_array, true_label):
#   predictions_array, true_label = predictions_array[i], true_label[i]
#   plt.grid(False)
#   plt.xticks([])
#   plt.yticks([])
#   thisplot = plt.bar(range(10), predictions_array, color="#777777")
#   plt.ylim([0, 1])
#   predicted_label = np.argmax(predictions_array)
#
#   thisplot[predicted_label].set_color('red')
#   thisplot[true_label].set_color('blue')
#
# i = 0
# plt.figure(figsize=(6,3))
# plt.subplot(1,2,1)
# plot_image(i, predictions, test_labels, test_images)
# plt.subplot(1,2,2)
# plot_value_array(i, predictions,  test_labels)
#
# i = 12
# plt.figure(figsize=(6,3))
# plt.subplot(1,2,1)
# plot_image(i, predictions, test_labels, test_images)
# plt.subplot(1,2,2)
# plot_value_array(i, predictions,  test_labels)
#
# # Plot the first X test images, their predicted label, and the true label
# # Color correct predictions in blue, incorrect predictions in red
# num_rows = 5
# num_cols = 3
# num_images = num_rows*num_cols
# plt.figure(figsize=(2*2*num_cols, 2*num_rows))
# for i in range(num_images):
#   plt.subplot(num_rows, 2*num_cols, 2*i+1)
#   plot_image(i, predictions, test_labels, test_images)
#   plt.subplot(num_rows, 2*num_cols, 2*i+2)
#   plot_value_array(i, predictions, test_labels)
#
# # Grab an image from the test dataset
# img = test_images[0]
# print(img.shape)
#
# predictions_single = model.predict(img)
# print(predictions_single)
#
# plot_value_array(0, predictions_single, test_labels)
# _ = plt.xticks(range(10), class_names, rotation=45)
#
# np.argmax(predictions_single[0])