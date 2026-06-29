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


le = joblib.load(
    os.path.join(
        BASE_DIR,
        "label_encoder (1).pkl"
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
    'yg','nya','dgn','utk','dr','pd','tsb',
    'dll','krn','jg','sdh','tlg','kmrn',
    'spt','lg','udh','bgt','jd','sy',
    'mohon','tolong','terima','kasih',
    'bapak','ibu','pak','bu',
    'terkait','mengenai','perihal',
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


    text = ' '.join(
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
    # NLP PREDICTION
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


    data["Prediksi Isu"] = (
        le.inverse_transform(
            prediction
        )
    )



    # =====================
    # OUTPUT
    # =====================

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


    # jumlah isu

    issue_count = (
        data["Prediksi Isu"]
        .value_counts()
        .reset_index()
    )

    issue_count.columns = [
        "Isu",
        "Jumlah"
    ]



    left,right = st.columns(2)



    with left:

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



    with right:

        st.subheader(
            "Isu Dominan"
        )


        for i in issue_count.head(5)["Isu"]:
            st.info(i)



    # untuk integrasi priority engine

    st.session_state["top_issue"] = (
        issue_count.iloc[0]["Isu"]
    )



else:

    st.warning(
        "Upload dataset aspirasi terlebih dahulu"
    )
