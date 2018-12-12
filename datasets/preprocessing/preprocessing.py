import make_labels
import category
import config
import os
from multiprocessing import Pool

data_directory = "/home/allparel/Allparel-ML/datasets/images/"


# Configuration
dress = category.Category('dress', config.dress_sub_categories, config.dress_replacements)
shirt = category.Category('shirt', config.shirt_sub_categories, config.shirt_replacements)
pant = category.Category('pant',   config.pant_sub_categories,  config.pant_replacements)
skirt = category.Category('skirt', config.skirt_sub_categories, config.skirt_replacements)
categories = [dress, shirt, pant, skirt]
groups = [config.neck]

# Multiprocessing
num_threads = 24
p = Pool(num_threads)

#Scraping
print("no scraping")

# Reading files
print("Processing raw txt files...", data_directory)
files = [f for f in os.listdir(data_directory) if f.endswith('.txt')]
records = make_labels.clean_records(p.map(make_labels.process_file, files))

# Updating database
#print("Writing updates to database", len(records))
##make_labels.update_db_records(records)
#chunk_records = make_labels.chunkify(records)
#p.map(make_labels.update_db_records, chunk_records)
#print("Total written records", len(records))
#
## Reading from database
#print("Reading records from database...")
#records = make_labels.read_db_records()

# Write training files
print("Writing image labels...")
make_labels.write_image_labels(records)
#make_labels.write_labels(len(records))
print("Organizing image files into train and val...")
make_labels.organize_image_data(records)
print("done organizing data")

# Data stats
make_labels.count_per_label(records)
#tests.top_tags(lines)
