import sys
import os
import glob
import re
import numpy as np

from flask import Flask, redirect, url_for, request, render_template, jsonify
from werkzeug.utils import secure_filename

from keras.models import load_model
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import cv2
import tensorflow as tf

app = Flask(__name__)
app.config["DEBUG"] = True

model = load_model('lilyora_fourth_try.h5')
model.layers[0].input_shape
# labels = ["dandelion", "jasmine", "rose", "sunflower", "viola"]

flowerInfo = [
    {
        'name':'anthurium',
        'medical':"",
        'cosmetic':"",
        'edibility':"",
        'decorative':"",
        'e-benefit':""

    },
    {
        'name':'anthurium',
        'medical':"",
        'cosmetic':"",
        'edibility':"",
        'decorative':"",
        'e-benefit':""

    },
    {
        'name':'anthurium',
        'medical':"",
        'cosmetic':"",
        'edibility':"",
        'decorative':"",
        'e-benefit':""

    },
    {
        'name':'anthurium',
        'medical':"",
        'cosmetic':"",
        'edibility':"",
        'decorative':"",
        'e-benefit':""

    }
]

#predicting code using the model

def model_predict(img, model):
    img_array = image.load_img(img, target_size=(150, 150))
    img_array = np.expand_dims(img_array, axis = 0)
    result = model.predict_classes(img_array)
    return result


# defining the index route

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
    # return "Hello there"


@app.route('/test', methods=['GET'])
def test():
    return jsonify({"test":"Hello from server"})


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #get the file from post request
        print("upload called")
        f = request.files['image']

        #save the file from post request
        basepath = os.path.dirname(__file__)
        file_path = os.path.join( basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        print("before prediction")

        # make prediction
        prediction = model_predict(file_path, model)
        predictionInt = np.int64(prediction[0]).item()

        print("after prediction")

        # These are the prediction categories
        CATEGORIES = ["Anthurium", "Bell flower", "Calendular", "Caliandra", "Cannas", "Cardinals Guard", "Chess flower",
            "Cleome Hassleriana", "Colstsfoot", "Common Dandelion", "Creeping Buttercup", "Daffodil", "Daisy", "Dandelion", 
            "Golden Penda", "Golden Shrimp", "Irises", "Jasmine", "Kapuru", "Leucantheum Maximum", "Local spider flower",
            "Malpighiaceae", "Manel", "Mountain Marigold", "Orchid Pink", "Orchid Yellow", "Pentas Lanceolata", "Phlox",
            "Phyllis African Marigold", "Plumbago Auriculata", "Rose", "Rose of venesuela", "Snowdrop", "Sunflower", 
            "Tanaman Hias Bunga Pink Kasturi", "Tiger Lily", "Viola", "Wedelia", "Wild Pansy", "Willowleaf Angelon", "Willowleaf Angelon(purple)",
            "Wood Anemone", "Yellow Cosmos"]
        result = CATEGORIES[predictionInt]

        # return jsonify({"flower":result})
        return result

    return None


@app.route('/flowerlist', methods=['GET'])
def getFlowerList():



if __name__ == '__main__':
    app.run(port=5000)

 


    