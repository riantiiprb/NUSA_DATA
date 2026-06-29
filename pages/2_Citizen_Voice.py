import streamlit as st
import pandas as pd
import joblib
import os
import re
import string
import plotly.express as px


st.set_page_config(
    page_title="Citizen Voice Intelligence",
    layout="wide"
)


st.title("Citizen Voice Intelligence")


# =====================
# LOAD MODEL
# =====================

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)


model = joblib.load(
    os.path.join(
        BASE_DIR,
        "model_linear_svm.pkl"
    )
)


tfidf = joblib.load(
    os.path.join(
        BASE_DIR,
        "tfidf_vectorizer.pkl"
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
# PREPROCESS
# =====================

sw_set = set([
    'yg','nya','dgn','utk','dr','pd',
    'tsb','dll','krn','jg','sdh',
    'tlg','kmrn','udh','bgt','jd',
    'mohon','tolong','terima','kasih',
    'warga','masyarakat',
    'pemerintah','dinas'
])


def preprocess(text):

    text = str(text).lower()

    text = re.sub(
        r'<[^>]+>',
        ' ',
        text
    )

    text = re.sub(
        r'http\S+|www\S+',
        ' ',
        text
    )

    text = re.sub(
        r'\d+',
        ' ',
        text
    )

    text = text.translate(
        str.maketrans(
            '',
            '',
            string.punctuation
        )
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()


    text = " ".join(
        w for w in text.split()
        if w not in sw_set
    )

    return text



# =====================
# UPLOAD
# =====================

file = st.file_uploader(
    "Upload Data Aspirasi Masyarakat",
    type=["csv"]
)



if file:

    data = pd.read_csv(file)


    st.subheader(
        "Preview Data"
    )

    st.dataframe(
        data.head()
    )


    kolom_teks = st.selectbox(
        "Pilih kolom aspirasi",
        data.columns
    )


    st.metric(
        "Jumlah Aspirasi",
        len(data)
    )


    # =====================
    # NLP MODEL
    # =====================

    data["clean"] = (
        data[kolom_teks]
        .fillna("")
        .apply(preprocess)
    )


    X = tfidf.transform(
        data["clean"]
    )


    prediction = model.predict(X)


    # Linear SVM langsung keluar label
    data["Prediksi Isu"] = prediction



    st.subheader(
        "Hasil Klasifikasi Isu"
    )


    st.dataframe(
        data[
            [
                kolom_teks,
                "Prediksi Isu"
            ]
        ]
    )



    # =====================
    # DASHBOARD
    # =====================


    issue_count = (
        data["Prediksi Isu"]
        .value_counts()
        .reset_index()
    )


    issue_count.columns = [
        "Isu",
        "Jumlah"
    ]



    col1,col2 = st.columns(2)



    with col1:

        st.subheader(
            "Distribusi Isu"
        )

        fig = px.bar(
            issue_count,
            x="Jumlah",
            y="Isu",
            orientation="h"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )



    with col2:

        st.subheader(
            "Isu Prioritas"
        )

        for i in issue_count.head(5)["Isu"]:
            st.info(i)


else:

    st.warning(
        "Upload dataset aspirasi terlebih dahulu"
    )
