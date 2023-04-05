from PIL import Image


def get_pixel(img: Image.Image):
    # rgb(255, 0, 0)
    size = img.size
    width = size[0]
    height = size[1]
    for i in range(width):
        for j in range(height):
            rgb = img.getpixel((i, j))
            if rgb == (255, 0, 0):
                return True
    return False


def main():
    ret = get_pixel(Image.open(r'D:\GitCode\pubg-press-gun\工具\无子弹.png'))
    print(f'has:{ret}')
    ret = get_pixel(Image.open(r'D:\GitCode\pubg-press-gun\工具\有子弹图片.png'))
    print(f'has:{ret}')


if __name__ == '__main__':
    main()
