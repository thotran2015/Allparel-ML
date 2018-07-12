from data_loader.dataloader import get_data_loader
from models.vgg_model import VGGModel
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
from keras.models import load_model
import cv2
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import numpy as np
from sklearn import metrics, classification_report

args = get_args()
config = process_config(args.config)

model = VGGModel(config)
model.load("/home/allparel/Allparel-ML/experiments/2018-07-03/vgg/checkpoints/vgg-26-0.82.hdf5")

generator = get_data_loader(config, False)

probabilities = model.predict_generator(generator, config.trainer.validation_steps)
val_preds = np.argmax(probabilities, axis=-1)
val_trues = generator.classes
cm = metrics.confusion_matrix(val_trues, val_preds)
print(cm)
print(classification_report(generator.classes, val_preds))
#print(probabilities)

#filename = "sweetheart.jpg"
filename = "/home/allparel/Allparel-ML/datasets/validation/neck/sweetheartneck/bariano-off-shoulder-sweetheart-sequin-maxi-dress.jpg"

X = np.empty((1, 224, 224, 3))
image = cv2.imread(filename)
image = cv2.resize(image, (224, 224))
image = img_to_array(image)
X[0,] = np.array(image, dtype="float") / 255.0

print(model.predict(X))