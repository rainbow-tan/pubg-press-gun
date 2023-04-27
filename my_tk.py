from tkinter import Tk, Label, StringVar

from common import SCREEN_WIDTH

win = Tk()
width = 1600  # tkinter宽度
height = 30  # tk的高度
distance_middle = 500  # 中间偏右多少
alpha = 0.5  # 设置透明度,数值是0-1之间的小数,包含0和1
bg = 'yellow'
fg = 'red'
font_name = '黑体'
font_size = 16  # 字体大小
font_choose = 'bold'

TEXT_switch = StringVar()
TEXT_press_count = StringVar()
TEXT_base_k = StringVar()
TEXT_gun_head = StringVar()
TEXT_auto_identify = StringVar()
TEXT_gun_grip= StringVar()
TEXT_gun_tail= StringVar()
TEXT_gesture= StringVar()


def create_win():
    x = int((SCREEN_WIDTH - width) / 2) + distance_middle
    win.geometry(f'{width}x{height}+{x}+0')
    win.attributes('-alpha', alpha)
    win.attributes("-fullscreen", False)  # 设置全屏
    win.attributes("-topmost", True)  # 设置窗体置于最顶层
    win.configure(bg=bg)  # 刷新窗口,否则获取的宽度和高度不准
    win.overrideredirect(True)  # 去除窗口边框
    create_label()
    print("创建了Tk窗口")
    win.mainloop()


def create_label():
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_switch).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_press_count).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_base_k).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_gun_head).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_auto_identify).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_gun_grip).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_gun_tail).pack(side='left')
    Label(master=win, bg=bg, fg=fg, font=(font_name, font_size, font_choose), textvariable=TEXT_gesture).pack(side='left')


if __name__ == '__main__':
    create_win()
