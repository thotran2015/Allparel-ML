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

    #model.load('/home/allparel/Allparel-ML/experiments/2018-08-10/pattern/checkpoints/pattern-70-1.32.hdf5')

    #model.load("/home/allparel/Allparel-ML/experiments/2018-08-12/color/checkpoints/color-99-1.38.hdf5")

    #model.load("/home/allparel/Allparel-ML/experiments/2018-08-08/material/checkpoints/material-36-1.69.hdf5")

    #model.load("/home/allparel/Allparel-ML/experiments/2018-12-09/baseline_crewneck/checkpoints/baseline_crewneck-66-0.43.hdf5")

    #model.load("/home/allparel/Allparel-ML/experiments/2018-12-09/turtleneck/checkpoints/turtleneck-61-0.37.hdf5")
    
    #model.load("/home/allparel/Allparel-ML/experiments/2018-12-10/crewneck/checkpoints/crewneck-52-0.32.hdf5")

    #model.load("/home/allparel/Allparel-ML/experiments/2018-12-11/baseline_turtleneck/checkpoints/baseline_turtleneck-12-0.73.hdf5")
    #model.load("/home/allparel/Allparel-ML/experiments/2018-12-11/matrix_turtleneck/checkpoints/matrix_turtleneck-12-0.67.hdf5")
    #model.load("/home/allparel/Allparel-ML/experiments/2018-12-11/baseline_turtleneck/checkpoints/baseline_turtleneck-12-0.73.hdf5")
    print('Create the trainer')
    trainer = ModelTrainer(model.model, training_generator, validation_generator, config)

    print('Start training the model.')
    trainer.train()


if __name__ == '__main__':
    main()
