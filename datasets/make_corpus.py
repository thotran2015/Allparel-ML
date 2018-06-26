import os
import operator
import json
from pathlib import Path
from shutil import copyfile
import json
from bs4 import BeautifulSoup
import string

directory = './images/images'
filecount = 0


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
            curr_copy = ' '.join(curr_copy)
            n_words.append(curr_copy)
            del curr[0]
        curr.append(word)

    return n_words;

            


table = str.maketrans(' ', ' ', string.punctuation)
#table = string.maketrans(string.punctuation, ' '*len(string.punctuation))
def make_desc(json_data):
    color = ''
    try:
        color = json_data['colors'][0]['name']
    except:
        color = ''	
    #title = json_data['unbrandedName']
    desc = json_data['description']
    html = color + " " + desc
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text()

    #Data cleanup 
    #remove punctuation
    text = text.translate(table)
    # remove numbers
    text = ''.join(i for i in text if not i.isdigit())
    text = text.lower()
    return text

with open("corpus.txt", "a") as myfile:
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as f:
                try:
                    json_data = json.load(f)
                except:
                    continue
                myfile.write(filename + " " + make_desc(json_data) + '\n')
                if filecount % 10000 == 0:
                    print("filecount", filecount)
            filecount = filecount + 1
