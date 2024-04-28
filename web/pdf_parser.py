# Standard library imports
from PIL import Image, ImageDraw

# Related third party imports
import numpy as np
import pdf2image
from matplotlib import pyplot as plt
from icecream import ic

# Local application/library specific imports
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor

import cv2
import re

step = 10
r1 = 255 / 2337
r2 = 2095 / 2337
r3 = step / 2337
model = load_model()
processor = load_processor()

def convertPdf2Image(path):
    images = pdf2image.convert_from_path(path)
    image = np.array(images[0])
    h, w, _ = image.shape
    ic(w, h)
    lineVars = []
    lastVar = (0, 0)
    for i in range(0, h, step):
        last =  i + step - 1 if i + step < h else h
        rows = image[i:last]
        v = np.var(rows)
        halfStep = int(step/2)
        if lastVar[1] != nonZero(v):
            if nonZero(v) == 1:
                lineVars.append((lastVar[0] + halfStep, lastVar[1]))
            else:
                lineVars.append((i + halfStep, nonZero(v)))
        lastVar = (i, nonZero(v))

    for i, v in enumerate(lineVars):
        if abs(v[0]/h - r1) < r3:
            start = i+1
        if abs(v[0]/h - r2) < r3:
            end = i
    return (images[0], lineVars, start, end)

def nonZero(v):
    return 1 if v != 0 else 0

def get_text():
    image, lineVars, s, e = convertPdf2Image('/home/jjin/Downloads/test.pdf')
    ic(type(s), type(e))
    imgData = np.array(image)
    seg_count = 3
    seg_len = int((e - s) / seg_count)
    img_parts = []
    res_list = []
    for i in range(0, seg_count):
        start = s + i * seg_len
        end = min(s + (i + 1) * seg_len, e)
        segImg = imgData[lineVars[start][0]:lineVars[end][0]]
        img_parts.append(segImg)
        cImg = Image.fromarray(segImg)
        res = batch_inference([cImg], model, processor)
        res_list.append(res)
        plt.imshow(segImg)
        plt.show()
    return (img_parts, res_list)

def get_equation_pos(img):
    bgrImg = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray,200, 255,cv2.THRESH_BINARY_INV)
        # get the outside contours of the digits {{
    kernel = np.ones((15,15),np.uint8)
    closing = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.dilate(closing, kernel)
    contours,_ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # draw the contours
    return (bgrImg, contours)

    
if __name__ == '__main__':
    imgs, resList = get_text()
    bgrImg, contours = get_equation_pos(imgs[0])
    # extract text using regular expression r'\$\$(.*)\$\$'
    equations = []
    ic(resList)
    for str in resList[0]:
        str = str.replace('$', '')
        text = re.findall(r'(.*)', str)
        for line in text:
            eqs = re.findall(r'[^=]+', line)
            ic(eqs)
            equations.extend(eqs)
    
    for i, contour in enumerate(contours[::-1]):
        x, y, w, h = cv2.boundingRect(contour)
        ic(i)
        cv2.putText(bgrImg, f'{equations[i]}-{i}', (x+200, y+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    plt.imshow(bgrImg)
    plt.show()
        
    


