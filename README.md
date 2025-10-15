# Hand Movement Recognition Web

Flask-based web interface for real-time hand gesture recognition. The application streams frames from a webcam, pre-processes them with OpenCV, and classifies the stacked sequence with a TensorFlow ResNet model to identify one of four hand movements.

## Key Features
- Live webcam feed served through `/video_feed` and displayed on the testing dashboard.
- Sequence-based prediction pipeline that stacks 20 frames before running inference.
- Pre-trained ResNet model inference served by TensorFlow/Keras.
- Simple UI in `templates/testing.html` with keyboard-triggered recognition (`D` key).
- Additional informational pages for landing (`/`) and help (`/help`).

## Requirements
- Python 3.8+ and `pip`
- A webcam accessible to OpenCV
- [TensorFlow 2.0](https://www.tensorflow.org/install) compatible hardware (GPU optional)
- Pre-trained weights file `models/ResNet.h5` (not included in this repository)
- Optional: ngrok account if you want to expose the app externally (used via `flask_ngrok`)

## Quick Start
1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/handmovement-recognition-web.git
   cd handmovement-recognition-web
   ```
2. **Create and activate a virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install flask-ngrok  # required by app.py but not pinned in requirements.txt
   ```
4. **Add the model weights**
   - Place your trained `ResNet.h5` inside the `models/` directory.
   - The loader expects the path `models/ResNet.h5`. Update `models/predict.py` if you store it elsewhere.
5. **Run the development server**
   ```bash
   python app.py
   ```
   The app defaults to port `3000`. Override it by exporting `PORT` before running: `export PORT=5000`.

## Using the App
- Navigate to `http://127.0.0.1:3000/testing` (replace `3000` with your chosen port).
- Allow the browser to access your webcam when prompted.
- Press the `D` key to send the latest 20-frame stack to `/recognize`.
- The server responds with the predicted class index; the frontend currently surfaces the raw response via a browser alert.
- Available gesture classes (as coded in the UI) are `Left`, `Right`, `Ok`, and `Call`. Update the UI and post-processing if your model uses different labels.

### REST Endpoints
| Endpoint        | Method | Description                                   |
|-----------------|--------|-----------------------------------------------|
| `/`             | GET    | Landing page with project overview.           |
| `/testing`      | GET    | Webcam dashboard for triggering predictions.  |
| `/help`         | GET    | Placeholder help page.                        |
| `/video_feed`   | GET    | MJPEG stream generated from the webcam feed.  |
| `/recognize`    | POST   | Runs the TensorFlow model on the frame stack and returns the predicted class index. |

## Project Structure
```text
.
├── app.py                 # Flask application wiring routes to templates and inference
├── camera.py              # VideoCapture helper for grabbing and resizing frames
├── models/
│   ├── cnn.py             # Model architecture (for reference/training)
│   └── predict.py         # Preprocessing and inference helpers
├── static/
│   ├── css/               # Bootstrap styles
│   └── js/                # Client-side scripts (Bootstrap bundle)
├── templates/
│   ├── index.html         # Landing page
│   ├── testing.html       # Webcam dashboard and AJAX trigger
│   └── help.html          # Help placeholder
├── requirements.txt       # Python dependencies
└── README.md
```

## Inference Pipeline Overview
1. Frames are captured by `VideoCamera.get_frame()` and downsized by a factor of 0.6.
2. `models.predict.recognize()` resizes frames to `320x240`, converts them to grayscale, thresholds, and stacks sequential frames with weighted blending.
3. The stacked frames are expanded to `(-1, 320, 240, 1)` and cast to `tf.float32`.
4. The model predicts class probabilities for each stacked frame. The app aggregates predictions via `numpy.bincount` to select the most common class.

## Troubleshooting
- **Model file missing**: Ensure `models/ResNet.h5` exists before invoking `/recognize`; otherwise TensorFlow will raise a file-not-found error on import.
- **No webcam detected**: Confirm another process is not using the camera. Update `camera.py` to select a different device index if needed.
- **Ngrok not required**: If you do not plan to expose the app externally, you can remove `run_with_ngrok(app)` and the extra dependency.
- **CORS considerations**: The app imports `flask_cors` but does not configure it. Add configuration if you expose the API to other origins.

## Contributing
Pull requests are welcome—please open an issue describing your feature or bugfix before submitting. Include details about model versions and testing steps so others can reproduce your results.

