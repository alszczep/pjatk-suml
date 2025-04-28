# pjatk-suml

AI app classifying cats and dogs.

## Setting up the local environment

Recommended python version is 3.10.
Create the venv - e.g. with `python -m venv venv` or using PyCharm.
Install dependencies - `[path/to/venv]/Scripts/pip.exe install -r [path/to/project]requirements.txt` 

## Running the app locally

`[path/to/venv]/Scripts/streamlit.exe run main.py`

## Retraining the model

To retrain the model, delete the `saved_model.keras` file and run the app as usual.

## Tensorflow with GPU

For native GPU support on Windows you will need:
- CUDA 11.2
- cuDNN 8.1.0

## Dataset

- https://www.kaggle.com/datasets/bhavikjikadara/dog-and-cat-classification-dataset/data

## Running the app using docker

Building docker image using docker file
- docker build -t [specify_image_name]

Pulling created docker image from docker hub
- docker pull mychnik/kotkiipieski:1.0

Running application using docker
- docker run -p 8501:8501 [image_id]

Using application
- app is avaliable at  http://localhost:8501 after running container