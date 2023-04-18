from PIL import Image


def get_all_pixel(file):
    """
    获取所有的像素点的颜色
    :param file:
    :return:
    """
    img = Image.open(file)
    width = img.size[0]
    height = img.size[1]
    ret = list()
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            print(f"{x},{y} -----> {pixel}")
            ret.append(dict(x=x, y=y, pixel=pixel))
    return ret
if __name__ == '__main__':
    get_all_pixel('./c95f2b84194842d69e7923abf1a16e2e.png')