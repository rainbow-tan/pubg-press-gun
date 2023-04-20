import datetime

import cv2


def calcMethodsTimes(func):
    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        res = func(*args, **kwargs)
        end = datetime.datetime.now()
        print("methods: %s ,运行共计耗时: %s s" % (func.__name__, end - start))
        return res

    return inner


def __a_hash(img):  # 均值哈希算法
    shape = (8, 8)
    img = cv2.resize(img, shape, interpolation=cv2.INTER_CUBIC)  # 缩放为shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    s = 0  # s为像素和初值为0
    hash_str = ''  # hash_str为hash值初值为''
    for i in range(shape[0]):  # 遍历累加求像素和
        for j in range(shape[1]):
            s = s + gray[i, j]
    avg = s / (shape[0] * shape[1])  # 求平均灰度
    for i in range(shape[0]):  # 灰度大于平均值为1相反为0生成图片的hash值
        for j in range(shape[1]):
            if gray[i, j] > avg:
                hash_str += '1'
            else:
                hash_str += '0'
    return hash_str


def __d_hash(img):
    shape = (9, 8)
    # 缩放8*9
    img = cv2.resize(img, (shape[0], shape[1]), interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换灰度图
    hash_str = ''
    # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
    for i in range(shape[0] - 1):
        for j in range(shape[1]):
            if gray[i, j] > gray[i, j + 1]:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


# Hash值对比
def cmp_hash(hash1, hash2, s):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1) != len(hash2):
        raise
    # 遍历判断
    for i in range(len(hash1)):
        # 不相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return round(n / s, 3)


def a_hash(img1, img2):
    ret = cmp_hash(__a_hash(cv2.imread(img1)), __a_hash(cv2.imread(img2)), 64)
    print(f"a_hash:{img1} <---> {img2} ({ret})")


def d_hash(img1, img2):
    ret = cmp_hash(__d_hash(cv2.imread(img1)), __d_hash(cv2.imread(img2)), 64)
    print(f"d_hash:{img1} <---> {img2} ({ret})")


if __name__ == '__main__':
    a_hash('1.png', '2.png')
    d_hash('1.png', '2.png')

    a_hash('1.png', '3.png')
    d_hash('1.png', '3.png')
