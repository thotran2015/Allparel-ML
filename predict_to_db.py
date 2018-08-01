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
from multiprocessing import Pool

num_threads = 24

def update_db_records(config, records, filenames, labels):
    client = MongoClient('localhost', 27017)
    db = client.allparel
    collection = db.clothes
    bulk = collection.initialize_unordered_bulk_op()

    for index, prediction in enumerate(records):
        filename = os.path.basename(filenames[index])
        filepath = config.data_loader.full_image_dir + filename
        try:
            #db_record = collection.find_one({'image_file': filepath})
            #predicted_tags = db_record.get("predicted_tags", {})
            #predicted_confidences = db_record.get("predicted_confidences", {})
            
            cls = np.argmax(prediction, axis=-1)
            predicted_tags = [labels[cls]]
            predicted_confidences = [float(prediction[cls])]
            #predicted_tags[config.predictor.tag_name] = labels[cls]
            #predicted_confidences[config.predictor.tag_name] = conf

            update_dict = { 'allparel_tags': predicted_tags, 'predicted_confidences': predicted_confidences}
            bulk.find({'image_file':filepath}).update({ '$set': update_dict})
        except Exception as e:
            print("Error failed: ", filepath, e)
            
    bulk.execute()

def chunkify(records):
    chunk_records = []
    chunk_size = int(len(records)/num_threads)
    for i in range(num_threads - 1):
        chunk_records.append(records[i*chunk_size :(i+1)*chunk_size])
    chunk_records.append(records[(num_threads - 1)*chunk_size:])
    return chunk_records

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
        workers=10,
    )
    print ("finished generating predictions")

    predictions = predictions[ : len(predict_generator.filenames)]
    p = Pool(num_threads)
    predictions_chunked = chunkify(predictions)
    filenames_chunked = chunkify(predict_generator.filenames)
    p.starmap(update_db_records, [(config, predictions_chunked[i], filenames_chunked[i], labels) for i in range(len(predictions_chunked))])

    print("finished")
if __name__ == '__main__':
    main()
