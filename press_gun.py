import ctypes
import os.path
import time
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, Label, Frame

import win32api
import win32con
from pynput import mouse, keyboard
from pynput.keyboard import KeyCode
from pynput.mouse import Button

import scar

SCREEN_WIDTH = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 屏幕高度
SCREEN_HEIGHT = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 屏幕宽度
##############################################################
Y_PIXEL = "Y_PIXEL"
TIME_SLEEP = "TIME_SLEEP"

LIB = None  # 加载的DLL
HANDLER = None  # 加载的句柄
MOUSE_LEFT_DOWN = False  # 鼠标左键按下
WORK = None  # 是否开启程序
Y_NUMBER = 2  # 下压的Y轴像素值
WIN = None  # tkinter界面
LABEL_WORK = None  # 显示是否开启程序
LABEL_Y_NUMBER = None  # 显示下压的Y轴像素值
PRESS_COUNT = 0  # 下压了多少次
LABEL_PRESS_COUNT = None  # 显示下压了多少次


def press_gun():
    global LIB, HANDLER, WORK, PRESS_COUNT, LABEL_PRESS_COUNT
    while True:
        if not WORK:
            # print(f"开关状态:{WORK}, 无需压枪")
            time.sleep(0.02)
            continue
        # print(f"开关状态:{WORK}， 需要压枪")
        if not MOUSE_LEFT_DOWN:
            # print("未按下鼠标左键, 无需压枪")
            time.sleep(0.02)
            continue
        # print("按下了鼠标左键, 需要压枪")
        print(f"次数的下压册数:{PRESS_COUNT}")
        data1 = scar.scar_data1
        data2 = scar.scar_data2
        data3 = scar.scar_data3
        data4 = scar.scar_data4
        data5 = scar.scar_data5
        data6 = scar.scar_data6
        data = data1 + data2 + data3 + data4 + data5 + data6
        for i in data:
            if not MOUSE_LEFT_DOWN:
                # print("压枪过程中, 释放了鼠标左键, 不应该再压了")
                break
            y_pixel = i[Y_PIXEL] + Y_NUMBER
            # y_pixel = Y_NUMBER
            sleep_second = i[TIME_SLEEP]
            LIB.M_MoveR2(HANDLER, 0, y_pixel)
            time.sleep(sleep_second)
            PRESS_COUNT += 1


def show_work():
    # return f'开启状态(1):{"开启" if WORK else "关闭"}'
    return f'开启状态:{"开启" if WORK else "关闭"}'


def show_press_count():
    return f'下压次数:{PRESS_COUNT}'


def show_press_pixel():
    # return f'压枪像素(+,-):{Y_NUMBER}'
    return f'压枪像素:{Y_NUMBER}'


def pack_components():
    global WIN, LABEL_WORK, LABEL_Y_NUMBER, LABEL_PRESS_COUNT
    bg = 'yellow'
    fg = 'red'

    frame = Frame(WIN, bg=bg)
    frame.pack(fill='both')
    font_name = '黑体'
    font_size = 16  # 字体大小
    font_choose = 'bold'
    side = 'left'
    LABEL_WORK = Label(
        master=frame,  # 父容器
        text=show_work(),  # 文本
        bg=bg,  # 背景颜色
        fg=fg,  # 文本颜色
        font=(font_name, font_size, font_choose),
    )
    LABEL_WORK.pack(side=side)

    LABEL_Y_NUMBER = Label(
        master=frame,  # 父容器
        text=show_press_pixel(),  # 文本
        bg=bg,  # 背景颜色
        fg=fg,  # 文本颜色
        font=(font_name, font_size, font_choose),
    )
    LABEL_Y_NUMBER.pack(side=side)

    LABEL_PRESS_COUNT = Label(
        master=frame,  # 父容器
        text=show_press_count(),  # 文本
        bg=bg,  # 背景颜色
        fg=fg,  # 文本颜色
        font=(font_name, font_size, font_choose),
    )
    LABEL_PRESS_COUNT.pack(side=side)


def create_win():
    global WIN
    WIN = Tk()
    width = 500  # tkinter宽度
    distance_middle = 500  # 中间偏右多少
    x = int((SCREEN_WIDTH - width) / 2) + distance_middle
    WIN.geometry(f'{width}x30+{x}+0')  # 设置宽度300,高度300,距离左上角x轴距离为500,y轴距离为100
    WIN.attributes('-alpha', 0.3)  # 设置透明度,数值是0-1之间的小数,包含0和1
    WIN.attributes("-fullscreen", False)  # 设置全屏
    WIN.attributes("-topmost", True)  # 设置窗体置于最顶层
    WIN.update()  # 刷新窗口,否则获取的宽度和高度不准
    WIN.overrideredirect(True)  # 去除窗口边框

    pack_components()

    WIN.mainloop()  # 显示窗口


def load_usb():
    global LIB, HANDLER
    path = "box64.dll"
    path = os.path.join(os.path.dirname(__file__), path)
    LIB = ctypes.windll.LoadLibrary(path)

    LIB.M_Open.restype = ctypes.c_uint64
    ret = LIB.M_Open(1)
    if ret in [-1, 18446744073709551615]:
        print('未检测到 USB 芯片!')
        print('未检测到 USB 芯片!')
        print('未检测到 USB 芯片!')
        os._exit(0)
    HANDLER = ctypes.c_uint64(ret)
    result = LIB.M_ResolutionUsed(HANDLER, SCREEN_WIDTH, SCREEN_HEIGHT)
    if result != 0:
        print('设置分辨率失败!')
        print('设置分辨率失败!')
        print('设置分辨率失败!')
        os._exit(0)
    print("加载USB成功!!!")
    print("加载USB成功!!!")
    print("加载USB成功!!!")


def mouse_click(x, y, button: Button, pressed):
    """
    鼠标点击事件
    :param x: 横坐标
    :param y: 纵坐标
    :param button: 按钮枚举对象 Button.left 鼠标左键 Button.right 鼠标右键 Button.middle 鼠标中键
    :param pressed: 按下或者是释放,按下是True释放是False
    :return:
    """
    global MOUSE_LEFT_DOWN, LABEL_PRESS_COUNT,PRESS_COUNT
    if pressed and button == Button.left:
        # print("鼠标左键按下")
        MOUSE_LEFT_DOWN = True
        PRESS_COUNT=0
    elif not pressed and button == Button.left:
        # print("鼠标左键释放")
        MOUSE_LEFT_DOWN = False
        LABEL_PRESS_COUNT.config(text=show_press_count())


def keyboard_press(key):
    global WORK, LABEL_WORK, Y_NUMBER, PRESS_COUNT
    if hasattr(key, 'vk') and key.vk == 97:  # 小键盘1
        WORK = not WORK
        LABEL_WORK.config(text=show_work())
        if not WORK:
            PRESS_COUNT = 0
            LABEL_PRESS_COUNT.config(text=show_press_count())
    elif key == KeyCode.from_char('+'):
        Y_NUMBER += 1
        # print(f"增加Y轴移动像素, 增加后:{Y_NUMBER}")
        LABEL_Y_NUMBER.config(text=show_press_pixel())
    elif key == KeyCode.from_char('-'):
        Y_NUMBER -= 1
        # print(f"降低Y轴移动像素, 降低后:{Y_NUMBER}")
        LABEL_Y_NUMBER.config(text=show_press_pixel())
    elif hasattr(key, 'vk') and key.vk == 103:  # 小键盘7
        os._exit(0)  # 强制所有线程都退出


def main():
    executor = ThreadPoolExecutor(max_workers=5)
    load_usb()

    executor.submit(press_gun, )
    executor.submit(create_win, )

    listener = mouse.Listener(on_click=mouse_click)
    listener.start()

    listener_keyboard = keyboard.Listener(on_press=keyboard_press)
    listener_keyboard.start()
    listener_keyboard.join()
    listener.join()


if __name__ == '__main__':
    """
    小键盘1是总开关 开启了才会压枪
    小键盘7是关闭整个程序 关闭了就整个退出了
    小键盘+-加减号是控制下拉像素点 每次增加或减少像素1
    """
    main()
