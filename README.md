# Data Scraping

# Creating Dataset
Process the raw scraped data with:
`cd datasets/labelling; python3 make_labels.py`
This will organize your images into directories by category, and create a files image_labels.txt (labels for each image) and labels.txt (total number of images and list of labels). 

If there are any processing errors, run 
`cd datasets; python3 clean_data.py`

# Running Training
