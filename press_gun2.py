import ctypes
import os
import time
from concurrent.futures import ThreadPoolExecutor
from tkinter import Tk, Label

import cv2
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from pynput import mouse, keyboard
from pynput.keyboard import KeyCode, Key
from pynput.mouse import Button

SCREEN_WIDTH = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 屏幕高度
SCREEN_HEIGHT = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 屏幕宽度


def exit_all():
    os._exit(0)
class Parts:
    def __init__(self,name,sim,path,xishu):
        self.xishu = xishu
        self.name = name
        self.sim = sim
        self.path = path

class MyGun:
    # -------------------tk参数-------------------
    bg = 'yellow'
    fg = 'red'
    font_name = '黑体'
    font_size = 16  # 字体大小
    font_choose = 'bold'

    # -------------------tk显示-------------------
    def show_switch(self):
        return f"开关:{'开启' if self.switch else '关闭'}"

    def show_press_count(self):
        return f"压枪次数:{self.press_count}"

    def show_base_k(self):
        return f"基础系数:{self.base_k}"

    def show_qiangtou(self):
        return f"枪头:{self.qiangtou}({self.qiangtou_sim})"


    def __init__(self):

        self.switch = False  # 整个程序的开关
        self.switch_label = None

        self.handler = None
        self.lib = None

        self.tk_win = None
        self.tk_width = 800  # tkinter宽度
        self.tk_height = 30  # tk的高度
        self.tk_distance_middle = 500  # 中间偏右多少
        self.tk_alpha = 0.5  # 设置透明度,数值是0-1之间的小数,包含0和1

        self.base_k = 1  # 基础比例系数
        self.base_k_label = None

        self.mouse_listener = None  # 监听鼠标事件
        self.keyboard_listener = None  # 监听键盘事件
        self.left_mouse_down = False  # 鼠标左键按下
        self.tab_down = False  # tab按下

        self.press_count = 0  # 压枪的次数
        self.press_count_label = None

        self.parts_width = 60  # 配件的宽度
        self.parts_height = 60  # 配件的高度
        self.parts_start_y = 330  # 配件的起始坐标Y
        self.parts_qiangtou = 1773  # 枪头的起始坐标X
        self.parts_woba = 1910  # 握把的起始坐标X
        self.parts_weibo = 2340  # 尾巴的起始坐标X

        self.inta=0.05#等待时间间隔

        self.qiangtou=None
        self.qiangtou_label=None
        self.qiangtou_sim=0

        self.src_qiantous=[Parts("补偿",0,"src-parts/buchang.png",1),
                           Parts("消音",0,"src-parts/xiaoying.png",1),
                           Parts("消炎", 0, "src-parts/xiaoyan.png",1),
            ]


    def start_listen_mouse_keyboard(self):
        self.mouse_listener = mouse.Listener(on_click=self.mouse_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.keyboard_press)
        self.mouse_listener.start()
        print("开始监听鼠标事件")
        self.keyboard_listener.start()
        print("开始监听键盘事件")
        self.mouse_listener.join()
        self.keyboard_listener.join()

    def mouse_click(self, x, y, button, pressed):
        """
        鼠标点击事件
        :param x: 横坐标
        :param y: 纵坐标
        :param button: 按钮枚举对象 Button.left 鼠标左键 Button.right 鼠标右键 Button.middle 鼠标中键
        :param pressed: 按下或者是释放,按下是True释放是False
        :return:
        """
        if pressed and button == Button.left:
            # print("鼠标左键按下")
            self.left_mouse_down = True
            self.press_count = 0
        elif not pressed and button == Button.left:
            # print("鼠标左键释放")
            self.left_mouse_down = False
            self.press_count_label.config(text=self.show_press_count())

    def keyboard_press(self, key):
        """
        蹲着0.83系数

        :param key:
        :return:
        """
        add_k = 0.01
        if hasattr(key, 'vk') and key.vk == 97:  # 小键盘1
            # print("按下了小键盘1")
            self.switch = not self.switch
            self.switch_label.config(text=self.show_switch())
            if not self.switch:
                self.press_count_label.config(text=self.show_press_count())
        elif key == KeyCode.from_char('+'):
            self.base_k += add_k
            self.base_k = round(self.base_k, 2)
            self.base_k_label.config(text=self.show_base_k())
        elif key == KeyCode.from_char('-'):
            self.base_k -= add_k
            self.base_k = round(self.base_k, 2)
            self.base_k_label.config(text=self.show_base_k())
        elif hasattr(key, 'vk') and key.vk == 105:  # 小键盘9
            pass
        elif hasattr(key, 'vk') and key.vk == 102:  # 小键盘6
            pass
        elif hasattr(key, 'vk') and key.vk == 103:  # 小键盘7
            print("手动结束了整个程序")
            exit_all()  # 强制所有线程都退出
        elif key==Key.tab:
            # print("按下了tab")
            self.tab_down=True

    def printscreen(self,x1, y1, x2, y2, filename):
        try:
            hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
            # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
            hwndDC = win32gui.GetWindowDC(hwnd)
            # 根据窗口的DC获取mfcDC
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            # mfcDC创建可兼容的DC
            saveDC = mfcDC.CreateCompatibleDC()
            # 创建bigmap准备保存图片
            saveBitMap = win32ui.CreateBitmap()
            # 获取监控器信息
            # MoniterDev = win32api.EnumDisplayMonitors(None, None)
            # w = MoniterDev[0][2][2]
            # h = MoniterDev[0][2][3]
            # print w,h　　　#图片大小
            # 为bitmap开辟空间
            saveBitMap.CreateCompatibleBitmap(mfcDC, x2 - x1, y2 - y1)
            # 高度saveDC，将截图保存到saveBitmap中
            saveDC.SelectObject(saveBitMap)
            # 截取从(x1, y1)长宽为(x2 - x1, y2 - y1)的图片
            saveDC.BitBlt((0, 0), (x2 - x1, y2 - y1), mfcDC, (x1, y1), win32con.SRCCOPY)
            if not os.path.exists(os.path.dirname(os.path.abspath(filename))):
                os.makedirs(os.path.dirname(os.path.abspath(filename)))
            saveBitMap.SaveBitmapFile(saveDC, filename)
            print(f"printscreen success, save to:{filename}")
        except Exception as e:
            print('截图失败,失败原因:{}'.format(e))

    @staticmethod
    def to_model_1(src, threshold=30):
        img = Image.open(src)
        img_2 = img.convert("L")
        table = []
        for i in range(256):  # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        img_3 = img_2.point(table, "1")  # 图片二值化 使用table来设置二值化的规则
        img_3.save(src)

    def check_parts(self):
        while True:
            if not self.switch:
                time.sleep(self.inta)
                continue
            if not self.tab_down:
                time.sleep(self.inta)
                continue
            t1=time.perf_counter()
            filename = f"qiangtou/qiangtou.png"
            self.printscreen(self.parts_qiangtou,
                             self.parts_start_y,
                             self.parts_qiangtou + self.parts_width,
                             self.parts_start_y + self.parts_height,
                             filename)
            self.to_model_1(filename)
            # qt=Parts(None,None,None,None)
            max_s=0
            for src in self.src_qiantous:
                f="qiangout/q.png"
                self.to_model_1(src.path)
                ret = self.a_hash(filename, src.path)
                if ret>max_s:
                    max_s=ret
                    # qt.name=src.name
                    # qt.sim=ret
                    # qt.xishu=src.xishu
                    self.qiangtou_sim=max_s
                    self.qiangtou=src.name
            self.qiangtou_label.config(text=self.show_qiangtou())



            t2=time.perf_counter()
            print(f"用时:{t2-t1}")
            self.tab_down=False


    def load_usb(self):
        path = "box64.dll"
        lib = ctypes.windll.LoadLibrary(path)

        lib.M_Open.restype = ctypes.c_uint64
        ret = lib.M_Open(1)
        if ret in [-1, 18446744073709551615]:
            print('未检测到 USB 芯片!')
            exit_all()

        handler = ctypes.c_uint64(ret)
        result = lib.M_ResolutionUsed(handler, SCREEN_WIDTH, SCREEN_HEIGHT)
        if result != 0:
            print('设置分辨率失败!')
            exit_all()
        print("加载USB成功!!!")
        self.lib = lib
        self.handler = handler

    def create_win(self):
        win = Tk()
        width = self.tk_width
        distance_middle = self.tk_distance_middle
        x = int((SCREEN_WIDTH - width) / 2) + distance_middle
        win.geometry(f'{width}x{self.tk_height}+{x}+0')
        win.attributes('-alpha', self.tk_alpha)
        win.attributes("-fullscreen", False)  # 设置全屏
        win.attributes("-topmost", True)  # 设置窗体置于最顶层
        win.configure(bg=self.bg)  # 刷新窗口,否则获取的宽度和高度不准
        win.overrideredirect(True)  # 去除窗口边框
        self.tk_win = win
        print("创建了Tk窗口")

    def pack_label(self, text: str):
        assert text
        label = Label(
            master=self.tk_win,  # 父容器
            text=text,  # 文本
            bg=self.bg,  # 背景颜色
            fg=self.fg,  # 文本颜色
            font=(self.font_name, self.font_size, self.font_choose),
        )
        label.pack(side='left')
        return label

    def pack_components(self):
        assert self.tk_win
        self.switch_label = self.pack_label(self.show_switch())
        self.press_count_label = self.pack_label(self.show_press_count())
        self.base_k_label = self.pack_label(self.show_base_k())
        self.qiangtou_label = self.pack_label(self.show_qiangtou())
        print("放置了一些label组件")

    def start_win(self):
        assert self.tk_win
        print("启动了Tk窗口")
        self.tk_win.mainloop()

    @staticmethod
    def __a_hash(img):  # 均值哈希算法
        shape = (60, 60)
        img = cv2.resize(img, shape, interpolation=cv2.INTER_CUBIC)  # 缩放为shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
        s = 0  # s为像素和初值为0
        hash_str = ''  # hash_str为hash值初值为''
        for i in range(shape[0]):  # 遍历累加求像素和
            for j in range(shape[1]):
                s = s + gray[i, j]
        avg = s / (shape[0] * shape[1])  # 求平均灰度
        for i in range(shape[0]):  # 灰度大于平均值为1相反为0生成图片的hash值
            for j in range(shape[1]):
                if gray[i, j] > avg:
                    hash_str += '1'
                else:
                    hash_str += '0'
        return hash_str

    # Hash值对比
    @staticmethod
    def __cmp_hash(hash1, hash2, s):
        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1) != len(hash2):
            raise
        # 遍历判断
        for i in range(len(hash1)):
            # 不相等则n计数+1，n最终为相似度
            if hash1[i] == hash2[i]:
                n = n + 1
        return round(n / s, 3)

    def a_hash(self, img1, img2):
        # print("==")
        ret = self.__cmp_hash(self.__a_hash(cv2.imread(img1)), self.__a_hash(cv2.imread(img2)), 3600)
        print(f"a_hash:{img1} <---> {img2} ({ret})")
        return ret


def main():
    executor = ThreadPoolExecutor(max_workers=10)
    my = MyGun()

    my.create_win()
    my.pack_components()
    # executor.submit(my.check_parts)
    executor.submit(my.start_listen_mouse_keyboard)
    my.start_win()


if __name__ == '__main__':
    main()
