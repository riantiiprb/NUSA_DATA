import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.preprocessing import RobustScaler
from sklearn.cluster import KMeans


st.set_page_config(
    page_title="Development Priority",
    layout="wide"
)


st.title("NUSA DATA - Development Priority Engine")


file = st.file_uploader(
    "Upload Dataset Pembangunan",
    type=["csv","xlsx"]
)



if file:

    # =====================
    # LOAD DATA
    # =====================

    if file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)


    st.subheader("Dataset Pembangunan")

    st.dataframe(df.head())


    # =====================
    # RENAME SESUAI DATASET
    # =====================

    df.columns = [
        "Provinsi",
        "Miskin_Kota",
        "Miskin_Desa",
        "Pengangguran",
        "PDRB",
        "HLS",
        "RLS",
        "UHH_L",
        "UHH_P",
        "Sanitasi",
        "AirMinum",
        "Internet_Kota",
        "Internet_Desa"
    ]



    # =====================
    # FEATURE ENGINEERING
    # sama seperti notebook
    # =====================

    df["Kemiskinan"] = (
        df["Miskin_Kota"] +
        df["Miskin_Desa"]
    ) / 2


    df["UHH"] = (
        df["UHH_L"] +
        df["UHH_P"]
    ) / 2


    df["Internet"] = (
        df["Internet_Kota"] +
        df["Internet_Desa"]
    ) / 2



    fitur = [
        "Kemiskinan",
        "Pengangguran",
        "PDRB",
        "RLS",
        "UHH",
        "Sanitasi",
        "AirMinum",
        "Internet"
    ]


    for col in fitur:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    df = df.dropna()



    # =====================
    # TRANSFORM PDRB
    # sama notebook
    # =====================

    df["PDRB"] = np.log1p(
        df["PDRB"]
    )



    # =====================
    # SCALING
    # =====================

    scaler = RobustScaler()


    X = scaler.fit_transform(
        df[fitur]
    )



    # =====================
    # KMEANS K=3
    # =====================

    model = KMeans(
        n_clusters=3,
        n_init=100,
        random_state=42
    )


    df["Cluster"] = model.fit_predict(X)



    # =====================
    # LABEL CLUSTER
    # sesuai notebook
    # =====================


    cluster_profile = (
        df.groupby("Cluster")
        [["PDRB","Kemiskinan"]]
        .mean()
    )


    # PDRB tertinggi = maju
    maju = (
        cluster_profile["PDRB"]
        .idxmax()
    )


    tertinggal = (
        cluster_profile["Kemiskinan"]
        .idxmax()
    )


    def label_cluster(x):

        if x == maju:
            return "Maju"

        elif x == tertinggal:
            return "Tertinggal"

        else:
            return "Berkembang"



    df["Label"] = (
        df["Cluster"]
        .apply(label_cluster)
    )


    st.success(
        "Clustering pembangunan berhasil"
    )



    # =====================
    # HASIL
    # =====================


    st.subheader(
        "Hasil Segmentasi Wilayah"
    )


    st.dataframe(
        df[
            [
            "Provinsi",
            "Label"
            ]
        ]
        .sort_values("Label")
    )



    # =====================
    # VISUAL
    # =====================


    fig = px.scatter(
        df,
        x="Kemiskinan",
        y="PDRB",
        color="Label",
        hover_name="Provinsi",
        title="Development Cluster Indonesia"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # =====================
    # PROFIL CLUSTER
    # =====================


    st.subheader(
        "Profil Rata-rata Cluster"
    )


    profile = (
        df.groupby("Label")[fitur]
        .mean()
        .round(2)
    )


    st.dataframe(profile)



    # simpan untuk modul lain

    st.session_state["cluster_result"] = df
