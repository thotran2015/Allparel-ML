from base.base_data_loader import BaseDataLoader
from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
import cv2
import random

class DataLoader(BaseDataLoader):
    def __init__(self, config):
        super(DataLoader, self).__init__(config)

        with open(config.data_loader.file_index) as f:
            file_index = f.read().splitlines()
        random.seed(42)
        random.shuffle(file_index)
        print("Loaded %d images", len(file_index))
        validationImages = config.trainer.validation_split * len(file_index)
        self.val_index = file_index[ : validationImages]
        self.train_index = file_index[validationImages : ]
        self.class_count = config.trainer.class_count
        self.image_root = config.dataloader.images_path
    
    def multiclass_flow_from_directory(file_index):
        def flow():
            random.shuffle(file_index)

            for index in file_index:
                imagePath = index.split(',')[0]
                positive = [int(x) for x in index.split(',')[1].split(' ')]
                negative = [int(x) for x in index.split(',')[2].split(' ')]

                image = cv2.imread(self.image_root + imagePath)
                image = cv2.resize(image, (224, 224))
                image = img_to_array(image)

                image = np.array(data, dtype="float") / 255.0
                
                label = [-1] * self.class_count;
                for i in range(self.class_count):
                    if i in positive:
                        label[i] = 1
                    elif i in negative:
                        label[i] = 0
                label = np.array(label)

                yield image, label
        return flow

    def get_train_data(self):
        return multiclass_flow_from_directory(self.train_index)

    def get_test_data(self):
        return multiclass_flow_from_directory(self.val_index)
