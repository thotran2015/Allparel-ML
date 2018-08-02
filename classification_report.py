from data_loader.dataloader import get_data_loader
from models.vgg_model import VGGModel
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
from keras.models import load_model
import cv2
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import numpy as np
from sklearn import metrics
import os, random, math

configFile="configs/length_config.json"
modelFile = "/home/allparel/Allparel-ML/experiments/2018-07-31/vgg/checkpoints/vgg-79-0.65.hdf5"
config = process_config(configFile)


model = VGGModel(config)
model.load(modelFile)

generator = get_data_loader(config, False)
batch_size = config.trainer.batch_size
steps = config.classification_report.steps
if config.classification_report.process_all:
    steps = math.ceil(len(generator.filenames) / batch_size)

probabilities = model.model.predict_generator(generator, steps, workers=6, use_multiprocessing=True, verbose=1)
val_preds = np.argmax(probabilities, axis=-1)

val_trues = [0] * len(val_preds)
generator = get_data_loader(config, False)
for i in range(steps):
    x = generator[i][1]
    for j in range(len(x)):
        val_trues[i * batch_size + j] = np.argmax(x[j], axis=-1)

labels = [""] * len(generator.class_indices)
for label, index in generator.class_indices.items():
    labels[index] = label

cm = metrics.confusion_matrix(val_trues, val_preds)
print(labels)
print(cm)
print(metrics.classification_report(val_trues, val_preds))