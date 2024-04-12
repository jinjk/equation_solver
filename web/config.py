from matplotlib import pyplot as plt
import os
from os.path import dirname, abspath

showImgFlag = True
rootPath = dirname(dirname(abspath(__file__)))
resources = os.path.join(rootPath, 'resources')
hw02 = os.path.join(resources, 'hw02.png')
static = os.path.join(rootPath, 'web', 'static')
out = os.path.join(static, 'out')
upload = os.path.join(rootPath, 'upload')

def showImg(img):
    if showImgFlag:
        plt.imshow(img)
        plt.show()


def showImgs(imgs):
    if not showImgFlag:
        return
    fig = plt.figure(figsize=(10, 7)) 
    i = 0
    for img in imgs:
        i += 1
        fig.add_subplot(8, 10, i) 
        # showing image 
        plt.imshow(img) 
        plt.axis('off') 
        plt.title(str(i)) 
    plt.show()
