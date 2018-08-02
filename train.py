from comet_ml import Experiment 
from data_loader.dataloader import get_data_loader
from models.vgg_model import VGGModel
from models.vgg_19_model import VGG19Model
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
    training_generator = get_data_loader(config, True)
    validation_generator = get_data_loader(config, False)

    print('Create the model.')
    if config.model.name == "vgg_model.VGG19Model":
        print("using vgg19")
        model = VGG19Model(config)
    else:
        model = VGGModel(config)

    # Load from previously trained 
    #model.load("/home/allparel/Allparel-ML/experiments/2018-07-02/vgg/checkpoints/vgg-20-0.93.hdf5")

    print('Create the trainer')
    trainer = ModelTrainer(model.model, training_generator, validation_generator, config)

    print('Start training the model.')
    trainer.train()


if __name__ == '__main__':
    main()
