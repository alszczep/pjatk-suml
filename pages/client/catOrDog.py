import streamlit as st

def run():
    st.title("Kot czy pies?")

    uploaded_file = st.file_uploader("Wgraj zdjęcie kota albo psa", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.write("To pewnie kot ale jeszcze nie wiadomo")
        review = st.text_input("Zostaw swoją opinię o wyniku, jest dla nas ważna!")
        downVote, upVote = st.columns(2)
        if downVote.button("Ocena pozytywna", icon="👍", use_container_width=True):
            setReview(review, True)

        if(upVote.button("Ocena negatywna", icon="👎", use_container_width=True)):
            setReview(review, False)


def setReview(review, mark):
    st.write("Dziękujemy za wystawioną opinię!")
    if(mark):
        st.write("Będziemy dalej się rozwijać")
    else:
        st.write("Obiecujemy poprawę jakości naszych usług")
