import json
import numpy as np
import cv2
import requests
import os
import sys
import dotenv

dotenv.load_dotenv()


def read_image(image_path):
    image = cv2.imread(image_path)
    return image


def preprocess(image):
    image = cv2.resize(image, (150, 150))
    image = image.astype("float32")
    return image


def predict(image):
    image = preprocess(image)
    image = image / 255
    data = json.dumps({"instances": [image.tolist()]})
    # Define headers with content-type set to json
    headers = {"content-type": "application/json"}

    # Capture the response by making a request to the appropiate URL with the appropiate parameters
    json_response = requests.post(
        os.getenv(
            "TENSORFLOW_SERVE_ENDPOINT",
            "http://localhost:8501/v1/models/my_model:predict",
        ),
        data=data,
        headers=headers,
    )
    if json_response.status_code != 200:
        raise Exception("Request failed with status code: {}".format(json_response))
    # Parse the predictions out of the response
    predictions = json.loads(json_response.text)["predictions"]
    return np.argmax(predictions, axis=1)[0]


def get_class(index):
    if index == 0:
        return "bird"
    elif index == 1:
        return "cat"
    elif index == 2:
        return "dog"
    return None


def main():
    try:
        file_name = sys.argv[1]
    except:
        raise Exception("Please provide an image file name")
    image = read_image(file_name)
    prediction = predict(image)
    print("The predicted class is: {}".format(get_class(prediction)))


if "__main__" == __name__:
    main()
