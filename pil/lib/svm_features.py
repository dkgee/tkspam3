"""
将图片的像素信息，利用特征工程，降维 为 特征列表文件
"""
import os
from os.path import join

from PIL import Image


def get_feature(img):
    """
    获取指定图片的特征值,
    1. 按照每排的像素点,高度为10,然后宽度为6,总共16个维度
    1. 按照每排的像素点,高度为42,然后宽度为16,总共58个维度
    2. 计算每个维度（行 或者 列）上有效像素点的和

    :type img: Image
    :return:一个维度为16的列表
    """

    width, height = img.size
    pixel_cnt_list = []

    # width=16, height = 42
    for y in range(height):
        pix_cnt_x = 0
        for x in range(width):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_x += 1
        pixel_cnt_list.append(pix_cnt_x)

    for x in range(width):
        pix_cnt_y = 0
        for y in range(height):
            if img.getpixel((x, y)) == 0:  # 黑色点
                pix_cnt_y += 1
        pixel_cnt_list.append(pix_cnt_y)

    return pixel_cnt_list

def get_feature_in_four_box(img):
    """
    获取指定图片的特征值,
    1. 按照四方格平均值求向量，高度为42,然后宽度为16,总共21x8=168个维度
    :type img: Image
    :return:一个维度为16的列表
    """

    width, height = img.size
    pixel_cnt_list = []

    # width=16, height = 42
    for y in range(0, height, 2):
        if (y+1) < height:
            for x in range(0, width, 2):
                if (x+1) < width:
                    pix_cnt_1 = 0
                    pix_cnt_2 = 0
                    pix_cnt_3 = 0
                    pix_cnt_4 = 0
                    if img.getpixel((x, y)) == 0:
                        pix_cnt_1 = 4
                    if img.getpixel((x+1, y)) == 0:
                        pix_cnt_2 = 4
                    if img.getpixel((x, y+1)) == 0:
                        pix_cnt_3 = 4
                    if img.getpixel((x+1, y+1)) == 0:
                        pix_cnt_4 = 4
                    avg_pix = (pix_cnt_1 + pix_cnt_2 + pix_cnt_3 + pix_cnt_4)/4
                    pixel_cnt_list.append(int(avg_pix))
    return pixel_cnt_list

def convert_values_to_str(label, dif_list):
    """
    将特征值串转化为标准的svm输入向量:

    9 1:4 2:2 3:2 4:2 5:3 6:4 7:1 8:1 9:1 10:3 11:5 12:3 13:3 14:3 15:3 16:6

    最前面的是 标记值，后续是特征值
    :param label: int
    :param dif_list:
    :type dif_list: list[int]
    :return:
    """
    index = 1
    line = '%d' % label

    for item in dif_list:
        fmt = ' %d:%d' % (index, item)
        line += fmt
        index += 1

    # print(line)
    return line

def convert_imgs_to_feature_file(label, svm_feature_file, img_folder):
    """
    将某个目录下二进制图片文件，转换成特征文件
    :param dig:检查的数字
    :param svm_feature_file: svm的特征文件完整路径
    :type label:string
    :return:
    """
    file_list = os.listdir(img_folder)

    if len(file_list) == 0:
        return

    # sample_cnt = 0
    # right_cnt = 0
    for file in file_list:
        img = Image.open(img_folder + '/' + file)
        #dif_list = get_feature(img)
        dif_list = get_feature_in_four_box(img)
        # sample_cnt += 1
        line = convert_values_to_str(label, dif_list)
        svm_feature_file.write(line)
        svm_feature_file.write('\n')

# todo 在预测时有用， 后面会移走，不放在这里
def convert_feature_to_vector(feature_list):
    """
    :param feature_list:
    :return:
    """
    index = 1
    xt_vector = []
    feature_dict = {}
    for item in feature_list:
        feature_dict[index] = item
        index += 1
    xt_vector.append(feature_dict)
    return xt_vector

def get_svm_train_txt(cut_pic_folder, train_file_name):
    """
    获取 测试集 的像素特征文件。
    所有的数字的可能分类为36，分别放在以相应的字母命名的目录中
    :return:
    """
    svm_feature_file = open(train_file_name, 'w')
    for i in range(36):
        img_folder = join(cut_pic_folder, str(i))
        convert_imgs_to_feature_file(i, svm_feature_file, img_folder)

    # 不断地以追加的方式写入到同一个文件当中
    svm_feature_file.close()


def get_svm_test_txt(label, test_cut_pic_folder,test_feature_file):
    """
    获取 测试集 的像素特征文件
    :return:
    """
    test_file = open(test_feature_file, 'w')
    convert_imgs_to_feature_file(label, test_file, test_cut_pic_folder)
    test_file.close()



if __name__ == '__main__':
    print("start captcha app...")

    # img_path='../cut_pic/1-0.png'
    # img = Image.open(img_path)
    # pixel_cnt_list=get_feature(img)
    # line = convert_values_to_str(6, pixel_cnt_list)
    # print(line)

    #dig = 6
    #img_folder='./cut_pic'
    #feature_file='./train_pix_feature_tt.txt'
    #test_file = open(feature_file, 'w')
    #convert_imgs_to_feature_file(dig, test_file, img_folder)


    # 生成训练初始模型
    #cut_pic_folder = '../data/cut_pic/'
    #train_file_name='./train_data/train_pix_feature_xy.txt'
    #get_svm_train_txt(cut_pic_folder, train_file_name)

    # 生成测试模型
    label = 241
    test_cut_pic_folder='./cut_pic'
    test_feature_file='./test_data/last_test_pix_xy_241.txt'
    get_svm_test_txt(label, test_cut_pic_folder, test_feature_file)

