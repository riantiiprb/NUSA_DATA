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


st.title("Development Priority Engine")



file = st.file_uploader(
    "Upload Data Pembangunan",
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



    st.subheader(
        "Dataset Pembangunan"
    )

    st.dataframe(
        df.head()
    )



    # =====================
    # RENAME KOLOM
    # SESUAI DATASET TEMANMU
    # =====================

    df = df.rename(columns={

        df.columns[0]:"Provinsi",
        df.columns[1]:"Kemiskinan",
        df.columns[2]:"Pengangguran",
        df.columns[3]:"PDRB",
        df.columns[4]:"RLS",
        df.columns[5]:"Sanitasi",
        df.columns[6]:"AirMinum",
        df.columns[7]:"Internet"

    })



    fitur = [
        "Kemiskinan",
        "Pengangguran",
        "PDRB",
        "RLS",
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
    # ROBUST SCALER
    # (punya temanmu)
    # =====================


    scaler = RobustScaler()


    X = scaler.fit_transform(
        df[fitur]
    )



    # =====================
    # KMEANS K=2
    # =====================


    model = KMeans(
        n_clusters=2,
        n_init=100,
        random_state=42
    )


    df["Cluster"] = (
        model.fit_predict(X)
    )



    # =====================
    # LABELING
    Maju/Tertinggal
    # =====================


    rata = (
        df.groupby("Cluster")
        ["PDRB"]
        .mean()
    )


    cluster_maju = (
        rata.idxmax()
    )


    df["Label"] = np.where(
        df["Cluster"]==cluster_maju,
        "Maju",
        "Tertinggal"
    )



    st.success(
        "Clustering berhasil"
    )



    # =====================
    # OUTPUT
    # =====================


    st.subheader(
        "Hasil Prioritas"
    )


    st.dataframe(
        df[
            [
            "Provinsi",
            "Label"
            ]
        ]
    )



    fig = px.scatter(
        df,
        x="Kemiskinan",
        y="PDRB",
        color="Label",
        hover_name="Provinsi",
        title="Cluster Provinsi"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    st.session_state["cluster_result"] = df
