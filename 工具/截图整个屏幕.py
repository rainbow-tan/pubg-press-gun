import os
import uuid

import win32api
import win32con
from PIL import ImageGrab
from pynput.keyboard import Listener, Key

SCREEN_WIDTH = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 屏幕高度
SCREEN_HEIGHT = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 屏幕宽度


def keyboard_press(key):
    # 按下W直接截图
    if hasattr(key, 'char') and getattr(key, 'char') == '\x17':  # Ctrl+W
        screenshot()


def keyboard_release(key):
    if key == Key.esc:  # 如果按下了ESC键,则结束监听
        return False


def screenshot():
    img = ImageGrab.grab((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    path = os.path.abspath(f'{uuid.uuid4().hex}.png')
    img.save(path)
    print(f"保存图片到:{path}")


def main():
    print("按下Ctrl+W截取整个屏幕,按下ESC退出程序")
    with Listener(on_press=keyboard_press,
                  on_release=keyboard_release) as listener:
        listener.join()


if __name__ == '__main__':
    main()
