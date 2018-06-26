from comet_ml import Experiment
from base.base_trainer import BaseTrain
import os
from keras.callbacks import ModelCheckpoint, TensorBoard


class ModelTrainer(BaseTrain):
    def __init__(self, model, train_data_generator, val_data_generator, config):
        super(ModelTrainer, self).__init__(model, train_data_generator, val_data_generator, config)
        self.callbacks = []
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []
        self.init_callbacks()

    def init_callbacks(self):
        self.callbacks.append(
            ModelCheckpoint(
                filepath=os.path.join(self.config.callbacks.checkpoint_dir, '%s-{epoch:02d}-{val_loss:.2f}.hdf5' % self.config.exp.name),
                monitor=self.config.callbacks.checkpoint_monitor,
                mode=self.config.callbacks.checkpoint_mode,
                save_best_only=self.config.callbacks.checkpoint_save_best_only,
                save_weights_only=self.config.callbacks.checkpoint_save_weights_only,
                verbose=self.config.callbacks.checkpoint_verbose,
            )
        )

        self.callbacks.append(
            TensorBoard(
                log_dir=self.config.callbacks.tensorboard_log_dir,
                write_graph=self.config.callbacks.tensorboard_write_graph,
            )
        )

        if hasattr(self.config,"comet_api_key"):
            experiment = Experiment(api_key=self.config.comet_api_key)
            experiment.log_multiple_params(self.config.data_loader)
            experiment.log_multiple_params(self.config.model)
            experiment.log_multiple_params(self.config.trainer)
            self.callbacks.append(experiment.get_keras_callback())

    def train(self):
        history = self.model.fit_generator(
            generator = self.train_data_generator,
            validation_data = self.val_data_generator,
            epochs=self.config.trainer.num_epochs,
            verbose=self.config.trainer.verbose_training,
            use_multiprocessing=True,
            workers=6,
            callbacks=self.callbacks,
        )
        self.loss.extend(history.history['loss'])
        self.acc.extend(history.history['acc'])
        self.val_loss.extend(history.history['val_loss'])
        self.val_acc.extend(history.history['val_acc'])
