from comet_ml import Experiment 
from data_loader.dataloader import DataGenerator
from models.vgg_model import VGGModel
from trainers.trainer import ModelTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args

def main():
    # capture the config path from the run arguments
    # then process the json configuration file
    args = get_args()
    config = process_config(args.config)
    
    # create the experiments dirs
    create_dirs([config.callbacks.tensorboard_log_dir, config.callbacks.checkpoint_dir])

    print('Create the data generator.')
    training_generator = DataGenerator(config, True)
    validation_generator = DataGenerator(config, False)

    print('Create the model.')
    model = VGGModel(config)

    print('Create the trainer')
    trainer = ModelTrainer(model.model, training_generator, validation_generator, config)

    print('Start training the model.')
    trainer.train()


if __name__ == '__main__':
    main()
