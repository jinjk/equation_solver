import pdf2image
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw
import math

step = 10
r1 = 255 / 2337
r2 = 2095 / 2337
r3 = step / 2337

def convertPdf2Image(path):
    images = pdf2image.convert_from_path(path)
    image = np.array(images[0])
    h, w, _ = image.shape
    print(w, h)
    lineVars = []
    lastVar = (0, 0)
    for i in range(0, h, step):
        last =  i + step - 1 if i + step < h else h
        rows = image[i:last]
        v = np.var(rows)
        if lastVar[1] != nonZero(v):
            if nonZero(v) == 1:
                lineVars.append((lastVar[0] + step/2, lastVar[1]))
            else:
                lineVars.append((i + step/2, nonZero(v)))
        lastVar = (i, nonZero(v))
    
    for l in lineVars:
        if abs(l[0]/h - r1) < r3:
            start = l
        if abs(l[0]/h - r2) < r3:
            end = l

    return (images[0], lineVars, start, end)

def nonZero(v):
    return 1 if v != 0 else 0

def debug():
    image, lineVars, s, e = convertPdf2Image('/home/jjin/Downloads/test.pdf')
    w, h = image.size
    draw = ImageDraw.Draw(image)
    for i, v in lineVars:
        draw.line((0, i, w, i), fill=(255, 0, 0), width=1)
        draw.text((0, i), str(i), fill=(255, 0, 0))
    image.show()
    print(s, e)

if __name__ == '__main__':
    debug()

