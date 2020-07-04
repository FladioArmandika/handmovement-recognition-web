from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    # app.run(host='0.0.0.0',port=port)
    app.run()
