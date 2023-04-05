from pynput.keyboard import Key
from pynput.keyboard import Listener
from pynput.mouse import Controller

mouse = Controller()


def keyboard_press(key):
    if hasattr(key, 'char') and getattr(key, 'char') == '\x17':  # Ctrl+W
        position = mouse.position  # 获取当前的鼠标位置
        print(f"position:{position}")


def keyboard_release(key):
    if key == Key.esc:  # 如果按下了ESC键,则结束监听
        return False


def main():
    print("按下Ctrl+W记录鼠标位置,按下ESC退出程序")
    with Listener(on_press=keyboard_press,
                  on_release=keyboard_release) as listener:
        listener.join()


if __name__ == '__main__':
    main()
