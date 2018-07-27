# Data Scraping
To run the scraper on Shopstyle, run `cd datasets/scraping; python3 scrape.py`. 
To run the scraper on Lyst, run `cd datasets/scraping/Lys; python3 getlyst.py`. (NOTE:does not check for existing images/records)

Images will be placed in `datasets/images` and metadatase (description, title, etc.) will be placed in the mongo database.

# Querying Database
Run `mongo` in the terminal. Then in the mongo command line:
```
> use allparel
> db.clothes.count(); 
> db.clothes.find({"image_file":"full_image_path"});
```

# Preparing the Dataset for Training
Before training, you must pre-process the data stored in the database:
```
cd datasets/labelling; python3 make_labels.py
```
This will organize your images into directories `train/group_name/label_name/image.jpg` and `validation/group_name/label_name/image.jpg` for each group and label. It will also create files image_labels.txt (labels for each image) and labels.txt (total number of images and list of labels). 

To change the groups, labels, ang clothing categories included, go to the top of the `make_labels.py` file in the configuration section as the top and change the following code:
```
categories = [dress, shirt, pant, skirt] #categries to include
groups = [config.group1, config.group2, ...]
group_names = ['group_name1', 'group_name2', ...]
labels = config.group1 + config.group2 + ...
```
To modify the configuration of the preprocessing, such as the labels contained in each group, the defined categorie and sub categories, etc. edit `datasets/labelling/config.py` which is a total mess. 

# Running Training
`python3 main.py -c configs/vgg_config.json`

# Evaluation


# Running Predictions
To predict on a single image, run:
`python3 predict.py -c configs/vgg_config.json`
To run prediction on all the records in the database, run `python3 predict_to_db.py`. This will store all the predictio results in the database.

# Interface
Images, descriptions, and prediction results stored in the mongo database can be viewed using the webapp https://github.com/sarahwooders/Allparel. 
