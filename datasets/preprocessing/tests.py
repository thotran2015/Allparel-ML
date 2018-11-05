import os
import sys
import operator
import json
#from pathlib import Path
from shutil import copyfile
import json
import string
from enum import Enum
from multiprocessing import Pool
import config
import category
import util
import make_labels

# Script to find top tags
def top_tags(lines):
    label_counts = {}
    for line in lines:
        category = get_category(line)
        tags = get_tags(category, line)
        for label in tags:
            if label in label_counts:
                label_counts[label] = label_counts[label] + 1
            else:
                label_counts[label] = 0
    sorted_labels= sorted(label_counts.items(), key=operator.itemgetter(1), reverse=True)
    i = 0
    with open("top_tags.txt", "w") as labelfile:
        while i < 5000 and i < len(sorted_labels):
            labelfile.write(str(sorted_labels[i][0]) + ' ' + str(sorted_labels[i][1]) + '\n')
            i = i + 1



# Count overlapping images between classes (num positive)

# Count overlapping categories

num_threads = 24
p = Pool(num_threads)
files = [f for f in os.listdir(make_labels.data_directory) if f.endswith('.txt')]
print('done reading files')
files = files[:1000]
lines = p.map(process_file, files)
print('done processing')
top_tags(lines)

