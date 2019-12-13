from os.path import join, exists
import os
from crack_gen import crackGenerator
from PIL import Image, ImageFilter, ImageEnhance
import random
from tqdm import tqdm

MAX_NUM_OF_CRACKS = 20

class dataPreProcessor():
    def __init__(self, in_path, out_path_data, out_path_true):
        self.in_path = in_path
        self.out_path_data = out_path_data
        self.out_path_true = out_path_true

    def pre_process(self):
        for filename in tqdm(os.listdir(self.in_path)):
            target = Image.open(join(self.in_path, filename), 'r')
            target = self.make_grayScale(target)
            target.save(join(self.out_path_true, filename))
            target = self.reduce_contrast(target)
            target = self.make_lighter(target)
            target = self.add_noise(target)
            target = self.add_cracks(target)
            target.save(join(self.out_path_data, filename))

    def make_grayScale(self, image):
        return image.convert('LA')

    def add_noise(self, image):
        return image

    def reduce_contrast(self, image):
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(0.5)

    def make_lighter(self, image):
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(1.2)

    def reduce_sharpness(self, image):
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(0.5)

    def add_cracks(self, image):
        cracker = crackGenerator(image)
        for _ in range(random.randint(5, MAX_NUM_OF_CRACKS)):
            cracker.generate_crack()
        return cracker.get_cracked_image()

