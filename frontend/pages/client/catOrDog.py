import streamlit as st
from PIL import Image
from tensorflow import keras
import numpy as np

cat_class_index = 0

def setReview(review, mark):
    st.write("Dziękujemy za wystawioną opinię!")
    if mark:
        st.write("Będziemy dalej się rozwijać")
    else:
        st.write("Obiecujemy poprawę jakości naszych usług")

def run():
    st.title("Kot czy pies?")

    uploaded_file = st.file_uploader("Wgraj zdjęcie kota albo psa", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Wgrane zdjęcie", use_container_width=True)

        resized_image = image.resize((32, 32))
        img_array = keras.preprocessing.image.img_to_array(resized_image)
        img_array = img_array.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # predictions = predict(model, img_array)
        # TODO: replace with a backend call
        predictions = [0.1, 0.9]

        print("Predictions:", predictions)

        predicted_class = np.argmax(predictions)
        if predicted_class == cat_class_index:
            st.write("To jest kot")
        else:
            st.write("To jest pies")

        review = st.text_input("Zostaw swoją opinię o wyniku, jest dla nas ważna!")
        down_vote, up_vote = st.columns(2)
        if down_vote.button("Ocena pozytywna", icon="👍", use_container_width=True):
            setReview(review, True)

        if up_vote.button("Ocena negatywna", icon="👎", use_container_width=True):
            setReview(review, False)
