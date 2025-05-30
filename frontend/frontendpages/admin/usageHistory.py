from io import BytesIO
import os

from PIL import Image
import requests
import streamlit as st

cat_class_index = 0


def run():
    st.title("Historia użycia aplikacji klienckiej")

    response = requests.get(os.environ["API_URL"] + "/api/all_predictions")

    if response.status_code != 200:
        st.error("Nie udało się pobrać listy")
        return

    predictions_list = response.json()
    print(predictions_list)

    st.markdown("### MODEL_1_PSY_KOTY 👤Akcje użytkowników:")

    for prediction in predictions_list:
        col1, col2 = st.columns([1, 3])
        with col1:
            img_response = requests.get(prediction["file_url"])
            img = Image.open(BytesIO(img_response.content))
            st.image(img, width=100)
        with col2:
            vote = "Pozytywna" if prediction["is_vote_positive"] else "Negatywna"
            result = (
                "Kot" if prediction["predicted_class"] == cat_class_index else "Pies"
            )
            st.markdown(
                f"**Wynik:** {result}  \n**Data i czas:** {prediction['prediction_date_time']}  \n**Opinia:** {prediction['feedback']}  \n**Ocena:** {vote}"
            )
