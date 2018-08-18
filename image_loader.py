"""
author: Fang Ren (SSRL), Robert Tang-Kong
version: 1.1

"""
import fabio
import numpy as np
import os


def load_image(imageFullname, detector=""):
    # get extension to consider
    ext = os.path.splitext(imageFullname)[1]
    print(imageFullname)
    imArray = np.array([])

    if ext.lower() in ['.tif', '.tiff']:
        # open tiff image
        im = fabio.open(imageFullname)
        # input image object into a numpy array
        imArray = im.data
    elif ext.lower() in ['.raw']:
        # extract raw file
        im = open(imageFullname, 'rb')
        arr = np.fromstring(im.read(), dtype='int32')
        im.close()
        try:
            arr.shape = (detector.getHeight(), detector.getWidth())
            #arr.shape = (195, 1475)
            imArray = np.array(arr)
        except:    #raw requires prompting for dimensions, hard code for now
            arr.shape = (3888, 3072)
            imArray = np.array(arr)
            
        
    return imArray
