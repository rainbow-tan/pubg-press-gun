import os

import cv2
from PIL import Image


def second_value_img_by_filename(src, des, threshold=150):
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    img = Image.open(src)
    img_2 = img.convert("L")

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    img_3 = img_2.point(table, "1")  # 图片二值化 使用table来设置二值化的规则
    if not os.path.exists(os.path.dirname(des)):
        os.makedirs(os.path.dirname(des))
    img_3.save(des)
    # print(f"二值化图像完成, src:{src}, des:{des}")

def second_value_img_memory(img:Image.Image, threshold=150):
    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return img.convert("L").point(table, "1")  # 图片二值化 使用table来设置二值化的规则
def cmp_hash(hash1, hash2, shape=(10, 10)):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n / (shape[0] * shape[1])


# 差值感知算法
def d_hash(img, shape=(10, 10)):
    # 缩放10*11
    img = cv2.resize(img, (shape[0] + 1, shape[1]))
    # 转换灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(shape[0]):
        for j in range(shape[1]):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str
