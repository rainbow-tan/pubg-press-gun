import os

from PIL import Image
from rembg import remove


def traverse_folder(folder, only_first=False):
    folder = os.path.abspath(folder)
    all_files = []
    all_dirs = []
    if os.path.isdir(folder):
        for root, dirs, files in os.walk(folder):
            for one_file in files:
                all_files.append(os.path.join(root, one_file))  # 所有文件
            for one_dir in dirs:
                all_dirs.append(os.path.join(root, one_dir))  # 所有文件夹
            if only_first:
                break
    else:
        msg = 'Can not find folder:{} for traverse'.format(folder)
        print(msg)
    return all_dirs, all_files
def remove_bg(src, des):
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    if os.path.isfile(os.path.dirname(des)):
        raise Exception(f'目标文件夹是一个已存在的文件:{os.path.dirname(des)}')

    if not os.path.isdir(os.path.dirname(des)):
        os.makedirs(os.path.dirname(des))

    with open(src, 'rb') as i:
        with open(des, 'wb') as o:
            o.write(remove(i.read()))
    print(f"remove bg success, save to {des}")
    return des
def convert_to1(src, des):
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
def convert_toL(src, des):
    # 转为1模式 像素点不是1就是255 非黑即白
    src = os.path.abspath(src)
    des = os.path.abspath(des)
    if os.path.isfile(os.path.dirname(des)):
        raise Exception(f'目标文件夹是一个已存在的文件:{os.path.dirname(des)}')

    if not os.path.isdir(os.path.dirname(des)):
        os.makedirs(os.path.dirname(des))
    empire = Image.open(src)
    empire_1 = empire.convert('L')
    empire_1.save(des)
    print(f"convert success, save to {des}")
    return des