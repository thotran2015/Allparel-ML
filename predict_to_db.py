from comet_ml import Experiment 
from data_loader.dataloader import get_predict_data_loader
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

    print('Create the data generator.')
    predict_generator = get_predict_data_loader(config)

    print('Create the model.')
    model = VGGModel(config)
    model.load("/home/allparel/Allparel-ML/experiments/2018-07-13/vgg/checkpoints/vgg-56-0.76.hdf5")
    
    # Load from previously trained 
    print('Start Prediction')
    predictions = model.model.predict_generator(
        generator = predict_generator,
        steps = config.predictor.steps,
        use_multiprocessing=True,
        workers=6,
    )

    for index, prediction in enumerate(predictions):
        print("filename: ", 
            predict_generator.filenames[index],
            "prediction: ", prediction)

if __name__ == '__main__':
    main()
