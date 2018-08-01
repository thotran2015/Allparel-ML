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
import util

# Configuration
dress = category.Category('dress', config.dress_sub_categories, config.dress_replacements)
shirt = category.Category('shirt', config.shirt_sub_categories, config.shirt_replacements)
pant = category.Category('pant',   config.pant_sub_categories,  config.pant_replacements)
skirt = category.Category('skirt', config.skirt_sub_categories, config.skirt_replacements)
categories = [dress, shirt, pant, skirt] #categries to include
groups = [config.pattern] #, config.other_group]
group_names = ['pattern'] #, 'other_group']
labels = config.pattern # + config.other_group

data_directory = "/home/allparel/Allparel-ML/datasets/images/"
label_directory = "/home/allparel/Allparel-ML/datasets/"

train = '/home/allparel/Allparel-ML/datasets/train/'
validation = '/home/allparel/Allparel-ML/datasets/validation/'
 
class Record:
    def __init__(self, image_filename, title, description, category=None, pos=[], neg=[]):
        self.image_filename = image_filename
        self.description = description
        self.title = title
        self.category =  category
        self.pos = pos
        self.neg = neg
        if self.category is None:
            self.category = get_category(description)
        if self.category is not None:
            if self.pos is None:
                self.pos = positive_tags(self.category, self.description)
            if self.neg is None:
                self.neg = negative_tags(self.pos)

    def __hash__(self):
        return hash(self.image_filename)

    def __eq__(self, other):
        return self.image_filename == other.image_filename


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
    for t in tags:
        if t in labels:
            matched_tags.append(t)
    return list(set(matched_tags))

def negative_tags(tags):
    neg_tags = []
    for tag in tags:
        for group in groups:
            if tag in group:
                neg_tags = neg_tags + [g for g in group if g != tag]
    return list(set(neg_tags))

def get_category(line):
    for cat in categories:
        if cat.in_category(line):
            return cat
    return None
    
def process_line(filename, line):
    # Determine category for determining labels
    image_file = data_directory + filename.replace('.txt','.jpg')
    description = simplify_text(line["description"])
    title = simplify_text(line["title"])
    category = get_category(title)
    pos_tags = []
    neg_tags = []
    if category is not None:
        pos_tags = positive_tags(category, description)
        neg_tags = negative_tags(pos_tags)
   
    record = Record(image_file, title, description, category, pos_tags, neg_tags)
    return record

def write_image_labels(records):
    with open(os.path.join(label_directory,"image_labels.txt"), "w") as outfile:
        for record in records:
            pos_string = ''
            neg_string = ''
            for p in record.pos:
                pos_string = pos_string + ' ' + str(labels.index(p))
            for n in record.neg:
                neg_string = neg_string + ' ' + str(labels.index(n))
            line = record.filename + ',' + pos_string + ',' + neg_string + '\n'
            outfile.write(line)

def write_labels(num_records):
    print("total num", num_records)
    with open(os.path.join(label_directory,"labels.txt"), "w") as outfile:
        outfile.write(str(num_records) + '\n')
        for l in labels:
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
        for name in group_names: #BUG HERE
            directory = train + name
            if i % n == 0:
                directory = validation + '/' + name
            if not os.path.exists(directory):
                os.makedirs(directory)


            for index in range(len(labels)):
                img = record.filename.replace('.txt', '.jpg')
                sub_directory = directory + '/' + labels[index]
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if labels[index] in record.pos:
                    dst = sub_directory + '/' + img
                    src = data_directory + img
                    os.symlink(src, dst)
            i = i + 1

def read_image_labels():
    records = []
    with open("image_labels.txt", "r") as infile:
        for line in infile:
            line = line.replace("\n", "")
            line = line.split(",")
            pos = []
            neg = []
            for p in line[1].split():
                pos.append(int(p))
            for n in line[2].split():
                neg.append(int(n))
            record = Record(line[0], pos, neg)
            records.append(record)
    return records

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
    description = json_data['description'] + color
    description = BeautifulSoup(description, "lxml").get_text()
    #print(json_data)
    title = json_data['name'] 
    title = BeautifulSoup(title, "lxml").get_text()
    category = json_data["categories"][0]["fullName"]
    return {"title":title, "description":description, "category":category}

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
        r = {}
        r['image_file'] = record.image_filename
        r['title'] = record.title
        r['description'] = record.description
        r['category']= str(record.category)
        r['positive_tags'] = record.pos
        r['negative_tags'] = record.neg
        bulk.find({'image_file':record.image_filename}).update({ '$set': r})
        #r_all.append(r)
        #collection.update({'image_file':record.image_filename}, {'$set':r}, upsert=True)
        c = c + 1
        if c % 1000 == 0:
            printf("Written", c)
            
    #collection.insert_many(r_all)
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
        pos = None
        neg = None
        if 'category' in record:
            category = record['category']
        if 'positive_tags' in record:
            pos = record['positive_tags']
        if 'negative_tags' in record:
            neg = record['negative_tags']
        records.append(Record(image_file, description, category, pos, neg))
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


# Reading files
files = [f for f in os.listdir(data_directory) if f.endswith('.txt')]
print('processing files', len(files))
lines = p.map(process_file, files)
records = p.starmap(process_line, [(files[i], lines[i]) for i in range(len(files))])
print('done processing', len(records))
records = clean_records(records)
print('done cleaning', len(records))


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
#
#
## Write training files
#write_image_labels(records)
#write_labels(len(records))
#organize_image_data(records)
#print("done organizing data")

# Data stats
#count_per_label(records)
#tests.top_tags(lines)
