import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.express as px


st.set_page_config(
    page_title="Citizen Voice Intelligence",
    layout="wide"
)


st.title("Citizen Voice Intelligence")

model = joblib.load(
    os.path.join(
        os.path.dirname(__file__),
        "nlp_model.pkl"
    )
)

tfidf = joblib.load(
    os.path.join(
        os.path.dirname(__file__),
        "tfidf.pkl"
    )
)

le = joblib.load(
    os.path.join(
        os.path.dirname(__file__),
        "label_encoder.pkl"
    )
)



st.write(
"""
Analisis aspirasi masyarakat menggunakan 
Natural Language Processing (NLP)
untuk mengidentifikasi isu publik.
"""
)


# =====================
# UPLOAD
# =====================

file = st.file_uploader(
    "Upload Data Aspirasi Masyarakat",
    type=["csv"]
)


if file:

    data = pd.read_csv(file)


    st.subheader("Preview Data")

    st.dataframe(
        data.head()
    )


    # pilih kolom teks
    kolom_teks = st.selectbox(
        "Pilih kolom aspirasi",
        data.columns
    )


    # =====================
    # CLEANING
    # =====================

    text = (
        data[kolom_teks]
        .dropna()
        .astype(str)
    )


    st.metric(
        "Jumlah Aspirasi",
        len(text)
    )



    # =====================
    # NLP TF-IDF
    # =====================


    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=30
    )


    tfidf = vectorizer.fit_transform(
        text
    )


    score = (
        tfidf
        .mean(axis=0)
        .A1
    )


    keywords = pd.DataFrame(
        {
            "Keyword":
            vectorizer.get_feature_names_out(),

            "Score":
            score
        }
    )


    keywords = keywords.sort_values(
        "Score",
        ascending=False
    )


    # =====================
    # OUTPUT
    # =====================


    left,right = st.columns(2)



    with left:

        st.subheader(
            "Top Keyword Aspirasi"
        )


        fig = px.bar(
            keywords.head(10),
            x="Score",
            y="Keyword",
            orientation="h"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )



    with right:

        st.subheader(
            "Isu Dominan"
        )


        for k in keywords.head(5)["Keyword"]:
            st.info(k)



    # simpan untuk NUSA MATCH

    st.session_state["top_issue"] = (
        keywords.iloc[0]["Keyword"]
    )



else:

    st.warning(
        "Upload dataset aspirasi terlebih dahulu"
    )
