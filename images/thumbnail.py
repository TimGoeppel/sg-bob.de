import os, sys, re
from PIL import Image

pattern = re.compile(r"(-thumb\.\w+|thumbnail\.py)$")
files = os.listdir('.')
for file in files:
    if not pattern.search(file):
        try:
            image = Image.open(file)
            new_path = os.path.splitext(file)[0]+"-thumb."
            if new_path + "jpeg" in files or new_path + "jpg" in files or new_path + "png" in files:
                print('Thumbnail already generated for ' + file)
                continue
            s = image.size;
            size2 = 200, s[1] * 200 / s[0]
            image.thumbnail(size2, Image.LANCZOS)
            image.save(new_path + "jpeg", "JPEG");
            print(new_path + "jpeg")
        except IOError:
            print("No thumbnail for %s" % file)
