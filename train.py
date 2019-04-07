import argparse
import random
import cv2

parser = argparse.ArgumentParser(description='parse Directory')
#command line arguments the program is willing to accept
parser.add_argument('--pos', help ='positive images')
parser.add_argument('--neg', help='negative images')

args = parser.parse_args()
#saving the parses arguments to variables
posImgDr = args.pos
negImgDr = args.neg

def crop_center(img):
    h, w, color = img.shape #returns the dimensions of the image + colourFLag
    l = (w - 64)/2
    t = (h - 128)/2

    crop = img[t:t+128, l:l+64]
    return crop

def randomWindows(img):  #generating 10 random windows from the  image
    h,w ,color = img.shape
    if h<128 or w<64:
        return []

    h = h-128
    w = w-64

    windows = []

    for i in range(10):
        x = random.randint(0,w)
        y = random.randint(0,h)
        windows.append(img[y:y+128,x:x+64])

    return windows

def extractFiles():

    pos = []
    neg = []

    pathPos = posImgDr
    for(dirpath, subdir, files) in os.walk(pathPos): #returns all the dir, file name in th specified dirpath
        pos.extend(files) #keeps adding all the files into the array
        break

    pathNeg = negImgDr
    for(dirpath, subdir, files) in os.walk(pathNeg):
        neg.extend(files)
        break

    return pos, neg


def readImages(posFiles, negFiles):

    x =[]
    Y =[]

    posCount = 0

    for imgFile in posFiles:
        absPath = os.path.join(posImgDr, imgFile) #creating an absolute path for the image
        print(absPath)
        img = cv2.imread(absPath) #reading the image using opencv
        cropped = crop_center(img)

        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        #features are extracted and represented using Histogram of Oriented Gradeints
        features = hog(gray, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True, feature_vector=True)
        posCount+= 1
        X.append(features)
        Y.append(1)


    negCount = 0

    for imgFile in negFiles:
        absPath = os.path.join(negImgDr, imgFile)
        print(absPath)
        img = cv2.imread(absPath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        windows = randomWindows(gray)

        for window in windows:
            features = hog(wundow, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2), block_norm="L2", transform_sqrt=True, feature_vector=True)
            negCount += 1
            X.append(features)
            Y.append(0)

    return X, Y, posCount, negCount
