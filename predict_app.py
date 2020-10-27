import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.applications import imagenet_utils
from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
from flask import Flask, request, render_template, redirect, url_for


app = Flask(__name__)


def get_model():
    global model
    model = load_model("clothing.h5")
    print(" *Model loaded!")


def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(image)


print(" * Loading Keras model...")
get_model()


@app.route("/templates", methods=["GET", "POST"])
def home():
    return render_template("predict.html")


@app.route("/predict", methods=["POST", "GET"])
def predict():
    message = request.get_json(force=True)
    encoded = message["image"]
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(224, 224))
    prediction = model.predict(processed_image)
    results = imagenet_utils.decode_predictions(prediction)

    maxv = 0
    maxi = ""

    list = []
    i_list = []
    count = 0
    for i in results:
        for j in i:
            i_list.append(results[0][count][1])
            i_list.append(results[0][count][2])

            if maxv < results[0][count][2]:
                maxv = results[0][count][2]
                maxi = results[0][count][1]

            list.append(i_list)
            count += 1
            i_list = []

    response = {"prediction": {"name1": list[0][0], "value1": str(list[0][1])}}

    return jsonify(response)


@app.route("/templates/<name>", methods=["GET", "POST"])
def p(name):
    if name == "shoe":
        return render_template("shoe.html")
    if name == "hoodie":
        return render_template("hoodie.html")
    if name == "pants":
        return render_template("pants.html")
    if name == "tshirt":
        return render_template("tshirt.html")
    if name == "cardigan":
        return render_template("cardigan.html")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


if __name__ == "__main__":
    app.debug = True
    app.run()
