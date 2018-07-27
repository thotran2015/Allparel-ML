import json
import numpy as np
import os
import random
import re
import time
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from multiprocessing import Pool
from pymongo import MongoClient
import lxml
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import shutil
import cv2

data_directory = '/home/allparel/Allparel-ML/datasets/images/'


def download_image(image, filename):
    while True:
        filename = data_directory + filename
        try:
            headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
            req = Request(image,None,headers)
            resp = urlopen(req)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            img = cv2.imdecode(image, cv2.IMREAD_COLOR)
            height, width = img.shape[:2]
            scaling_factor = 1024.0 / max(height, width)
            img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
            cv2.imwrite(filename, img)
            break
        except Exception as e:
            print("download_image exception: ", filename, e)


def section(name):
    try:
        client = MongoClient('localhost', 27017)
        db = client.allparel
        collection = db.clothes
        bulk = collection.initialize_unordered_bulk_op()

        with open(name, "r") as fp:
            Urls = fp.read().split("\n")
        total = len(Urls)
        dname = name.split("//")[2]
        counter = 0
        for index, url in enumerate(Urls):
            try:
                if (url == ""):
                    print(dname + " Done.")
                    break
                #print(dname + ": " + str(index + 1) + "//" + str(total - 1))
                proxies_req = Request(url)
                ua = UserAgent()
                proxies_req.add_header('User-Agent', ua.random)
                html = urlopen(proxies_req).read().decode('utf8')
                soup = BeautifulSoup(html, "lxml")
                try:
                    title = soup.find('div', {'class': "text-paragraph"}).text
                except:
                    title = ""
                # print(title)
                try:
                    brand = soup.find('div', {'class': "heading-4 mb5"}).find('a').text
                except:
                    brand = ""
                try:
                    description = soup.find('div', {'class': "product-description text-paragraph mb0"}).text
                except:
                    description = ""
                try:
                    image = soup.find('div', {'class': "image-gallery-thumbnails image-gallery-thumbnails--vertical hidden-mobile"}).findAll('a')
                    # print(image)
                    images = [i.attrs['href'] for i in image]
                except:
                    try:
                        image = soup.findAll('a', {'class': "image-gallery-main-img-link image-gallery-main-img-link--vertical hidden-mobile"})
                        images = [i.attrs['href'] for i in image]
                    except Exception as e:
                        print(e)
                        images = []
                if(len(images) != 0):
                    # os.path.isfile(image_location)
                    filename = urlparse(images[0]).path
                    filename = os.path.basename(filename)
                    download_image(images[0], filename)
                    # REPLACE WITH MONGO CODE LATER
                    j = {'image_file': data_directory + filename, 'url': url, 'title': title.replace("\n", ''), 'brand': brand.replace("\n", ''),
                              'description': description.replace("\n", '')}
                    bulk.find({'image_file': data_directory + filename}).upsert().update({'$set':j})
                    counter = counter + 1

                if counter > 0 and counter % 1000 == 0:
                    bulk.execute()
                    bulk = db.testdata.initialize_ordered_bulk_op()
                    print("1000 ITEMS WRITTEN", filename)
            except Exception as e:
                print("error skipping url:", url, e)
        if counter > 0 and counter % 1000 != 0:
            bulk.execute()
    except Exception as e:
        print("error ended program", e, counter)

names = [
    "Lyst//Women//beachwear//beachwear.txt"
    ,"Lyst//Women//coats//coats.txt"
    ,"Lyst//Women//dresses//dresses.txt"
    ,"Lyst//Women//jeans//jeans.txt"
    ,"Lyst//Women//jumpsuits//jumpsuits.txt"
    ,"Lyst//Women//knitwear//knitwear.txt"
    ,"Lyst//Women//lingerie//lingerie.txt"
    ,"Lyst//Women//nightwear//nightwear.txt"
    ,"Lyst//Women//pants//pants.txt"
    ,"Lyst//Women//shorts//shorts.txt"
    ,"Lyst//Women//skirts//skirts.txt"
    ,"Lyst//Women//suits//suits.txt"
    ,"Lyst//Women//sweats//sweats.txt"
    ,"Lyst//Women//tops//tops.txt"
    ,"Lyst//Men//Beachwear//Beachwear.txt"
    ,"Lyst//Men//Beachwear//Beachwear.txt"
    ,"Lyst//Men//Coats//Coats.txt"
    ,"Lyst//Men//Jackets//Jackets.txt"
    ,"Lyst//Men//Jeans//Jeans.txt"
    ,"Lyst//Men//Knitwear//Knitwear.txt"
    ,"Lyst//Men//Nightwear//Nightwear.txt"
    ,"Lyst//Men//Pants//Pants.txt"
    ,"Lyst//Men//Shirts//Shirts.txt"
    ,"Lyst//Men//Shorts//Shorts.txt"
    ,"Lyst//Men//Suits//Suits.txt"
    ,"Lyst//Men//Sweats//Sweats.txt"
    ,"Lyst//Men//T//T.txt"
    ,"Lyst//Men//Underwear//Underwear.txt"]

num_threads = 24
p = Pool(num_threads)

p.map(section, names)

#section(names[0])
#outputs = [o for output in outputs for o in output]  #flatten
#with open("output.json", 'w') as outfile:
#    json.dump(outputs, outfile, indent=4, sort_keys=False)
