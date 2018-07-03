from base.base_data_loader import BaseDataLoader
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import cv2
import random
from keras import utils
import numpy as np
import os
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
def get_data_loader(config, train):
    if train:
        data_gen = ImageDataGenerator(
            rescale = 1./255,
            shear_range = 0.2, # random application of shearing
            zoom_range = 0.2,
            horizontal_flip = True
        )
        return data_gen.flow_from_directory(config.data_loader.train_dir, target_size = (224, 224), batch_size=config.trainer.batch_size)
    else:
        data_gen = ImageDataGenerator(
            rescale=1./255
        )
        return data_gen.flow_from_directory(config.data_loader.val_dir, target_size= (224, 224), batch_size=config.trainer.batch_size)
