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

## Running the apps using docker

The easiest way to get the apps running is to use docker compose:
- running: `docker-compose up`
- rebuilding: `docker-compose build`
- run with rebuild: `docker-compose up --build`

### Frontend

`docker-compose up --build frontend`

The app will be available at http://localhost:8501.

### Backend

`docker-compose up --build backend`

The app will be available at http://localhost:8000.

`saved_model.keras` file can be copied into the `backend` folder,
this way model will be loaded from there, instead of the cloud storage.

#### Migrations

- Create a .env file in the backend folder. You can use .env.example file as a template.
- Make sure the database is running (`docker compose up db`)
- Also, you might need to install `psycopg2` in the backend's venv, in case the app crashes.

To create migrations you can use:
`python manage.py makemigrations`

To apply migrations you can use:
`python manage.py migrate`
