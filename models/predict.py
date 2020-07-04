from cv2 import cv2
import numpy as np



def stackingImages(img1,img2):
    alpha = 1.0 / 2
    beta = 1.0 - alpha
    new_img = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
    return new_img

def recognize(frames):

    # Preprocessing
    preprocessedFrames = []
    for frame in frames:
        preprocessed = preprocessing(frame)
        preprocessedFrames.append(preprocessed)

    # Stacking images
    stackedFrames =[]
    tempFrame = preprocessedFrames[0]
    for frame in preprocessedFrames:
        stack = stackingImages(tempFrame,frame)
        stackedFrames.append(stack)
        tempFrame = stack

    # Identification
    results = []
    for stackedFrame in stackedFrames:
        result = predict(stackedFrame)
        results.append(result)

    # a = np.array(results)
    counts = np.bincount(results)
    result = np.argmax(counts)

    print(results)

    return "hello"

def predict(frame):
    
    return result

def preprocessing(frame):
    resized = cv2.resize(frame, (320,240))
    grayscaled = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    retval,thresholded = cv2.threshold(grayscaled, 128, 1, cv2.THRESH_BINARY)
    return thresholded