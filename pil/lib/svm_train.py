"""
SVM示例:

- http://www.cnblogs.com/Finley/p/5329417.html
"""
from pil.lib.svm_lib.svm import svm_problem, svm_parameter
from pil.lib.svm_lib.svmutil import *


def svm_model_train(train_file_name, model_path):
    """
    使用图像的特征文件 来训练生成model文件
    :return:
    """
    y, x = svm_read_problem(train_file_name)
    model = svm_train(y, x)
    svm_save_model(model_path, model)


def svm_model_test(test_feature_file, model_path, lable_to_type_path):
    """
    使用测试集测试模型
    :return:
    """
    yt, xt = svm_read_problem(test_feature_file)
    model = svm_load_model(model_path)
    p_label, p_acc, p_val = svm_predict(yt, xt, model)


    label_to_type = []
    with open(lable_to_type_path) as f:
        for line in f:
            tt = line.split(',')[1]
            label_to_type.append(tt)

    cnt = 0
    for item in p_label:
        # print('%d' % item, end=',')
        print(label_to_type[int(item)])

        cnt += 1
        if cnt % 8 == 0:
            print('')


if __name__ == "__main__":
    print('svm demo')
    # svm_data_demo()
    # train_svm_model()
    # svm_model_test()

    #使用抽取出切图特征文件训练出模型文件
    model_path='./train_data/svm_model_file'

    # train_file_name='./train_data/train_pix_feature_xy.txt'
    # svm_model_train(train_file_name, model_path)

    # 使用测试文件测试模型文件
    test_feature_file='./test_data/last_test_pix_xy_241.txt'
    lable_to_type_path = './train_data/label_to_type.txt'
    svm_model_test(test_feature_file, model_path, lable_to_type_path)



