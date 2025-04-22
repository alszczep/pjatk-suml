import streamlit as st

from model.model import train_or_load_model
from pages.client import catOrDog
from pages.admin import manageDataSet, usageHistory

model = train_or_load_model()

pages = {
    "Klient": [
        st.Page(catOrDog.mkRun(model), title="Kot czy pies?", default=True),
    ],
    "Admin": [
        st.Page(manageDataSet.run, title="Zarządzanie zestawem danych", url_path="admin--manage-data-set"),
        st.Page(usageHistory.run, title="Historia użycia aplkiacji klienckiej", url_path="admin--usage-history"),
    ],
}

pg = st.navigation(pages)
pg.run()
