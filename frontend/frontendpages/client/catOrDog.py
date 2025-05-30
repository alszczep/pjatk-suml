import os

from PIL import Image
import requests
import streamlit as st

cat_class_index = 0


def setReview(review, mark, prediction_id):
    st.write("Dziękujemy za wystawioną opinię!")
    if mark:
        st.write("Będziemy dalej się rozwijać")
    else:
        st.write("Obiecujemy poprawę jakości naszych usług")

    json_params = {
        "prediction_id": prediction_id,
        "is_vote_positive": mark,
        "feedback": review,
    }
    requests.post(
        os.environ["API_URL"] + "/api/change_vote_and_feedback", json=json_params
    )


def predict(uploaded_file):
    if (
        st.session_state.predicted_class is not None
        or st.session_state.prediction_id is not None
    ):
        return

    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    response = requests.post(os.environ["API_URL"] + "/api/predict", files=files)

    if response.status_code != 200:
        st.error("Wystąpił błąd podczas przetwarzania obrazu.")
        return

    st.session_state.predicted_class = response.json().get("predicted_class")
    st.session_state.prediction_id = response.json().get("prediction_id")


def run():
    st.title("Kot czy pies?")

    uploaded_file = st.file_uploader(
        "Wgraj zdjęcie kota albo psa", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is None:
        st.session_state.predicted_class = None
        st.session_state.prediction_id = None
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Wgrane zdjęcie", use_container_width=True)

        predict(uploaded_file)

        if st.session_state.predicted_class == cat_class_index:
            st.write("To jest kot")
        else:
            st.write("To jest pies")

        review = st.text_input("Zostaw swoją opinię o wyniku, jest dla nas ważna!")
        down_vote, up_vote = st.columns(2)
        if down_vote.button("Ocena pozytywna", icon="👍", use_container_width=True):
            setReview(review, True, st.session_state.prediction_id)

        if up_vote.button("Ocena negatywna", icon="👎", use_container_width=True):
            setReview(review, False, st.session_state.prediction_id)
