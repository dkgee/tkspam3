# -*- coding: utf-8 -*-
import dlcvae.tf.mnist.input_data as input_data

#自动下载mnist数据集， 下载地址http://yann.lecun.com/exdb/mnist/
# train-images-idx3-ubyte：训练图像
# train-labels-idx1-ubyte：训练标签
# t10k-images-idx3-ubyte：测试图像
# t10k-labels-idx1-ubyte：测试标签
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)



import tensorflow as tf
#实现回归模型
x = tf.placeholder("float", [None, 784])
W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x,W) + b)

#训练模型
y_ = tf.placeholder("float", [None,10])
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)
for i in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

#评估模型， 准确率：0.917700。
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print("准确率：%f。"%sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))


