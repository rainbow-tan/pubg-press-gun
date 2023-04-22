import os
import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import dxcam
from PIL import Image
from pynput import mouse, keyboard
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button

from img_utils import second_value_img_by_filename, d_hash, cmp_hash
from my_tk import TEXT_switch, TEXT_press_count, TEXT_base_k, TEXT_gun_head, create_win
from parts_utils import GunHead, GunHeadHashLike, GUN_HEAD_POINT


class MyGun:
    def show_switch(self):
        return f"开关:{'开启' if self.switch else '关闭'}"

    def show_press_count(self):
        return f"压枪次数:{self.press_count}"

    def show_base_k(self):
        return f"基础系数:{self.base_k},实际系数:{self.k}"

    def show_gun_head(self):
        return f"枪头:{self.gun_head}({self.gun_head_sim})"

    # ——————————————————————————————————————————————————————————————————
    def __init__(self):

        self.threshold = 40
        self.mouse_listener = mouse.Listener(on_click=self.mouse_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.keyboard_press)
        self.camera = dxcam.create()

        ###########################
        self.switch = False
        self.press_count = 0
        self.base_k = 1
        self.k = self.base_k
        self.gun_head = None
        self.gun_head_sim = 0
        self.head_limit_like = 0.9

        ############################
        self.left_mouse_down = False
        self.tab_down = False
        self.auto_identify = False
        ############################
        self.sleep_time = 0.05
        self.shape = (10, 10)

        self.init_text()
        self.src_heads = self.get_gun_head_d_hash()

    def init_text(self):
        TEXT_switch.set(self.show_switch())
        TEXT_press_count.set(self.show_press_count())
        TEXT_base_k.set(self.show_base_k())
        TEXT_gun_head.set(self.show_gun_head())

    def mouse_click(self, x, y, button, pressed):
        if pressed and button == Button.left:
            # print("鼠标左键按下")
            self.left_mouse_down = True
            self.press_count = 0
        elif not pressed and button == Button.left:
            # print("鼠标左键释放")
            self.left_mouse_down = False

    def keyboard_press(self, key):
        """
        蹲着0.83系数
        """
        add_k = 0.01
        if hasattr(key, 'vk') and key.vk == 97:  # 小键盘1
            # print("按下了小键盘1")
            self.switch = not self.switch
            TEXT_switch.set(self.show_switch())
            if not self.switch:
                self.press_count = 0
                TEXT_press_count.set(f"压枪次数:{self.press_count}")

                self.gun_head = None
                self.gun_head_sim = 0
                TEXT_gun_head.set(self.show_gun_head())

                self.k = self.base_k
                TEXT_base_k.set(self.show_base_k())
        elif key == KeyCode.from_char('+'):
            self.base_k += add_k
            self.base_k = round(self.base_k, 2)
            TEXT_base_k.set(self.show_base_k())
        elif key == KeyCode.from_char('-'):
            self.base_k -= add_k
            self.base_k = round(self.base_k, 2)
            TEXT_base_k.set(self.show_base_k())
        elif hasattr(key, 'vk') and key.vk == 105:  # 小键盘9
            pass
        elif hasattr(key, 'vk') and key.vk == 102:  # 小键盘6
            pass
        elif hasattr(key, 'vk') and key.vk == 103:  # 小键盘7
            print("手动结束了整个程序")
            os._exit(0)  # 强制所有线程都退出
        elif key == Key.tab:
            # print("按下了tab")
            if self.switch:
                self.tab_down = True

    def start_listener(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.mouse_listener.join()
        self.keyboard_listener.join()

    def re_gun_head(self, img_big):
        img_head = img_big.crop(GUN_HEAD_POINT)
        name = "img_head.png"
        name2 = "img_head_second_value.png"
        img_head.save(name)
        second_value_img_by_filename(name, name2, self.threshold)

        value = d_hash(cv2.imread(name2), self.shape)
        # print(f"枪头的hash:{value}")
        for i in self.src_heads:
            like = cmp_hash(i.hash_value, value)
            print(f"{i} -> {like}")
            if like >= self.head_limit_like:
                self.gun_head = i
                self.gun_head_sim = like
                self.k = round(self.base_k - i.k, 2)
                TEXT_gun_head.set(self.show_gun_head())
                TEXT_base_k.set(self.show_base_k())
                return


    def start_camera(self):
        self.camera.start()
        while True:
            if not self.switch:
                time.sleep(self.sleep_time)
                continue
            # print("===")

            if self.tab_down:
                print("按下了tab 需要识别配件信息")
                frame = self.camera.get_latest_frame()
                img_big = Image.fromarray(frame)
                self.re_gun_head(img_big)


                self.tab_down = False
                print("完成识别配件信息")
            else:
                time.sleep(self.sleep_time)

    def get_gun_head_d_hash(self):
        threshold = self.threshold

        data = [dict(path='parts/qiangtou/buchang.png', head=GunHead("补偿", 0.15)),
                dict(path='parts/qiangtou/xiaoyan.png', head=GunHead("消烟", 0.1)),
                dict(path='parts/qiangtou/xiaoying.png', head=GunHead("消音", 0)), ]
        heads = []
        for one in data:
            path = one['path']
            des = "src_head.png"
            second_value_img_by_filename(path, des, threshold)
            # print(type(img_pl))
            # img_cv = cv2.cvtColor(np.asarray(img_pl), cv2.COLOR_RGB2BGR)
            value = d_hash(cv2.imread(des), self.shape)
            # print(f"{os.path.basename(path)}的hash是:{value}")
            head = one['head']
            heads.append(GunHeadHashLike(head.name, head.k, value, 0))
        print("获取枪口hash完成")
        return heads


def main():
    executor = ThreadPoolExecutor(5)
    my = MyGun()
    executor.submit(my.start_listener)
    executor.submit(my.start_camera)
    create_win()


if __name__ == '__main__':
    main()
