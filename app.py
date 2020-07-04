from flask import Flask, render_template, Response, request, jsonify, after_this_request
from flask_ngrok import run_with_ngrok
from camera import VideoCamera
from models.predict import recognize
from cv2 import cv2
import numpy as np
import os


from flask_cors import CORS, cross_origin

# Initializing flask application
app = Flask(__name__)
run_with_ngrok(app)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/testing')
def pengujian():
    return render_template('testing.html')
@app.route('/help')
def bantuan():
    return render_template('help.html')

@app.route('/video_feed')
def video_feed():

    frame = gen(VideoCamera())

    return Response(frame,
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(predict(VideoCamera()))


def gen(camera):
    frames = []
    while True:
        frame = camera.get_frame()
        frames.append(frame)

        print(len(frames))

        if(len(frames) == 20):
            recognize(frames)
            frames = []

        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    # app.run(host='0.0.0.0',port=port)
    app.run()
