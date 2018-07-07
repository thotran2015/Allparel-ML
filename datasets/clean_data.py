import os
import json

directory = "images/"

def valid_json(filename):
    fullpath = directory + filename
    with open(fullpath, 'r') as myfile:
        data = myfile.read()
    try:
        jsonfile = json.loads(data)
    except Exception as e:
        print(filename, str(e))
        return False
    return True

def jpg_file_exists(filename):
    fullpath = directory + filename
    if os.path.isfile(fullpath) and os.path.getsize(fullpath) > 100:
        return True
    return False


def txt_file_exists(filename):
    fullpath = directory + filename
    if os.path.isfile(fullpath) and os.path.getsize(fullpath) > 10:
        return True
    return False


invalid_jsons = 0
invalid_json_files = 0
invalid_images = 0
total = 0
bad_file_prefixes = []
# program for deleted invalid images and files 
for filename in os.listdir(directory):
    total = total + 1
    if filename.endswith(".txt"):
        json_file = filename
        image_file = filename.replace(".txt", ".jpg")
        prefix = filename.replace(".txt", "")
    elif filename.endswith(".jpg"):
        json_file = filename.replace(".jpg", ".txt")
        image_file = filename
        prefix = filename.replace(".jpg", "")

    json_file_valid = txt_file_exists(json_file)
    if not json_file_valid:
        invalid_json_files = invalid_json_files + 1
        bad_file_prefixes.append(prefix)
        continue
    img_file_valid = jpg_file_exists(image_file)
    if not img_file_valid:
        invalid_images = invalid_images + 1
        bad_file_prefixes.append(prefix)
        continue
    json_valid = valid_json(json_file)
    if not json_valid:
        invalid_jsons = invalid_jsons + 1
        bad_file_prefixes.append(prefix)
        continue
    
print(total, "invalid json", invalid_jsons, "invalid json files", invalid_json_files, "invalid images", invalid_images)

for prefix in bad_file_prefixes:
    img_file = directory + prefix + ".jpg"
    txt_file = directory + prefix + ".txt"
    if os.path.isfile(txt_file):
        os.remove(txt_file)
    if os.path.isfile(img_file):
        os.remove(img_file)
    
