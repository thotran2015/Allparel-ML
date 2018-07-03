# https://github.com/keras-team/keras-applications/blob/master/keras_applications/vgg16.py
from base.base_model import BaseModel
from keras.models import Sequential
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.applications import vgg16
from keras.activations import sigmoid
from keras import backend as K
from keras.models import Model
from keras.utils import multi_gpu_model

# https://www.dlology.com/blog/how-to-multi-task-learning-with-missing-labels-in-keras/
def masked_loss_function(y_true, y_pred):
    mask = K.cast(K.not_equal(y_true, -1), K.floatx())
    return K.binary_crossentropy(y_true * mask, y_pred * mask)

class VGGModel(BaseModel):
    def __init__(self, config):
        super(VGGModel, self).__init__(config)
        self.num_classes = config.trainer.class_count
        self.batch_size = config.trainer.batch_size
        self.build_model()
    
    def build_model(self):
        self.model = vgg16.VGG16(include_top=True, weights=None, input_tensor=None, input_shape=None, pooling=None, classes=self.num_classes)
        self.model.compile(
              loss="categorical_crossentropy",
              optimizer=self.config.model.optimizer,
              metrics=['accuracy'])
        self.model = multi_gpu_model(self.model, gpus=3)
        
        self.model.summary()
        return self.model
