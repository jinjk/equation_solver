import cv2
import numpy as np

image_path = '/home/jjin/workspace/equation_solver/hw01.jpg'

def readDigitsFromImg():
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarize the image, black background and white digits
    _, binary = cv2.threshold(gray,127, 255,cv2.THRESH_BINARY_INV)

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
    kernel = np.ones((30, 30), np.uint8)
    closing = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.dilate(closing, kernel)
    contours,_ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # }}


    # Get digit images with white background {{
    digitImgs = []
    contours = sorted(contours, key=lambda x: cv2.boundingRect(x)[0])
    h = max([cv2.boundingRect(cnt)[3] for cnt in contours])
    for cnt in contours:
        x, y, w, _ = cv2.boundingRect(cnt)
        oriDigImg = image[y:y+h, x:x+w].copy()
        oriDigImg[(binary[y:y+h, x:x+w]==0)] = 255
        digitImgs.append(oriDigImg)
    # }}

    return digitImgs

# Example usage

readDigitsFromImg()
