import os.path

from PIL import Image


def convert(src, des):
    # 转为1模式 像素点不是1就是255 非黑即白
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    if os.path.isfile(os.path.dirname(des)):
        raise Exception(f'目标文件夹是一个已存在的文件:{os.path.dirname(des)}')

    if not os.path.isdir(os.path.dirname(des)):
        os.makedirs(os.path.dirname(des))
    empire = Image.open(src)
    empire_1 = empire.convert('1')
    empire_1.save(des)
    print(f"convert success, save to {des}")
    return des


def main():
    convert('img/loading.png', 'img/1/loading_1.png')
    convert('img/loading_no_background.png', 'img/1/loading_no_background_1.png')

    convert('img/stop_flag.png', 'img/1/stop_flag_1.png')
    convert('img/stop_flag_no_background.png', 'img/1/stop_flag_no_background_1.png')


if __name__ == '__main__':
    main()
