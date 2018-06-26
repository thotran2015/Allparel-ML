# https://github.com/keras-team/keras-applications/blob/master/keras_applications/vgg16.py
from base.base_model import BaseModel
from keras.models import Sequential
from keras.layers import Input, Dense, Conv2D, MaxPooling2D, Dropout, Flatten
from keras.applications import vgg16
from keras.activations import sigmoid
from keras import backend as K

# https://www.dlology.com/blog/how-to-multi-task-learning-with-missing-labels-in-keras/
def masked_loss_function(y_true, y_pred):
    mask = K.cast(K.not_equal(y_true, -1), K.floatx())
    return K.binary_crossentropy(y_true * mask, y_pred * mask)

class VGGModel(BaseModel):
    def __init__(self, config):
        super(VGGModel, self).__init__(config)
        self.build_model()
    
    def build_model(self):
        base_model = vgg16.VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
        base_model.layers[-1].activation=sigmoid
        self.model = Model(input = base_model.input, output = base_model.layers[-1])

        self.model.compile(
              loss=masked_loss_function,
              optimizer=self.config.model.optimizer,
              metrics=['accuracy'])
        
        self.model.summary()
        return self.model