import cv2
import numpy as np
import config as config

def readDigitsFromImg(image_path, kernel):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarize the image, black background and white digits
    _, binary = cv2.threshold(gray,200, 255,cv2.THRESH_BINARY_INV)

    # remove small stains from image {{
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats( \
        binary, None, None, None, 8, cv2.CV_32S)
    areas = stats[1:,cv2.CC_STAT_AREA]
    cleaned = np.zeros((labels.shape), np.uint8)
    for i in range(0, nlabels - 1):
        if areas[i] >= 100:   #keep
            cleaned[labels == i + 1] = 255
    # }}

    # get the outside contours of the digits {{
    closing = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.dilate(closing, kernel)
    contours,_ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(cnt) for cnt in contours]
    # }}


    # Get digit images with white background {{
    rects = sorted(rects, key=lambda r: r[1])
    rectList = []
    row = []
    for i in range(0, len(rects)):
        row.append(rects[i])
        if (i+1) % 10 == 0 and i != 0 or i == len(rects) - 1:
            print(f'i -> {i}')
            row = sorted(row, key=lambda c: c[0])
            rectList.append(row)
            row = []

    # find contours in a row
    
    i = 0
    maxH = -1
    for row in rectList:
        for r in row:
            x, y, w, h = r
            maxH = max(maxH, h)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, str(i) + ',' + str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            i += 1

    print(len(rectList))
    print(maxH)
    digitImgs = []
    for row in rectList:
        for r in row:
            x, y, w, _ = r
            oriDigImg = image[y:y+maxH, x:x+w].copy()
            oriDigImg[(binary[y:y+maxH, x:x+w]==0)] = 255
            digitImgs.append(oriDigImg)
    # }}

    return digitImgs

def printCnt(image, cnts):
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    config.showImg(image)

# Example usage
if __name__ == '__main__':
    kernel = np.ones((30, 30), np.uint8)
    imgs = readDigitsFromImg(config.hw02, kernel)
    config.showImgs(imgs)
    
