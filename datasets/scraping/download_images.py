import json
import os

directory = '../images/'

removed_files = 0
updated_images = 0
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        if os.path.getsize(directory + filename) == 0:
            #os.remove(directory + filename)
            #removed_files = removed_files + 1
            continue

        image_path = directory +  filename.replace(".txt",".jpg")

        if not os.path.isfile(image_path) or os.path.getsize(image_path) <= 100:
            with open(os.path.join(directory, filename), 'r') as f:
                try:
                    data = json.load(f)
                    link = data['image']['sizes']['XLarge']['url']
                    print(link)
                except Exception as e:
                    print(data)
                    print(data['image']['sizes']['XLarge'])
                    print(directory + filename)
                    print(e)
                    break
