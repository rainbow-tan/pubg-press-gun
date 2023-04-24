from PIL import Image


def get_second_img_pixel(file:str):
    #获取二值图片的像素列表 二值图片像素是0和255
    img = Image.open(file)
    width = img.size[0]
    height = img.size[1]
    ret = list()
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            if pixel==255:
                pixel=1
            ret.append(pixel)
    return ret



