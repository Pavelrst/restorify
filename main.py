import os
from os.path import join, exists
from os import mkdir
from data_pre_proc import dataPreProcessor
from PIL import Image
import numpy as np

def main():
    # target_path = 'J:\\Celebs_dataset\\small_celeba_cracked\\label\\000001.png'
    # img = Image.open(target_path)
    #
    # kernelarr = np.array([[1,1,1,1,1],
    #                    [1,0,0,0,1],
    #                    [1,0,0,0,1],
    #                    [1,0,0,0,1],
    #                    [1,1,1,1,1]]) * 255
    #
    # kernel = Image.fromarray(kernelarr).convert("L")
    #
    # img.paste(kernel, (70, 70), mask=kernel)
    #
    # img.show()

    DATA_SET_FOLDER = 'J:\Celebs_dataset\small_celeba'
    OUT_DATA_FOLDER = 'J:\Celebs_dataset\small_celeba_cracked'
    if not exists(OUT_DATA_FOLDER):
        mkdir(OUT_DATA_FOLDER)

    out_data_path = join(OUT_DATA_FOLDER, 'data')
    out_label_path = join(OUT_DATA_FOLDER, 'label')
    if not exists(out_data_path):
        mkdir(out_data_path)
    if not exists(out_label_path):
        mkdir(out_label_path)

    preproc = dataPreProcessor(DATA_SET_FOLDER,
                               out_path_data=out_data_path,
                               out_path_true=out_label_path)

    preproc.pre_process()

main()

