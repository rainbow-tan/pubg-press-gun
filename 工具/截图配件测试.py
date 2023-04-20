import datetime
import time

import dxcam
from PIL import Image
from pynput.keyboard import Key, Listener

from 工具.win截图 import printscreen


def keyboard_press(key):
    if hasattr(key, 'vk') and key.vk == 97:  # 小键盘1
        screenshot_parts()


def keyboard_release(key):
    if key == Key.esc:  # 如果按下了ESC键,则结束监听
        return False


def main():
    with Listener(on_press=keyboard_press,
                  on_release=keyboard_release) as listener:
        listener.join()


def screenshot_parts():
    t = datetime.datetime.now()
    box1 = (1773, 329, 1837, 392)
    box2 = (1908, 329, 1972, 394)
    box3 = (2055, 332, 2121, 392)
    box4 = (2341, 331, 2401, 394)
    box = [box1, box2, box3, box4]
    camera = dxcam.create()
    for index, region in enumerate(box):
        # printscreen(region[0],region[1],region[2],region[3],f"parts_{index + 1}.png")
        frame = camera.grab(region)
        img = Image.fromarray(frame)
        img.save(f"parts_{index + 1}1.png")
        time.sleep(0.05)
    t2 = datetime.datetime.now()
    print(f"screenshot_parts end, time:{t2 - t}")


if __name__ == '__main__':
    main()
