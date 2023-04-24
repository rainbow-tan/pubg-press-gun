import ctypes
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import dxcam
from PIL import Image
from pynput import mouse, keyboard
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button

from common import Gun, SCREEN_WIDTH, SCREEN_HEIGHT
from get_pixel import get_all_pixel
from img_utils import second_value_img_by_filename, d_hash, cmp_hash, pk_zishi
from my_tk import TEXT_switch, TEXT_press_count, TEXT_base_k, TEXT_gun_head, create_win, TEXT_gun_grip, TEXT_gun_tail, \
    TEXT_zishi
from parts_utils import GunHead, GunHeadHashLike, GUN_HEAD_POINT, GunGrip, GunGripHashLike, GUN_GRIP_POINT, \
    GunTailHashLike, GunTail, GUN_TAIL_POINT, ZISHI_POINT, ZiShi, ZiShiHashLike


class MyGun:
    def show_switch(self):
        return f"开关:{'开启' if self.switch else '关闭'}"

    def show_press_count(self):
        return f"压枪次数:{self.press_count}"

    def show_base_k(self):
        return f"基础系数:{self.base_k},实际系数:{self.k}"

    def show_gun_head(self):
        return f"枪头:{self.gun_head}({self.gun_head_sim})"
    def show_gun_grip(self):
        return f"握把:{self.gun_grip}({self.gun_grip_sim})"
    def show_gun_tail(self):
        return f"尾巴:{self.gun_tail}({self.gun_tail_sim})"
    def show_zishi(self):
        return f"姿势:{self.zishi}({self.zishi_sim})"

    # ——————————————————————————————————————————————————————————————————
    def __init__(self):


        self.threshold_zishi = 200
        self.threshold = 40

        self.lib,self.handler = self.load_usb()

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
        self.grip_limit_like = 0.9
        self.tail_limit_like = 0.9
        self.zishi_limit_like = 0.9
        self.gun_grip = None
        self.gun_tail= None
        self.zishi= None
        self.gun_grip_sim = 0
        self.zishi_sim = 0
        self.gun_tail_sim = 0
        self.gun_head_k=0
        self.gun_grip_k=0
        self.gun_tail_k=0
        self.zishi_k=0

        ############################
        self.left_mouse_down = False
        self.tab_down = False
        self.auto_identify = False
        ############################
        self.sleep_time = 0.05
        self.shape = (10, 10)

        self.gun_json_name = "berry"

        self.init_text()
        self.src_heads = self.get_gun_head_d_hash()
        self.src_grip = self.get_gun_grip_d_hash()
        self.src_tail= self.get_gun_tail_d_hash()
        self.src_zishi= self.get_zishi_d_hash()


        self.gun_data=self.load_data_by_name()

    def load_usb(self):
        # global LIB, HANDLER
        path = "box64.dll"
        path = os.path.join(os.path.dirname(__file__), path)
        lib = ctypes.windll.LoadLibrary(path)

        lib.M_Open.restype = ctypes.c_uint64
        ret = lib.M_Open(1)
        if ret in [-1, 18446744073709551615]:
            print('未检测到 USB 芯片!')
            os._exit(0)
        handler = ctypes.c_uint64(ret)
        result = lib.M_ResolutionUsed(handler, SCREEN_WIDTH, SCREEN_HEIGHT)
        if result != 0:
            print('设置分辨率失败!')
            os._exit(0)
        print("加载USB成功!!!")
        return lib,handler
    def load_data_by_name(self):
        with open(f"{self.gun_json_name}.json") as f:
            data = json.load(f)
        gun=Gun(self.gun_json_name,data['time'],data['press'])
        print(f"加载枪械数据完成:{gun}")
        return gun


    def init_text(self):
        TEXT_switch.set(self.show_switch())
        TEXT_press_count.set(self.show_press_count())
        TEXT_base_k.set(self.show_base_k())
        TEXT_gun_head.set(self.show_gun_head())
        TEXT_gun_grip.set(self.show_gun_grip())
        TEXT_gun_tail.set(self.show_gun_tail())
        TEXT_zishi.set(self.show_zishi())

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
                self.gun_head_k=0
                TEXT_gun_head.set(self.show_gun_head())

                self.gun_grip=None
                self.gun_grip_sim=0
                self.gun_grip_k=0
                TEXT_gun_grip.set(self.show_gun_grip())

                self.gun_tail = None
                self.gun_tail_sim = 0
                self.gun_tail_k = 0
                TEXT_gun_tail.set(self.show_gun_tail())

                self.zishi = None
                self.zishi_sim = 0
                self.zishi_k = 0
                TEXT_zishi.set(self.show_zishi())

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
                self.gun_head_k=i.k
                # self.k = round(self.k - i.k, 2)
                TEXT_gun_head.set(self.show_gun_head())
                # TEXT_base_k.set(self.show_base_k())
                return

    def re_gun_grip(self, img_big):
        img_head = img_big.crop(GUN_GRIP_POINT)
        name = "img_grip.png"
        name2 = "img_grip_second_value.png"
        img_head.save(name)
        second_value_img_by_filename(name, name2, self.threshold)

        value = d_hash(cv2.imread(name2), self.shape)
        # print(f"握把的hash:{value}")
        for i in self.src_grip:
            like = cmp_hash(i.hash_value, value)
            print(f"{i} -> {like}")
            if like >= self.grip_limit_like:
                self.gun_grip = i
                self.gun_grip_sim = like
                self.gun_grip_k=i.k
                # self.k = round(self.k - i.k, 2)
                TEXT_gun_grip.set(self.show_gun_grip())
                # TEXT_base_k.set(self.show_base_k())
                return
    def re_gun_tail(self, img_big):
        img_head = img_big.crop(GUN_TAIL_POINT)
        name = "img_tail.png"
        name2 = "img_tail_second_value.png"
        img_head.save(name)
        second_value_img_by_filename(name, name2, self.threshold)

        value = d_hash(cv2.imread(name2), self.shape)
        # print(f"握把的hash:{value}")
        for i in self.src_tail:
            like = cmp_hash(i.hash_value, value)
            print(f"{i} -> {like}")
            if like >= self.tail_limit_like:
                self.gun_tail = i
                self.gun_tail_sim = like
                self.gun_tail_k=i.k
                TEXT_gun_tail.set(self.show_gun_tail())
                return

    def re_zishi(self, img_big):
        img_head = img_big.crop(ZISHI_POINT)
        name = "img_zishi.png"
        name2 = "img_zishi_second_value.png"
        img_head.save(name)
        second_value_img_by_filename(name, name2, self.threshold_zishi)
        for i in self.src_zishi:
            like = pk_zishi(get_all_pixel(name2),i.hash_value)
            # print(f"{i.name}--{like}")
            if like >= self.zishi_limit_7like:
                self.zishi = i
                self.zishi_sim = like
                self.zishi_k = i.k
                TEXT_zishi.set(self.show_zishi())
                return True
        return False

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
                self.re_gun_grip(img_big)
                self.re_gun_tail(img_big)
                # self.re_zishi(img_big)

                self.k=round(self.base_k-self.gun_head_k-self.gun_grip_k-self.gun_tail_k,2)
                TEXT_base_k.set(self.show_base_k())

                self.tab_down = False
                print("完成识别配件信息")
            elif self.left_mouse_down:
                while True:
                    # print("需要识别姿势了！！！")
                    frame = self.camera.get_latest_frame()
                    img_big = Image.fromarray(frame)
                    ok=self.re_zishi(img_big)
                    # if ok:
                    #     print("站姿识别匹配")
                    # else:
                    #     print("站姿识别不匹配")
                    self.k = round(self.base_k - self.gun_head_k - self.gun_grip_k - self.gun_tail_k-self.zishi_k, 2)
                    TEXT_base_k.set(self.show_base_k())
                    if not self.left_mouse_down:
                        # print("不需要识别姿势了")
                        break
                    else:
                        time.sleep(self.sleep_time)



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

    def get_gun_grip_d_hash(self):
        threshold = self.threshold

        data = [dict(path='parts/woba/chuizhi.png', head=GunGrip("垂直", 0.15)),
                dict(path='parts/woba/hongwo.png', head=GunGrip("红握",0.08 )),
                dict(path='parts/woba/jiguang.png', head=GunGrip("激光", 0)),
                dict(path='parts/woba/muzhi.png', head=GunGrip("拇指", 0.08)),
                dict(path='parts/woba/qinxing.png', head=GunGrip("轻型", 0)),
                dict(path='parts/woba/sanjiao.png', head=GunGrip("三角", 0)),
                ]
        parts = []
        for one in data:
            path = one['path']
            des = "src_woba.png"
            second_value_img_by_filename(path, des, threshold)
            # print(type(img_pl))
            # img_cv = cv2.cvtColor(np.asarray(img_pl), cv2.COLOR_RGB2BGR)
            value = d_hash(cv2.imread(des), self.shape)
            # print(f"{os.path.basename(path)}的hash是:{value}")
            head = one['head']
            parts.append(GunGripHashLike(head.name, head.k, value, 0))
        print("获取握把hash完成")
        return parts
    def get_gun_tail_d_hash(self):
        threshold = self.threshold

        data = [dict(path='parts/pigu/putong.png', head=GunTail("普通", 0.05)),
                dict(path='parts/pigu/zhongxing.png', head=GunTail("重型",0.05 )),
                ]
        parts = []
        for one in data:
            path = one['path']
            des = "src_pigu.png"
            second_value_img_by_filename(path, des, threshold)
            value = d_hash(cv2.imread(des), self.shape)
            head = one['head']
            parts.append(GunTailHashLike(head.name, head.k, value, 0))
        print("获取屁股hash完成")
        return parts

    def get_zishi_d_hash(self):
        threshold = self.threshold_zishi

        data = [dict(path='parts/zishi/zhan.png', head=ZiShi("站", 0)),
                dict(path='parts/zishi/dun.png', head=ZiShi("蹲", 0.17)),
                dict(path='parts/zishi/pa.png', head=ZiShi("趴", 0)),
                ]
        parts = []
        for one in data:
            path = one['path']
            des = "src_zishi.png"
            second_value_img_by_filename(path, des, threshold)
            value = get_all_pixel(des)
            head = one['head']
            parts.append(ZiShiHashLike(head.name, head.k, value, 0))
        print("获取姿势hash完成")
        return parts

    def yaqiang(self):
        while True:
            if not self.switch:
                # print(f"开关状态:{SWITCH}, 无需压枪")
                time.sleep(self.sleep_time)
                continue
            # if EMPTY_BULLET:
            #     # print(f"子弹用完了, 不压枪")
            #     time.sleep(0.02)
            #     continue
            # print(f"开关状态:{SWITCH}， 需要压枪")
            if not self.left_mouse_down:
                # print("未按下鼠标左键, 无需压枪")
                time.sleep(self.sleep_time)
                continue
            # print("按下了鼠标左键, 需要压枪")
            # print(f"次数的下压册数:{PRESS_COUNT}")
            data = self.gun_data.s
            # data1 = berry.scar_data1
            # data2 = berry.scar_data2
            # data3 = berry.scar_data3
            # data4 = berry.scar_data4
            # data5 = berry.scar_data5
            # data6 = berry.scar_data6
            # data = data1 + data2 + data3 + data4 + data5 + data6
            for index, value in enumerate(data):
                if not self.left_mouse_down:
                    # print("压枪过程中, 释放了鼠标左键, 不应该再压了")
                    break
                # if EMPTY_BULLET:
                #     print("压枪过程中, 子弹打完了")
                    # break
                y_pixel = value
                # if index>20:
                # y_pixel = y_pixel + Y_NUMBER
                # y_pixel = y_pixel * K
                # y_pixel = int(y_pixel)
                y = int(y_pixel*self.k)
                # sleep_second = value[TIME_SLEEP]
                print(f"y:{y}")
                self.lib.M_MoveR2(self.handler, 0, y)
                time.sleep(self.gun_data.t)
                self.press_count += 1
def main():
    executor = ThreadPoolExecutor(5)
    my = MyGun()
    executor.submit(my.start_listener)
    executor.submit(my.start_camera)
    executor.submit(my.yaqiang)
    create_win()


if __name__ == '__main__':
    main()
