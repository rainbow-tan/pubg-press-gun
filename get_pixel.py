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
            # print(f"{x},{y} -----> {pixel}")
            # ret.append(dict(x=x, y=y, pixel=pixel))
            if pixel==255:
                pixel=1
            ret.append(pixel)
    return ret



