from PIL import Image
import glob
import os
import numpy as np
import csv
import random
from skimage.transform import resize
from skimage import io
from sklearn.model_selection import train_test_split
import re

image_size = 224

r1 = re.compile("(\d+)_")
r2 = re.compile("_(\d+)")

IMGpath = "../../data/DataSet2/IMG/"


def key1(a):
    m1 = r1.findall(a)
    m2 = r2.findall(a)
    return int(m1[0]), int(m2[0])


# resize images
def resize_Images():
    i = 0
    for filepath in glob.iglob(IMGpath + '*.jpg'):
        filename = os.path.basename(filepath)
        image = io.imread(filepath)
        resized = resize( image, (image_size, image_size), anti_aliasing=True)
        io.imsave('../../data/DataSet2/resized224/' + filename, resized)
        #print(filename)
        i += 1
    print("%d imagegs resized"%i)

def load_Data():
    (x_all, y_all) = load_batch()
    x_all = np.array(x_all)
    y_all = np.array(y_all)
    x_train, x_test, y_train, y_test = train_test_split(x_all, y_all, test_size=0.2, random_state=10)
    return (x_train, y_train), (x_test, y_test)


def load_batch():
    # image data
    imageCount = 0
    filelist = []
    for imagefile in glob.iglob('../../data/DataSet2/resized224/*.jpg'):
        filelist.append(imagefile)
        imageCount += 1

    filelist.sort(key=key1)
    data = np.zeros((imageCount, image_size, image_size, 1))
    labels = np.zeros(imageCount)
    index = 0

    # labels
    labelsDict = dict()
    labels = list()
    # for filepath in glob.iglob(''):
    with open('../../data/DataSet2/label.csv') as csvfile:
        lines = csvfile.readlines()
        for line in lines:
            labelsDict[line.strip().split(',')[0].strip()] = line.strip().split(',')[1].strip()

#     for val,key in labelsDict.iteritems():
#         print(val)

    for counter, imagefile in enumerate(filelist):
        #print(str(counter + 1) + 'load image file: ' + imagefile)
        imgFileName = imagefile.strip().split("/")[5]
        print(imgFileName)
        t = Image.open(imagefile)
        arr = np.array(t)  # Convert test image into an array 32*32*3
        data[index] = np.expand_dims(arr, axis=2)
        labels.append(labelsDict[str(imgFileName)])
        # Progress Record
#         print("Index "+str(counter + 1) +
#               ' Image Name: ' +
#               imgFileName +
#               " Labels: " + labelsDict[imgFileName])
        index += 1

    # # labels
    # labelsDict = dict()
    # labels = list()
    # # for filepath in glob.iglob(''):
    # with open('../data/label.csv') as csvfile:
    #     lines = csvfile.readlines()
    #     for line in lines:
    #         labelsDict[line.strip().split(',')[0]] = line.strip().split(',')[1]


    return data, labels

#
# if __name__ == '__main__':
#      resize_Images()
