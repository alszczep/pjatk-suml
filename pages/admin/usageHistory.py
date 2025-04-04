import streamlit as st
import pandas as pd
import json
from PIL import Image

def run():
    st.title("Historia użycia aplikacji klienckiej")
    json_data = '''
    [
        {"result": "Dobrze - przewidziano kota", "responseTime": 100,"userReview": "Mój kot to najlepszy zwierzak na świecie", "userMark": "👍", "photo": "pages/admin/images/cat1.jpg"},
        {"result": "Dobrze - przewidziano kota", "responseTime": 15,"userReview": "Ale kocur hehe", "userMark": "👍", "photo": "pages/admin/images/cat2.jpg"},
        {"result": "Źle - przewidziano psa", "responseTime": 10000,"userReview": "Działa jak zwykle, czyli nie działa", "userMark": "👎", "photo": "pages/admin/images/cat3.jpg"},
        {"result": "Dobrze - przewidziano psa", "responseTime": 200,"userReview": "Mój pies odrazu został rozpoznany", "userMark": "👍",  "photo": "pages/admin/images/dog1.jpg"}
    ]
    '''

    # Parsujemy JSON
    data = json.loads(json_data)

    # Dla każdego rekordu wyświetlamy dane + zdjęcie
    st.markdown("### MODEL_1_PSY_KOTY 👤Akcje użytkowników:")

    for item in data:
        col1, col2 = st.columns([1, 3])
        with col1:
            img = Image.open(item["photo"])
            st.image(img, width=100)
        with col2:
            st.markdown(f"**Wynik:** {item['result']}  \n**Czas odpowiedzi (ms):** {item['responseTime']}  \n**Opinia:** {item['userReview']}  \n**Ocena:** {item['userMark']}")
