GUN_HEAD_POINT = (1782, 339, 1830, 385)  # 枪头位置
GUN_GRIP_POINT = (1917, 338, 1966, 384)  # 握把位置
GUN_TAIL_POINT = (2347, 337, 2394, 386)  # 屁股位置
ZISHI_POINT = (950, 1305, 990, 1370)#姿势位置

class GunHead:
    def __init__(self, name, k):
        self.k = k
        self.name = name

    def __str__(self):
        return f"{self.name}({self.k})"

    def __repr__(self):
        return self.__str__()


class GunHeadHashLike(GunHead):
    def __init__(self, name, k, hash_value, like):
        super().__init__(name, k)
        self.hash_value = hash_value
        self.like = like


class GunGrip:
    def __init__(self, name, k):
        self.k = k
        self.name = name

    def __str__(self):
        return f"{self.name}({self.k})"

    def __repr__(self):
        return self.__str__()


class GunGripHashLike(GunGrip):
    def __init__(self, name, k, hash_value, like):
        super().__init__(name, k)
        self.hash_value = hash_value
        self.like = like


class GunTail:
    def __init__(self, name, k):
        self.k = k
        self.name = name

    def __str__(self):
        return f"{self.name}({self.k})"

    def __repr__(self):
        return self.__str__()


class GunTailHashLike(GunTail):
    def __init__(self, name, k, hash_value, like):
        super().__init__(name, k)
        self.hash_value = hash_value
        self.like = like

class ZiShi:
    def __init__(self, name, k):
        self.k = k
        self.name = name

    def __str__(self):
        return f"{self.name}({self.k})"

    def __repr__(self):
        return self.__str__()


class ZiShiHashLike(GunTail):
    def __init__(self, name, k, hash_value, like):
        super().__init__(name, k)
        self.hash_value = hash_value
        self.like = like