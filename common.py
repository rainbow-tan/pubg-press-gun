import win32api
import win32con

SCREEN_WIDTH = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 屏幕宽度
print(f"屏幕分辨率宽度:{SCREEN_WIDTH}")
SCREEN_HEIGHT = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 屏幕高度
print(f"屏幕分辨率高度:{SCREEN_HEIGHT}")

class Gun:
    def __init__(self, name:str, y_axis_pixels:list[int], fire_rate:float):
        self.name = name
        self.y_axis_pixels = y_axis_pixels
        self.fire_rate = fire_rate
    def __str__(self):
        return f"Gun({self.name})"

    def __repr__(self):
        return self.__str__()