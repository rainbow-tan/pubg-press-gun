from pynput.keyboard import Key
from pynput.keyboard import Listener
from pynput.mouse import Controller

mouse = Controller()


def keyboard_press(key):
    if hasattr(key, 'vk') and key.vk == 97:  # 小键盘1
        position = mouse.position  # 获取当前的鼠标位置
        print(f"position:{position}")


def keyboard_release(key):
    if key == Key.esc:  # 如果按下了ESC键,则结束监听
        return False


def main():
    with Listener(on_press=keyboard_press,
                  on_release=keyboard_release) as listener:
        listener.join()


if __name__ == '__main__':
    main()
