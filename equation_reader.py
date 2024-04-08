import cv2
import pytesseract
from dataclasses import dataclass
from typing import List
from digits_reader import readDigitsFromImg

import xml.etree.ElementTree as ET

@dataclass
class Pos:
    x: int
    y: int
    w: int
    h: int
    text: str

def parseXml(xml_string):
    # Parse the XML string
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

def readEquationsFromImage(image_path):
    image = cv2.imread(image_path)
    xmlData = pytesseract.image_to_alto_xml(image, 
        config='--oem 3 -c tessedit_char_whitelist=0123456789Xx=÷')
    # read xmlData get equations and postions
    #
    data = parseXml(xmlData.decode('utf-8'))
    return data

def evaluateEquations(data: List[Pos], image_path, digits):
    image = cv2.imread(image_path)
    itemToSkip = 10
    itemIdx = -1
    for item in data:
        itemIdx += 1
        if itemIdx < itemToSkip:
            continue
        eq = item.text.replace('X', '*') \
                .replace('x', '*') \
                .replace('÷', '/') \
                .replace('=', '')
        res = eval(eq)
        print(f'{item.text} {res}')
        img = strToImg(str(res), digits)
        r = item.w / img.shape[1]
        print(r)
        w = int(img.shape[1] * r)
        h = int(img.shape[0] * r)
        img = cv2.resize(img, (w, h))
        # overlay the image
        # add img to image use addWeighted
        x, y = item.x, item.y
        print(item.x, item.y, w, h)
        print(image[y:y+h, x+w:x+w*2].shape)
        print(img[:h, :w].shape)
        image[y:y+h, x+w:x+w*2] = img[:h, :w]

    cv2.imshow('image', image)
    # wait for window to close or key press
    cv2.waitKey(0)

def strToImg(str, imgs):
    img = None
    for i in range(len(str)):
        ch = int(str[i])
        idx = (ch + 9) % 10
        if i == 0:
            img = imgs[idx].copy()
        else:
            img = cv2.hconcat([img[:, :-5], imgs[idx][:, 15:]])
    w, h, *_ = img.shape
    print(w, h)
    return img


# Example usage

image_path = '/home/jjin/workspace/equation_solver/eq.jpg'
data = readEquationsFromImage(image_path)
digits = readDigitsFromImg()
evaluateEquations(data, image_path, digits)
