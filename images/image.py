import os, sys
from PIL import Image

for file in os.listdir('.'):
    print(file)
    try:
        image = Image.open(file)
        s = image.size;
        size2 = 200, s[1] * 200 / s[0]
        image.thumbnail(size2, Image.LANCZOS)
        image.save(os.path.splitext(file)[0]+"-thumb.jpeg", "JPEG");
    except IOError:
        print("No thumbnail for %s" % file)
