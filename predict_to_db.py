from comet_ml import Experiment 
from data_loader.dataloader import *
from models.vgg_model import VGGModel
from models.vgg_19_model import VGG19Model
from trainers.trainer import ModelTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
from pymongo import MongoClient
import numpy as np
import os
import math
import json
from multiprocessing import Pool

num_threads = 24

def update_db_records(config, records, filenames, labels):
    client = MongoClient('localhost', 27017)
    db = client.allparel
    collection = db.clothes
    bulk = collection.initialize_unordered_bulk_op()

    i = 0
    for index, prediction in enumerate(records):
        filename = os.path.basename(filenames[index])
        filepath = config.data_loader.full_image_dir + filename
        try:
            #db_record = collection.find_one({'image_file': filepath})
            #predicted_tags = db_record.get("predicted_tags", {})
            #predicted_confidences = db_record.get("predicted_confidences", {})
            
            cls = np.argmax(prediction, axis=-1)
            predicted_tags = [labels[cls]]
            predicted_confidences = []
            for label in labels:
                predicted_confidences.append((label, float(prediction[labels.index(label)])))

            #predicted_confidences = [float(prediction[cls])]
            #predicted_tags[config.predictor.tag_name] = labels[cls]
            #predicted_confidences[config.predictor.tag_name] = conf

            #update_dict = { 
            #        'allparel_tags': predicted_tags, 
            #        'predicted_confidences': predicted_confidences}
            #bulk.find({'image_file':filepath}).upsert().update({ '$set': update_dict})
            bulk.find({'image_file':filepath}).upsert().update({ 
                '$addToSet': {
                    'allparel_tags': {'$each': predicted_tags}, 
                    'predicted_confidences': {'$each': predicted_confidences}
                    }})
            i = i + 1
            if i % 10000 == 0:
                bulk.execute()
                bulk = collection.initialize_unordered_bulk_op()
        except Exception as e:
            print("Error failed: ", filepath, e)
            
    if i % 10000 != 0:
        bulk.execute()

def chunkify(records):
    chunk_records = []
    chunk_size = int(len(records)/num_threads)
    for i in range(num_threads - 1):
        chunk_records.append(records[i*chunk_size :(i+1)*chunk_size])
    chunk_records.append(records[(num_threads - 1)*chunk_size:])
    return chunk_records

def main():
    config_directory = 'configs/'

    # load checkpoints.json
    groups = [ 
           "neck",
           "pattern",
           "fit",
           "sleeve_length",
           "pant_shape",
           "color",
           "material",
           "shape",
           "skirt_length",
           "sleeve_shape",
           "style",
           "texture" 
       ]

    with open('/home/allparel/Allparel-ML/checkpoints.json') as f:
        checkpoints = json.load(f)

    for group in groups:
        checkpoint_file = checkpoints[group]
        config_file = group + "_config.json"
        config = process_config(config_directory + config_file)
        print("PREDICTING", config_file)

        generator = get_data_loader(config, False)
        labels = [""] * len(generator.class_indices)
        for label, index in generator.class_indices.items():
            labels[index] = label

        print('Create the data generator.')
        predict_generator = get_predict_data_loader(config)

        print('Create the model.')
        if config.model.name == "vgg_model.VGG19Model":
            print("using vgg19")
            model = VGG19Model(config)
        else:
            model = VGGModel(config)
        model.load(checkpoint_file)
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
        print("finished writing to database")

    print("finished")

if __name__ == '__main__':
    main()
