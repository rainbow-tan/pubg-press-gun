import datetime

from pynput.keyboard import Key, Listener

from 工具.win截图 import printscreen


def keyboard_press(key):
    if hasattr(key, 'vk') and key.vk == 97:  # 小键盘1
        # pigu()
        # woba()
        qiangtou()


def keyboard_release(key):
    if key == Key.esc:  # 如果按下了ESC键,则结束监听
        return False


def main():
    with Listener(on_press=keyboard_press,
                  on_release=keyboard_release) as listener:
        listener.join()


INDEX = 1

width = 60
height = 60
y = 330


def qiangtou():
    global INDEX
    start = datetime.datetime.now()
    start_x = 1773
    printscreen(start_x, y, start_x + width, y + height, f"枪头/枪头{INDEX}.png")
    end = datetime.datetime.now()
    print(f"用时:{end - start}")
    INDEX += 1


def woba():
    global INDEX
    start = datetime.datetime.now()
    start_x = 1910
    printscreen(start_x, y, start_x + width, y + height, f"握把/握把{INDEX}.png")
    end = datetime.datetime.now()
    print(f"用时:{end - start}")
    INDEX += 1


def pigu():
    global INDEX
    start = datetime.datetime.now()
    start_x = 2340
    printscreen(start_x, y, start_x + width, y + height, f"屁股/屁股{INDEX}.png")
    end = datetime.datetime.now()
    print(f"用时:{end - start}")
    INDEX += 1


if __name__ == '__main__':
    main()
