# -*- coding: utf-8 -*-

import tensorflow as tf
from tensorflow import keras

print('Tensorflow Version: %s'%tf.__version__)

#文本分类，此处对影评进行分类，好评或差评，属于二分类，

# step01: 下载数据
imdb = keras.datasets.imdb
(train_data, train_labels),(test_data, test_labels) = imdb.load_data(num_words=10000)

# step02: 探索数据
print("Training entries:{}, labels:{}".format(len(train_data), len(train_labels)))
print(train_data[0])

print("第一、二条影评长度：{},二：{}".format(len(train_data[0]),len(train_data[1])))

# A dictionary mapping words to an integer index
word_index = imdb.get_word_index()

# The first indices are reserved
word_index = {k:(v+3) for k,v in word_index.items()}
word_index['<PAD>'] = 0
word_index['<START>'] = 1
word_index['<UNK>'] = 2  #unknown
word_index['<UNUSED>'] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

def decode_review(text):
    return ' '.join([reverse_word_index.get(i, '?') for i in text])

print("第一条影评：%s"%decode_review(train_data[0]))

#准备数据
# 影评必须转换为张量，才能传送到神经网络中去，
# 填充数组，使它们都具有相同的长度
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)

test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                       value=word_index["<PAD>"],
                                                       padding='post',
                                                       maxlen=256)
print("训练样本长度：{},测试样本长度：{}".format(train_data.shape, test_data.shape))
print("第一、二条影评长度：{},二：{}".format(len(train_data[0]),len(train_data[1])))
print(train_data[0])    #输出填充后的模型

#构建模型
# 神经网络通过堆叠层创建而成，多少个层？每个层使用多少个隐藏单元？

# input shape is the vocabulary count used for the movie reviews (10,000 words)
vocab_size = 10000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size + 1, 16))       # 第一层是 Embedding 层 (batch, sequence, embedding)
model.add(keras.layers.GlobalAveragePooling1D())        # 对序列维度求平均值
model.add(keras.layers.Dense(16, activation=tf.nn.relu))    # 全连接 (Dense) 层（包含 16 个隐藏单元）
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))  # 最后一层，Sigmoid函数阈值函数，将变量映射到0,1之间

model.summary() #打印模型概要

#损失函数和优化器
model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

#创建验证集
x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

print("训练样本长度：{},训练样本标签长度：{}".format(partial_x_train.shape, partial_y_train.shape))
#训练模型(此处有异常)
history = model.fit(partial_x_train,
                    partial_y_train,
                    epochs=40,
                    batch_size=512,
                    validation_data=(x_val, y_val),
                    verbose=1)

#评估模型，模型会返回两个值：损失（表示误差的数字，越低越好）和准确率。
results = model.evaluate(test_data, test_labels)
print(results)

#创建准确率和损失随时间变化的图
history_dict = history.history
history_dict.keys()

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(acc) + 1)

# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')

# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

plt.clf()   # clear figure
acc_values = history_dict['acc']
val_acc_values = history_dict['val_acc']

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()

#出现过拟合训练

