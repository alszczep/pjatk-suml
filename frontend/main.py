from frontendpages.admin import usageHistory
from frontendpages.client import catOrDog
import streamlit as st

pages = {
    "Klient": [
        st.Page(catOrDog.run, title="Kot czy pies?", default=True),
    ],
    "Admin": [
        st.Page(
            usageHistory.run,
            title="Historia użycia aplkiacji klienckiej",
            url_path="admin--usage-history",
        ),
    ],
}

pg = st.navigation(pages)
pg.run()
