import os
from PIL import Image

directory = 'imgs'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and f.endswith('.jpg'):
        with Image.open(f) as img:
            width, height = img.size
            print(f"{filename}: {width}x{height}")
            img2 = img.crop((0, 60, 1274, 1738))
            img2.save(os.path.join(directory, 'cropped_' + filename))
    # crop image to (0, 60, 1274, 1738)
