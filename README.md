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


