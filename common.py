import win32api
import win32con

SCREEN_WIDTH = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)  # 屏幕宽度
print(f"SCREEN_WIDTH:{SCREEN_WIDTH}")
SCREEN_HEIGHT = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)  # 屏幕高度
print(f"SCREEN_HEIGHT:{SCREEN_HEIGHT}")

class Gun:
    def __init__(self,name,t,s):
        self.name = name
        self.t = t
        self.s = s
    def __str__(self):
        return f"{self.name}({self.t})"

    def __repr__(self):
        return self.__str__()