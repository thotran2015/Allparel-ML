from comet_ml import Experiment 
from data_loader.dataloader import *
from models.vgg_model import VGGModel
from trainers.trainer import ModelTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
from pymongo import MongoClient
import numpy as np
import os
import math

def main():
    # capture the config path from the run arguments
    # then process the json configuration file
    args = get_args()
    config = process_config(args.config)

    generator = get_data_loader(config, False)
    labels = [""] * len(generator.class_indices)
    for label, index in generator.class_indices.items():
        labels[index] = label

    print('Create the data generator.')
    predict_generator = get_predict_data_loader(config)

    print('Create the model.')
    model = VGGModel(config)
    model.load("/home/allparel/Allparel-ML/experiments/2018-07-13/vgg/checkpoints/vgg-56-0.76.hdf5")
    
    steps = config.predictor.steps

    if config.predictor.process_all:
        steps = math.ceil(len(predict_generator.filenames) / config.predictor.batch_size)
    # Load from previously trained 
    print('Start Prediction')
    predictions = model.model.predict_generator(
        generator = predict_generator,
        steps = steps,
        use_multiprocessing=True,
        workers=6,
    )

    client = MongoClient('localhost', 27017)
    db = client.allparel
    collection = db.clothes
    bulk = collection.initialize_unordered_bulk_op()
    counter = 0
    for index, prediction in enumerate(predictions):
        if index >= len(predict_generator.filenames):
            break
        filename = os.path.basename(predict_generator.filenames[index])
        filepath = config.data_loader.full_image_dir + filename
        print(filepath)
        #db_record = collection.find_one({'image_file': filepath})
        #predicted_tags = db_record.get("predicted_tags", {})
        #predicted_confidences = db_record.get("predicted_confidences", {})
        
        cls = np.argmax(prediction, axis=-1)
        conf = prediction[cls]
        predicted_tags = [labels[cls]]
        predicted_confidences = [float(prediction[cls])]
        #predicted_tags[config.predictor.tag_name] = labels[cls]
        #predicted_confidences[config.predictor.tag_name] = conf

        update_dict = { 'allparel_tags': predicted_tags, 'predicted_confidences': predicted_confidences}
        bulk.find({'image_file':filepath}).update({ '$set': update_dict})
        counter = counter + 1
        if counter % 10 == 0:
            bulk.execute()
            bulk = db.testdata.initialize_ordered_bulk_op()
            print("COUNT: ", counter, "filename: ", 
                filename,
                "prediction: ", predicted_tags,
                "confidence: ", predicted_confidences
            )

        # update_dict = {'predicted_tags': predicted_tags, 'predicted_confidences': predicted_confidences}
        # collection.update(
        #     {'image_file':filepath}, 
        #     {'$set':update_dict}, 
        #     upsert=True)
    if counter % 1000 != 0:
        bulk.execute()

if __name__ == '__main__':
    main()
