import flask, os
from main import predict, read_image, get_class
import requests

app = flask.Flask(__name__)

# api to save image
@app.route("/predict_local_image", methods=["POST"])
def save_image():
    """
    Save image to local directory

    usage: curl -X POST -F "image=@/path/to/image" http://localhost:5000/predict_local_image
    """
    if flask.request.method == "POST":

        # get image from request
        image = flask.request.files["image"]
        # save image to disk
        if not os.path.exists("tmp"):
            os.mkdir("tmp")

        image.save(os.path.join("tmp", image.filename))
        image = read_image(os.path.join("tmp", image.filename))
        prediction = get_class(predict(image))
        return flask.jsonify({"prediction": prediction})

    else:
        return flask.jsonify({"error": "Invalid request"})


@app.route("/predict_url_image", methods=["POST"])
def predict_url_image():
    """
    Predict image from url

    usage: curl -X POST -d "url=https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" http://localhost:5000/predict_url_image
    """

    if flask.request.method == "POST":
        # get image from request
        image_url = flask.request.form["image_url"]
        # download image from url

        image = requests.get(image_url).content
        # save image to disk
        if not os.path.exists("tmp"):
            os.mkdir("tmp")

        with open("tmp/image.jpg", "wb") as f:
            f.write(image)

        image = read_image(os.path.join("tmp", "image.jpg"))
        prediction = get_class(predict(image))
        return flask.jsonify({"prediction": prediction})
    else:
        return flask.jsonify({"error": "Invalid request"})


if __name__ == "__main__":
    app.run(debug=True)
