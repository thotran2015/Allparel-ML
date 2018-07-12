import requests
import json
from multiprocessing import Pool
import urllib.request
import os.path
from functools import partial
from fake_useragent import UserAgent
import cv2
import time
import numpy as np

data_directory = "../images/"
labels = [
   #"vneck", 
   #"v neck",
   #"crewneck", 
   #"scoopneck", 
   "sweetheart neck",
   "sweetheart", 
   #"turtleneck", 
   #"highneck", 
   #"high neck", 
   #"roundneck",
   #"round neck", 
   #"offtheshoulder",
   #"off the shoulder",
   #"collar"
]

error = "errorCode"
categories = [
    'jeans',
    'dresses',
    'womens-intimates',
    'jackets',
    'womens-outerwear',
    'womens-pants',
    'shorts',
    'skirts',
    'sweaters',
    'swimsuits',
    'sweatshirts',
    'womens-tops',
    'womens-suits',
    'bridal',
    'maternity-clothes',
    'petites',
    'plus-sizes',
    'teen-girls-clothes',
    'womens-clothes',
    'womens-shoes',
    'boots',
    'evening-shoes',
    'flats',
    'mules-and-clogs',
    'platforms',
    'pumps',
    'sandals',
    'womens-sneakers',
    'wedges',
    'mens-shoes',
    'mens-boots',
    'mens-sandals',
    'mens-lace-up-shoes',
    'mens-slip-ons-shoes',
    'mens-sneakers',
    'girls-shoes',
    'boys-shoes',
    'backpacks',
    'clutches',
    'hobo-bags',
    'satchels',
    'shoulder-bags',
    'tote-bags',
    'wallets',
    'handbags',
    'mens-bags',
    'mens-messenger-bags',
    'mens-tote-bags',
    'mens-business-bags',
    'mens-backpacks',
    'mens-sports-bags'
    'womens-accessories',
    'belts',
    'womens-eyewear',
    'gloves',
    'hats',
    'jewelry',
    'scarves',
    'womens-tech-accessories',
    'mens-accessories',
    'mens-belts',
    'mens-eyewear',
    'mens-gloves',
    'mens-hats',
    'mens-scarves',
    'mens-tech-accessories',
    'mens-wallets',
    'mens-clothes',
    'mens-athletic',
    'mens-bags',
    'mens-jeans',
    'mens-outerwear',
    'mens-pants',
    'mens-shirts',
    'mens-shorts',
    'mens-shoes',
    'mens-suits',
    'mens-sweaters',
    'mens-sweatshirts',
    'mens-swimsuits',
    'mens-ties',
    'girls-dresses',
    'girls-outerwear',
    'girls-pants',
    'girls-shoes',
    'girls-skirts',
    'girls-tops',
    'girls',
    'boys-outerwear',
    'boys-pants',
    'boys-shoes',
    'boys-shorts',
    'boys-sweaters',
    'boys-tops',
    'boys'
]

sorts = [
    'PriceLoHi',
    'PriceHiLo',
    'Popular',
    'Favorite',
    'Recency'
]


def download_image(image, filename):
    filename = data_directory + filename + ".jpg"
    try:
        #urllib.request.urlretrieve(image, filename)
        resp = urllib.request.urlopen(image)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
        height, width = img.shape[:2]
        scaling_factor = 1024.0 / max(height, width)
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        cv2.imwrite(filename, img)
    except Exception as e:
        print("download_image exception: ", image, str(e))

def scrape_offset(category, sort, is_search, label, offset):
    ua = UserAgent()
    header = {'User-Agent': str(ua.chrome)}
    if is_search:
        print(category, sort, offset, is_search, label)
        url = "https://www.shopstyle.com/api/v2/site/search?abbreviatedCategoryHistogram=true&cat=" + category + "&device=desktop&filters=Size%2CColor%2CCategory%2CTopRetailer%2CTopBrand%2CHeelHeight&fts=" + label + "&includeLooks=true&includeProducts=true&includeSavedQueryId=true&limit=40&locales=all&maxNumFilters=1000&maxQuickFilters=30&numLooks=20&offset=" + str(offset) + "&numSponsoredProducts=10&pid=shopstyle&prevCat=cocktail-dresses&productScore=" + sort + "&quickFilterTypes=brand&quickFilterTypes=color&quickFilterTypes=fts&url=%2Fbrowse%2Fdresses&useElasticsearch=true&view=angular2"
    else:
        url = 'https://www.shopstyle.com/api/v2/products?cat=' + category + '&device=desktop&includeLooks=true&includeProducts=true&includeSavedQueryId=true&limit=1000&locales=all&maxNumFilters=1000&numLooks=20&offset=' + str(offset) + '&pid=shopstyle&prevCat=mens-shirts&productScore=' + sort + '&url=%2Fbrowse%2F' + category + '&view=angular'

    if offset % 1000 == 0:
        print('SORT: ', sort, 'CATEGORY: ', category, ' OFFSET ', offset)

    try:
        response = requests.get(url, headers=header)
        json_data = json.loads(response.text)
        #json_data = json.load(json_data)
    except Exception as e:
        print("Json load eception", str(e), url)
        return

    if error in json_data and json_data["errorCode"] == 400:
        print('Error')
    #if (len(json_data["products"]) < 50):
    #    print ("short list", len(json_data["products"]))
    #    print(url)
    if 'products' not in json_data:
        print(url)
        print(json_data)
        sys.exit()

    for p in json_data["products"]:
        # check if valid json:
        #try:
        #    json_line = json.loads(p)
        #except ValueError:
        #    print("Invalid json", category, offset, p)

        # skip if valid data already exists
        filename = p["urlIdentifier"]
        image_location = data_directory + filename + ".jpg"
        txt_location = data_directory + filename + ".txt"
        valid_json = True
        if os.path.isfile(txt_location):
            try:
                with open(txt_location, 'r') as f:
                    json_data = json.load(f)
            except ValueError:
                valid_json = False

        if os.path.isfile(image_location) and os.path.getsize(image_location) > 100 and valid_json:
            continue

        # download image
        try: 
            if sort in sorts:
                image = p["image"]["sizes"]["Best"]["url"]
            else:
                u = "https://img.shopstyle-cdn.com/sim/"
                image = p["image"]["id"]
                first = image[0:2]
                second = image[2:4]
                u = u + first + "/" + second + "/" + image + "_best/"
                print(u)
                download_image(u, filename)
        except Exception as e:
            print("Image download exception", category, offset, str(e))
            print(p)
            print(url)
            continue

        #if (''.join(p["image"]["sizes"]["Best"]["url"].split('/')[:3]) != 'https:img.shopstyle-cdn.com'):
        #    print(p["image"]["sizes"]["Best"]["url"])
        filename = data_directory + p["urlIdentifier"] + ".txt" #('-'.join(p["image"]["sizes"]["Best"]["url"].split('/')[3:])).split('.jpg')[0] + '.txt'
        f = open(filename, 'w')
        f.write(json.dumps(p))
        f.close()

        '''
        print(category, p["id"])
        print(p["unbrandedName"])
        print(p['description'])
        print(p["image"]["sizes"]["Best"]["url"])
        '''
    #except Exception as e:
    #    print("scrape offset exception, skipping: ", category, offset, str(e))
    #    print(url)
    #    return 

def scrape_label(p, category, sort, label):
    url = "https://www.shopstyle.com/api/v2/site/search?abbreviatedCategoryHistogram=true&cat=dresses&device=desktop&filters=Size%2CColor%2CCategory%2CTopRetailer%2CTopBrand%2CHeelHeight&fts=" + label + "&includeLooks=true&includeProducts=true&includeSavedQueryId=true&limit=40&locales=all&maxNumFilters=1000&maxQuickFilters=30&numLooks=20&offset=" + str(0) + "&numSponsoredProducts=10&pid=shopstyle&prevCat=cocktail-dresses&productScore=LessPopularityEPC&quickFilterTypes=brand&quickFilterTypes=color&quickFilterTypes=fts&url=%2Fbrowse%2Fdresses&useElasticsearch=true&view=angular2"

    response = requests.get(url)


    json_data = json.loads(response.text)
    try:
        total = json_data['metadata']['total']
    except Exception as e:
        print(response.text)

    total = 5000
    #print("Category: ", category, " Total:", total)
    func = partial(scrape_offset, category, sort, True, label)
    p.map(func, range(0, total, 50))



def scrape_category(p, category, sort):
    #get total
    url = 'https://www.shopstyle.com/api/v2/products?cat=' + category + '&device=desktop&includeLooks=true&includeProducts=true&includeSavedQueryId=true&limit=1000&locales=all&maxNumFilters=1000&numLooks=20&offset=' + str(
        0) + '&pid=shopstyle&prevCat=mens-shirts&productScore=' + sort + '&url=%2Fbrowse%2F' + category + '&view=angular'

    response = requests.get(url)


    json_data = json.loads(response.text)
    try:
        total = json_data['metadata']['total']
    except Exception as e:
        print(response.text)

    total = 5000
    #print("Category: ", category, " Total:", total)
    func = partial(scrape_offset, category, sort, False, "")
    p.map(func, range(0, total, 50))


if __name__ == '__main__':
    start = time.time()
    p = Pool(24)
    for sort in sorts:
        for label in labels:
            for category in categories:
                #     scrape_category(p, category, sort)
                scrape_label(p, category, sort, label)

    p.terminate()
    p.join()
    print ('It took', time.time() - start, 'seconds.')
