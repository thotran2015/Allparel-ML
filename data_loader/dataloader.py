from base.base_data_loader import BaseDataLoader
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
import cv2
import random
from keras import utils
import numpy as np

# https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly.html
class DataGenerator(utils.Sequence):
    'Generates data for Keras'
    def __init__(self, config, train):
        'Initialization'
        with open(config.data_loader.file_index) as f:
            file_index = f.read().splitlines()
        random.seed(42)
        random.shuffle(file_index)
        print("Loaded %d images", len(file_index))
        validationImages = int(config.trainer.validation_split * len(file_index))
        self.indexes = file_index[validationImages : ] if train else file_index[ : validationImages]
        self.class_count = config.trainer.class_count
        self.image_root = config.dataloader.images_path
        self.batch_size = config.trainer.batch_size
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.indexes) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Generate data
        X, y = self.__data_generation(indexes)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        random.shuffle(self.indexes)


    def __data_generation(self, indexes):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, 224, 224, 3))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, index in enumerate(indexes):
            imagePath = index.split(',')[0]
            positive = [int(x) for x in index.split(',')[1].split(' ')[1 : ]]
            negative = [int(x) for x in index.split(',')[2].split(' ')[1 : ]]

            image = cv2.imread(self.image_root + imagePath)
            image = cv2.resize(image, (224, 224))
            image = img_to_array(image)

            X[i,] = np.array(data, dtype="float") / 255.0
            
            label = [-1] * self.class_count;
            for i in range(self.class_count):
                if i in positive:
                    label[i] = 1
                elif i in negative:
                    label[i] = 0
            y[i] = np.array(label)

        return X, y
