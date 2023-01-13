# Tensorflow Serve

Tensorflow serve is a tool that allow us to deploy tensorflow models in the server. Here, we will discuss the easiest way to get started with the tensorflow serve using docker.
This repository takes inspiration from the coursera's MLOps course Deploying Machine Learning Models in Production part 4.

## Pull the docker image

```
docker pull tensorflow/serving
```

## Download Pretrained Models
Download pretrained models and save it inside model folder

```
wget -q -P models/animal_classifier/1/ https://storage.googleapis.com/mlep-public/course_1/week2/model-augmented/saved_model.pb
wget -q -P models/animal_classifier/1/variables/ https://storage.googleapis.com/mlep-public/course_1/week2/model-augmented/variables/variables.data-00000-of-00001
wget -q -P models/animal_classifier/1/variables/ https://storage.googleapis.com/mlep-public/course_1/week2/model-augmented/variables/variables.index
```

## Install the requirements

```
pip install -r requirements.txt
```

## Running the model
```
docker run --rm -p 8501:8501 \
    --mount type=bind,\
    source=<absolute path of the model in the host>,\
    target=<destination path>\
    -e MODEL_NAME=<model_name> -t <tag_name>

```

More specific command
```
docker run --rm -p 8501:8501 --mount type=bind,source=/home/siddhi/git/tensorflow-serve/models,target=/models/ -e MODEL_NAME=animal_classifier -t tensorflow/serving
```

After you run the tensorflow serving server, now we run the actual client program `main.py`

<strong>NOTE: </strong> you might want to change the paths. This is what my directory structure looks like:

<img src = 'resources/directory_structure.png'>

```
python main.py data/test_dog.jpg  

>>>The predicted class is: dog 
```

## Using the Flask API

I have created a wrapper around the main function so that it can be accessed through the Flask API. To make the serving available through flask, first run the flask api.

```
flask run
```

Test out the APIs in your terminal using curl command

Making prediction from the url (Make sure the URL redirects to an image)

``` 
curl -X POST http://127.0.0.1:5000/predict_url_image  -d "image_url=https://static01.nyt.com/images/2021/04/27/science/21SCI-DISHONESTBIRDS1/21SCI-DISHONESTBIRDS1-mediumSquareAt3X.jpg"
```


Making predictions from local file

```
curl -X POST http://127.0.0.1:5000/predict_local_image -F image=@data/test_dog.jpg
```
