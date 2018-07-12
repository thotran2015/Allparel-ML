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
from multiprocessing import Pool
import config
import category
import util

data_directory = "/home/allparel/Allparel-ML/datasets/images/"
label_directory = "/home/allparel/Allparel-ML/datasets/"

class Record:
    def __init__(self, filename, pos, neg):
        self.filename = filename
        self.pos = pos
        self.neg = neg

    def __hash__(self):
        return hash(self.filename)

    def __eq__(self, other):
        return self.filename == other.filename

all_tags = []

dress_sub_categories = config.dress_sub_categories
shirt_sub_categories = config.shirt_sub_categories
pant_sub_categories = config.pant_sub_categories
skirt_sub_categories = config.skirt_sub_categories
dress_replacements = config.dress_replacements
shirt_replacements = config.shirt_replacements
pant_replacements = config.pant_replacements
skirt_replacements = config.skirt_replacements

dress = category.Category('dress', dress_sub_categories, dress_replacements)
shirt = category.Category('shirt', shirt_sub_categories, shirt_replacements)
pant = category.Category('pant',   pant_sub_categories,  pant_replacements)
skirt = category.Category('skirt', skirt_sub_categories, skirt_replacements)


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

def positive_tags(tags):
    matched_tags = []
    for t in tags:
        if t in config.labels:
            matched_tags.append(t)
    return list(set(matched_tags))

def negative_tags(tags):
    neg_tags = []
    for tag in tags:
        for group in config.groups:
            if tag in group:
                neg_tags = neg_tags + [g for g in group if g != tag]
    return list(set(neg_tags))

def process_line(filename, line):
    # Determine category for determining labels
    category = ''
    if dress.in_category(line):
        category = dress
    elif shirt.in_category(line):
        category = shirt
    elif pant.in_category(line):
        category = pant
    elif skirt.in_category(line):
        category = skirt
    else:
        # not included categories,e.g.shoes 
        #print("faled to categorize", line)
        return
    tags = get_tags(category, line)
    #all_tags = all_tags + tags
    pos_tags = positive_tags(tags)
    neg_tags = negative_tags(pos_tags)
   
    record = Record(filename, pos_tags, neg_tags)
    return record


def write_image_labels(records):
    with open(os.path.join(label_directory,"image_labels.txt"), "w") as outfile:
        for record in records:
            pos_string = ''
            neg_string = ''
            for p in record.pos:
                pos_string = pos_string + ' ' + str(config.labels.index(p))
            for n in record.neg:
                neg_string = neg_string + ' ' + str(config.labels.index(n))
            line = record.filename + ',' + pos_string + ',' + neg_string + '\n'
            outfile.write(line)

def write_labels(num_records):
    print("total num", num_records)
    with open(os.path.join(label_directory,"labels.txt"), "w") as outfile:
        outfile.write(str(num_records) + '\n')
        for l in config.labels:
            outfile.write(l + '\n')

def write_top_labels(label_counts):
    sorted_labels= sorted(label_counts.items(), key=operator.itemgetter(1), reverse=True)
    i = 0
    with open("top_tags.txt", "w") as labelfile:
        while i < 5000 and i < len(sorted_labels):
            labelfile.write(str(sorted_labels[i][0]) + ' ' + str(sorted_labels[i][1]) + '\n')
            i = i + 1

def write_all_tags(label_counts):
    with open("tags.txt", "w") as labelfile:
        for key in label_counts.keys():
            labelfile.write(str(key) + ' ' + str(label_counts[key]) + '\n')


def count_per_label(records):
    positive = [0] * len(config.labels)
    negative = [0] * len(config.labels)
    for record in records:
        pos = record.pos
        neg = record.neg
        for p in pos:
            positive[config.labels.index(p)] = positive[config.labels.index(p)] + 1
        for n in neg:
            negative[config.labels.index(n)] = negative[config.labels.index(n)] + 1
    for i in range(len(positive)):
        print(config.labels[i], "positive: ", positive[i], "negative: ", negative[i])

def organize_image_data(records):
    train = '/home/allparel/Allparel-ML/datasets/train/'
    validation = '/home/allparel/Allparel-ML/datasets/validation/'
    if not os.path.exists(train):
        os.makedirs(train)
    if not os.path.exists(validation):
        os.makedirs(validation)

    i = 0
    n = 10
    for record in records:
        for name in config.group_names: #BUG HERE
            directory = train + name
            if i % n == 0:
                directory = validation + '/' + name
            if not os.path.exists(directory):
                os.makedirs(directory)


            for index in range(len(config.labels)):
                img = record.filename.replace('.txt', '.jpg')
                sub_directory = directory + '/' + config.labels[index]
                if not os.path.exists(sub_directory):
                    os.makedirs(sub_directory)
                if config.labels[index] in record.pos:
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
    records = [record for record in records if len(record.pos) > 0 or len(record.neg) > 0]
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
    data = json_data['description'] + color
    text = BeautifulSoup(data, "lxml").get_text()
    text = text.translate(table)
    text = ''.join(i for i in text if not i.isdigit())
    text = text.lower()
    return text




num_threads = 24
p = Pool(num_threads)
files = [f for f in os.listdir(data_directory) if f.endswith('.txt')]
lines = p.map(process_file, files)
print("done processing files")
records = p.starmap(process_line, [(files[i], lines[i]) for i in range(len(files))])
#records = [y for x in records for y in x]
print("done processing lines")
records = [r for r in records if r is not None]
records = clean_records(records)
write_image_labels(records)
write_labels(len(records))
print("total written records", len(records))
organize_image_data(records)
print("done organizing data")
count_per_label(records)

#records = read_image_labels()
