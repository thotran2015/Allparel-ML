class BaseTrain(object):
    def __init__(self, model, train_data_generator, val_data_generator, config):
        self.model = model
        self.train_data_generator = train_data_generator
        self.val_data_generator = val_data_generator
        self.config = config

    def train(self):
        raise NotImplementedError
