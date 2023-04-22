class GunHead:
    def __init__(self,name,k):
        self.k=k
        self.name = name
    def __str__(self):
        return f"{self.name}({self.k})"
    def __repr__(self):
        return self.__str__()
class GunHeadHashLike(GunHead):
    def __init__(self, name, k,hash_value,like):
        super().__init__(name, k)
        self.hash_value = hash_value
        self.like = like
GUN_HEAD_POINT = (1782, 339, 1830, 385)  # 枪头位置