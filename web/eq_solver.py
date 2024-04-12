from dataclasses import dataclass
from digits_reader import readDigitsFromImg
from PIL import Image
from typing import List
import cv2
import numpy as np
import pytesseract
import random
import re
import sys

import xml.etree.ElementTree as ET
import config

@dataclass
class Pos:
    x: int
    y: int
    w: int
    h: int
    text: str

def parseXml(xml_string):
    # Parse the XML stringconfig
    root = ET.fromstring(xml_string)
    # Create a list to store the data
    items = []

    # Iterate over all 'TextLine' elements in the XML
    for textline in root.iter('{http://www.loc.gov/standards/alto/ns-v3#}String'):
        # Extract the 'HPOS', 'VPOS', and 'CONTENT' attributes
        x = int(textline.get('HPOS'))
        y = int(textline.get('VPOS'))
        w = int(textline.get('WIDTH'))
        h = int(textline.get('HEIGHT'))
        text = textline.get('CONTENT')

        # Append the data to the list
        items.append(Pos(x, y, w, h, text))

    return items

def readEquationsFromImage(image):
    xmlData = pytesseract.image_to_alto_xml(image, 
        config='--oem 3 -c tessedit_char_whitelist=0123456789Xx=÷')
    # read xmlData get equations and postions
    #
    data = parseXml(xmlData.decode('utf-8'))
    return data

def evaluateEquations(data: List[Pos], image, digits, a, b, skip=0):
    ih, iw, _ = image.shape
    itemIdx = -1
    for item in data:
        itemIdx += 1
        if itemIdx < skip:
            continue
        eq = item.text.lower()
        eq = re.sub(r'x+', '*', eq)
        eq = re.sub(r'÷+', '/', eq).replace('=', '')
        res = eval(eq)
        print(f'{item.text} {res}')
        img = strToImg(str(res), digits)
        r = (item.w / img.shape[1]) * a + b
        w = int(img.shape[1] * r)
        h = int(img.shape[0] * r)
        img = cv2.resize(img, (w, h))
        # overlay the image
        # add img to image use addWeighted
        x, y = item.x, item.y
        # print(item.x, item.y, w, h)
        # print(image[y:y+h, x+w:x+w*2].shape)
        # print(img[:h, :w].shape)
        rx = x+item.w
        ry = y - int(h * 0.2)
        ry2 = min(ry+h, ih)
        rx2 = min(rx+w, iw)
        h = ry2 - ry
        w = rx2 - rx
        image[ry:ry+h, rx:rx+w] = img[:h, :w]

    path = f'{config.static}/result.png'
    cv2.imwrite(path, image)
    image_1 = Image.open(f'{config.static}/result.png')
    im_1 = image_1.convert('RGB')
    im_1.save(f'{config.static}/result.pdf')
    config.showImg(image)

def strToImg(str, imgs):
    img = None
    for i in range(len(str)):
        ch = int(str[i])
        idx = (ch + 9) % 10
        r = random.randint(0, 7)
        r = 3 if r == 1 else r
        idx = r * 10 + idx
        if i == 0:
            img = imgs[idx].copy()
        else:
            img = cv2.hconcat([img[:, :-5], imgs[idx][:, 5:]])
        img = shake(img)
    # w, h, *_ = img.shape
    # print(w, h)
    return img

def shake(img):
    f1 = random.randint(90, 100) / 100.0
    f2 = random.randint(90, 100) / 100.0
    shaked = img.copy()
    shaked.fill(255)
    img = cv2.resize(img, (0, 0), fx = f1, fy = f2, interpolation=cv2.INTER_CUBIC)
    angle = random.randint(0, 5)
    M = cv2.getRotationMatrix2D((img.shape[1] / 2, img.shape[0] / 2), angle, 1)
    img = cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), borderValue=(255,255,255))
    y, x, _ = tuple((np.subtract(shaked.shape, img.shape)/2).astype(int))
    shaked[y:y+img.shape[0], x:x+img.shape[1]] = img[:]
    return shaked


def writeAnswerToPDF(img_path, fontSize, todoCount):
    image = cv2.imread(img_path)
    image = cv2.resize(image, (0, 0), fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    data = readEquationsFromImage(image)
    kernel = np.ones((20, 20), np.uint8)
    digits = readDigitsFromImg(config.hw02, kernel)
    evaluateEquations(data, image, digits, 0.05, fontSize/100, skip=todoCount)

# Example usage
if __name__ == '__main__':
    # get image path from command line
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        print("Please provide an image path as a command line argument.")
        sys.exit(1)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (0, 0), fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    data = readEquationsFromImage(image)
    kernel = np.ones((20, 20), np.uint8)
    digits = readDigitsFromImg(config.hw02, kernel)
    evaluateEquations(data, image, digits, 0.05, 0.25)
