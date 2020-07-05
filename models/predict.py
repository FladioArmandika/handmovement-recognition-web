from cv2 import cv2
import numpy as np
import os
from tensorflow.keras.models import load_model
import tensorflow as tf

model = load_model(os.path.join('models','ResNet.h5'))
# model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])

def stackingImages(img1,img2):
    alpha = 1.0 / 2
    beta = 1.0 - alpha
    new_img = cv2.addWeighted(img1, alpha, img2, beta, 0.0)
    return new_img

def recognize(frames):

    print('raw: ' + str(frames[0].shape))

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

    # reshape
    stackedFrames = np.array(stackedFrames).reshape(-1,320,240,1) 

    #decode   
    decodedFrames = []
    for stackedFrame in stackedFrames:
        # decodedFrame = tf.image.decode_jpeg(stackedFrame)
        decodedFrame = tf.cast(stackedFrame, tf.float32)
        decodedFrames.append(decodedFrame)

    print('decoded : ' + str(decodedFrames[0].shape) )

    # Identification
    results = []
    for decodedFrame in decodedFrames:
        result = predict(decodedFrame)
        results.append(result)

    # counts = np.bincount(results)
    # result = np.argmax(counts)
    # print('result : ' + str(results[0]))

    # print(results)

    return results

def predict(frame):
    print('predic' + str(len(frame)))
    frame = frame[None,:]
    result = model.predict(frame)
    # result = 3
    return result

def preprocessing(frame):
    resized = cv2.resize(frame, (320,240))
    # print('resized : ' + str(resized.shape))
    grayscaled = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # print('grayscaled : ' + str(grayscaled.shape))
    retval,thresholded = cv2.threshold(grayscaled, 128, 1, cv2.THRESH_BINARY)
    # print('thresholded : ' + str(thresholded.shape))
    thresholded = np.expand_dims(thresholded, axis=-1)
    # print('expand : ' + str(thresholded.shape))
    return thresholded  
