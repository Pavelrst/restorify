import os
from PIL import Image

def main():
    print('hi')

    mask_path = 'mask1.png'

    mask = Image.open(mask_path, 'r')

    target_path = 'target.JPG'

    target = Image.open(target_path, 'r')

    # res_img = Image.new('RGBA', (600, 320), (0, 0, 0, 0))

    target.paste(mask, (1000,1000), mask=mask)

    target.show()

    # text_img.paste(bg, (0, 0))
    # text_img.paste(ironman, (0, 0), mask=ironman)
    # text_img.save("ball.png", format="png")

main()

