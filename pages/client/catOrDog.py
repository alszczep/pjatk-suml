import streamlit as st

def run():
    st.title("Kot czy pies?")

    uploaded_file = st.file_uploader("Wgraj zdjęcie kota albo psa", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.write("To pewnie kot ale jeszcze nie wiadomo")
