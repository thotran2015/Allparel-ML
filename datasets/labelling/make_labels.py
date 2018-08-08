from pymongo import MongoClient
from multiprocessing import Pool
import os
import sys
import operator
import json
#from pathlib import Path
from shutil import copyfile
import json
from bs4 import BeautifulSoup
import string
from enum import Enum
import config
import category
import record
import util

groups = [config.neck, config.sleeve_shape, config.sleeve_length, config.color, config.pattern, config.material, config.texture, config.style, config.fit, config.pant_shape, config.shape, config.length]

categories = [config.dress, config.shirt, config.pant, config.skirt] #categries to include
labels = []
for group in groups:
    labels = labels + group.labels
data_directory = "/home/allparel/Allparel-ML/datasets/images/"
label_directory = "/home/allparel/Allparel-ML/datasets/"

train = '/home/allparel/Allparel-ML/datasets/train/'
validation = '/home/allparel/Allparel-ML/datasets/validation/'

# Punctuation replacement table (for description cleaning)
table = str.maketrans(' ', ' ', string.punctuation)

#Current Approach:
#   * consider all 1-3 grams 
#   * lump together anything with 1/3 character diff
#   * count top frequencies
def n_gram(text, n):
    words = text.split();
    n_words = []
    curr = []
    for word in words:
        if len(curr) == n:
            curr_copy = list(curr)
            curr_copy = ''.join(curr_copy)
            n_words.append(curr_copy)
            del curr[0]
        curr.append(word)
    return n_words;

def get_tags(category, text):
    tags = []
    category.replace(tags)
    tags = tags + n_gram(text, 1) + n_gram(text, 2) + n_gram(text, 3)
    category.replace(tags)
    return list(set(tags))

def positive_tags(category, line):
    tags = get_tags(category, line)
    matched_tags = []
    for tag in tags:
        for group in groups:
            if tag in group.labels and group.has_category(category):
                matched_tags.append(tag)
    return list(set(matched_tags))

def negative_tags(tags):
    neg_tags = []
    for tag in tags:
        for group in groups:
            if tag in group.labels:
                neg_tags = neg_tags + [g for g in group.labels if g != tag]
    return list(set(neg_tags))

def get_category(line):
    for cat in categories:
        if cat.in_category(line):
            return cat
    return None

def write_image_labels(records):
    for group in groups:
        filename = group.name + "_image_labels.txt"
        num_records = 0
        with open(os.path.join(label_directory, filename), "w") as outfile:
            for record in records:
                pos_string = ''
                neg_string = ''
            
                for p in record.pos:
                    if p in group.labels:
                        pos_string = pos_string + ' ' + str(group.labels.index(p))
                for n in record.neg:
                    if n in group.labels:
                        neg_string = neg_string + ' ' + str(group.labels.index(n))

                if len(pos_string) > 0:
                    line = record.image_filename + ',' + pos_string + ',' + neg_string + '\n'
                    outfile.write(line)
                    num_records = num_records + 1
        label_filename = group.name + "_labels.txt"
        with open(os.path.join(label_directory, label_filename), "w") as outfile:
            outfile.write(str(num_records) + '\n')
            for l in group.labels:
                outfile.write(l + '\n')

def count_per_label(records):
    positive = [0] * len(labels)
    negative = [0] * len(labels)
    category_counts = [[0] * len(labels) for i in range(len(categories))]
    for record in records:
        pos = record.pos
        neg = record.neg
        for p in pos:
            index = labels.index(p)
            positive[index] = positive[index] + 1
            category_index = categories.index(record.category)
            category_counts[category_index][index] = category_counts[category_index][index] + 1
        for n in neg:
            negative[labels.index(n)] = negative[labels.index(n)] + 1
    print("LABELS")
    for i in range(len(positive)):
        print(labels[i])
    print("POSITIVE COUNTS")
    for i in range(len(positive)):
        print(positive[i])
    print("CATEGORY COUNTS")
    for i in range(len(categories)):
        print(categories[i].category)
        for j in range(len(positive)):
            print(category_counts[i][j])

    for i in range(len(positive)):
        print(labels[i], "positive: ", positive[i], "negative: ", negative[i])

def organize_image_data(records):
    if not os.path.exists(train):
        os.makedirs(train)
    if not os.path.exists(validation):
        os.makedirs(validation)

    i = 0
    n = 10
    for record in records:
        for group in groups: #BUG HERE
            directory = train + group.name
            if i % n == 0:
                directory = validation + '/' + group.name
            if not os.path.exists(directory):
                os.makedirs(directory)

            for label in group.labels:
                img = os.path.basename(record.image_filename)
                sub_directory = directory + '/' + label
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if label in record.pos:
                    dst = sub_directory + '/' + img
                    src = data_directory + img
                    if not os.path.lexists(dst):
                        os.symlink(src, dst)
                    #except Exception as e:
                        
        i = i + 1


def clean_records(records):
    records = list(set(records))
    #records = [record for record in records if record is not None and (len(record.pos) > 0 or len(record.neg) > 0)]

    records = [record for record in records if record is not None]
    return records

def process_file(filename):
    with open(os.path.join(data_directory, filename), 'r') as f:
        json_data = json.load(f)
    table = str.maketrans(' ', ' ', string.punctuation)
    # Get color
    try:
        color = json_data['colors'][0]['name']
    except:
        color = ''
    
    image_filename = data_directory + filename.replace('.txt','.jpg')
    description = json_data['description'] + color
    description = BeautifulSoup(description, "lxml").get_text()
    title = json_data['name'] 
    title = BeautifulSoup(title, "lxml").get_text()
    raw_category = json_data["categories"][0]["fullName"]
    product_url = json_data['clickUrl']
    #category = get_category(title)
    category = get_category(simplify_text(raw_category))
    
    if category is None:
        return 
    pos = positive_tags(category, simplify_text(description))
    neg = negative_tags(pos)

    return record.Record(image_filename, title, description, product_url, raw_category, category, pos, neg)

#def process_line(filename, line):
#    # Determine category for determining labels
#    image_file = data_directory + filename.replace('.txt','.jpg')
#    description = simplify_text(line["description"])
#    title = simplify_text(line["title"])
#    category = line["category"]
#    old = simplify_text(line["category"])
#    #category = get_category(title)
#    category = get_category(simplify_text(category))
#    if category is None:
#        return 
#    pos_tags = positive_tags(category, description)
#    neg_tags = negative_tags(pos_tags)
#    record = record.Record(image_file, title, description, category, pos_tags, neg_tags)
#    return record



def simplify_text(text):
    text = text.translate(table)
    text = ''.join(i for i in text if not i.isdigit())
    text = text.lower()
    return text


###############################################################
#  DATABASE METHODS
###############################################################

def write_to_db(lines): # add url later
    all_items = []
    image_filenames = [os.path.join(data_directory, f) for f in os.listdir(data_directory) if f.endswith('.jpg')]
    for i in range(len(lines)):
        line = lines[i]
        image_file = image_filenames[i]
        collection.update({'image_file':image_file}, {"$set": {'description':line}}, upsert=True)
    print("wrote lines", len(lines))

def update_db_records(records):

    client = MongoClient('localhost', 27017)
    db = client.allparel
    collection = db.clothes
    bulk = collection.initialize_unordered_bulk_op()

    r_all = []
    c = 0
    for record in records:
        bulk.find({'image_file':record.image_filename}).upsert().update({ '$set': record.dict()})
        c = c + 1
        if c % 1000 == 0:
            print("Written", c)
            
    bulk.execute()

def read_db_records():
    client = MongoClient('localhost', 27017)
    db = client.allparel
    collection = db.clothes
    db_records = collection.find()

    records = []
    for record in db_records:
        image_file = record['image_file']
        description = record['description']
        
        category = None
        pos = []
        neg = []
        title = None
        if 'title' in record:
            title = record['title']
        if 'category' in record:
            category = record['category']
        if 'positive_tags' in record:
            pos = record['positive_tags']
        if 'negative_tags' in record:
            neg = record['negative_tags']
        records.append(record.Record(image_file, title, description, category, pos, neg))
    return records

def chunkify(records):
    chunk_records = []
    chunk_size = int(len(records)/num_threads)
    for i in range(num_threads - 1):
        chunk_records.append(records[i*chunk_size :(i+1)*chunk_size])
    chunk_records.append(records[(num_threads - 1)*chunk_size:])
    return chunk_records


# Multiprocessing
num_threads = 24
p = Pool(num_threads)


## Reading files
files = [f for f in os.listdir(data_directory) if f.endswith('.txt')]
print('processing files', len(files))
records = p.map(process_file, files)
#records = p.starmap(process_line, [(files[i], lines[i]) for i in range(len(files))])
print('done processing', len(records))
records = clean_records(records)
print('done cleaning', len(records))
#
#
# Updating database
chunk_records = chunkify(records)
total_count = 0
for c in chunk_records:
    total_count = total_count + len(c)
if total_count != len(records):
    print("CHUNK ERROR", total_count)
    sys.exit()
p.map(update_db_records, chunk_records)
print("total written records", len(records))

## Reading from database
#records = read_db_records()
#print('done reading records')


# Write training files
write_image_labels(records)
print('done writing labels')
organize_image_data(records)
print("done organizing data")

# Data stats
#count_per_label(records)
#tests.top_tags(lines)
