import os.path

from rembg import remove


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


def main():
    remove_bg('img/loading.png', 'img/loading_no_background.png')
    remove_bg('img/stop_flag.png', 'img/stop_flag_no_background.png')


if __name__ == '__main__':
    main()
