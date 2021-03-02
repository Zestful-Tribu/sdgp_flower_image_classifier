import sys
import os
import glob
import re
import numpy as np

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import cv2
import tensorflow as tf

app = Flask(__name__)
app.config["DEBUG"] = True

model = load_model('lilyora_first_try.h5')
model.layers[0].input_shape
# labels = ["dandelion", "jasmine", "rose", "sunflower", "viola"]

#predicting code using the model

def model_predict(img, model):
    img_array = image.load_img(img, target_size=(150, 150))
    img_array = np.expand_dims(img_array, axis = 0)
    result = model.predict_classes(img)
    return result


# defining the index route

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
    # return "Hello there"


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #get the file from post request
        f = request.file['file']

        #save the file from post request
        basepath = os.path.join.dirname(__file__)
        file_path = os.path.join( basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # make prediction
        prediction = model_predict(file_path, model)

        # These are the prediction categories
        CATEGORIES = ["dandelion", "jasmine", "rose", "sunflower", "viola"]
        result = CATEGORIES[prediction]

        return result

    return None


if __name__ == '__main__':
    app.run(port=5000, debug=True)




    