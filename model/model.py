import os
import random

import kagglehub
from keras.src.utils import to_categorical
import numpy as np
import tensorflow as tf
from tensorflow import keras

cat_class_index = 0
dog_class_index = 1


def set_seed(seed=42):
    tf.random.set_seed(seed)
    np.random.seed(seed)
    random.seed(seed)


def check_device():
    print("Available devices:")
    print(tf.config.list_physical_devices())
    print("Num GPUs Available: ", len(tf.config.list_physical_devices("GPU")))
    print("Num TPUs Available: ", len(tf.config.list_physical_devices("TPU")))
    print("Num CPUs Available: ", len(tf.config.list_physical_devices("CPU")))


def load_dataset():
    main_folder_name = "PetImages"
    cat_folder_name = "Cat"
    dog_folder_name = "Dog"

    images_extension = ".jpg"

    dataset_path = kagglehub.dataset_download(
        "bhavikjikadara/dog-and-cat-classification-dataset"
    )

    print("Dataset saved to:", dataset_path)

    x = []
    y = []

    for folder_name, label in zip(
        [cat_folder_name, dog_folder_name], [cat_class_index, dog_class_index]
    ):
        folder_path = os.path.join(dataset_path, main_folder_name, folder_name)
        files_list = os.listdir(folder_path)
        files_count = len(files_list)
        for index, filename in enumerate(files_list):
            if filename.endswith(images_extension):
                if index % 1000 == 1:
                    print(
                        "Loading "
                        + folder_name
                        + " image "
                        + str(index)
                        + " of "
                        + str(files_count)
                    )
                img_path = os.path.join(folder_path, filename)
                img = keras.preprocessing.image.load_img(img_path, target_size=(32, 32))
                img_array = keras.preprocessing.image.img_to_array(img)
                img_array = img_array.astype("float32") / 255.0
                x.append(img_array)
                y.append(label)

    x = np.array(x)
    y = np.array(y)

    return x, y


def split_dataset(x, y, ratio=0.1):
    num_classes = len(np.unique(y))
    indices = []
    for i in range(num_classes):
        class_indices = np.where(y == i)[0]
        np.random.shuffle(class_indices)
        split_count = int(len(class_indices) * ratio)
        indices.extend(class_indices[:split_count])
    x_split = x[indices]
    # TypeError: list indices must be integers or slices, not list
    y_split = y[indices]
    x_remaining = np.delete(x, indices, axis=0)
    y_remaining = np.delete(y, indices, axis=0)

    return (x_remaining, y_remaining), (x_split, y_split), num_classes


def create_test_set(x, y, test_size=0.1):
    (x_train, y_train), (x_test, y_test), num_classes = split_dataset(
        x, y, ratio=test_size
    )

    y_test = to_categorical(y_test, num_classes=num_classes)

    return (x_train, y_train), (x_test, y_test)


def create_validation_set(x_train, y_train, val_size=0.1):
    (x_train, y_train), (x_val, y_val), num_classes = split_dataset(
        x_train, y_train, ratio=val_size
    )

    y_val = to_categorical(y_val, num_classes=num_classes)
    y_train = to_categorical(y_train, num_classes=num_classes)

    return (x_train, y_train), (x_val, y_val)


def create_model():
    model = keras.Sequential(
        [
            keras.layers.InputLayer(input_shape=(32, 32, 3)),
            keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
            keras.layers.BatchNormalization(),
            keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Dropout(0.25),
            keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.5),
            keras.layers.Dense(2, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )

    return model


def train_model(model, x_train, y_train, x_val, y_val):
    return model.fit(
        x_train,
        y_train,
        epochs=10,
        batch_size=64,
        validation_data=(x_val, y_val),
    )


def evaluate_model(model, x_test, y_test):
    test_loss, test_acc = model.evaluate(x_test, y_test)
    return test_loss, test_acc


def predict(model, x):
    return model.predict(x)[0]


def train_and_save_model():
    model_path = "../saved_model.keras"

    set_seed(42)
    check_device()

    (x_train, y_train) = load_dataset()
    (x_train, y_train), (x_test, y_test) = create_test_set(
        x_train, y_train, test_size=0.1
    )
    (x_train, y_train), (x_val, y_val) = create_validation_set(
        x_train, y_train, val_size=0.1
    )

    model = create_model()
    train_model(model, x_train, y_train, x_val, y_val)
    evaluate_model(model, x_test, y_test)

    model.save(model_path)
    # TODO: save to storage

    return model
