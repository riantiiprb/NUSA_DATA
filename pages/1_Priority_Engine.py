import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json

from sklearn.preprocessing import RobustScaler
from sklearn.decomposition import PCA
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
    # RENAME
    # SAMA NOTEBOOK
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
    # HAPUS DATA
    # SAMA NOTEBOOK
    # =====================

    df = df[df["Provinsi"]!="INDONESIA"]


    hapus = [
        "PAPUA BARAT DAYA",
        "PAPUA TENGAH",
        "PAPUA PEGUNUNGAN",
        "PAPUA SELATAN"
    ]


    df = df[
        ~df["Provinsi"].isin(hapus)
    ]



    # =====================
    # CLEAN NUMERIC
    # DITAMBAHKAN AGAR STREAMLIT AMAN
    # =====================


    numeric = [
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


    for col in numeric:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%","")
            .str.replace(",","")
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


    # median imputation
    for col in numeric:
        df[col] = (
            df[col]
            .fillna(df[col].median())
        )



    # =====================
    # FEATURE ENGINEERING
    # SAMA NOTEBOOK
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



    # DKI adjustment
    dki = df["Provinsi"]=="DKI JAKARTA"

    df.loc[dki,"Internet"] = (
        df.loc[dki,"Internet_Kota"]
    )



    fitur = [
        "Kemiskinan",
        "Pengangguran",
        "PDRB",
        "HLS",
        "RLS",
        "UHH",
        "Sanitasi",
        "AirMinum",
        "Internet"
    ]



    # =====================
    # PREPROCESSING
    SAMA NOTEBOOK
    =====================


    df["PDRB"] = np.log1p(
        df["PDRB"]
    )



    # winsorize
    for col in fitur:

        low = df[col].quantile(0.05)
        high = df[col].quantile(0.95)

        df[col] = df[col].clip(
            low,
            high
        )



    scaler = RobustScaler()


    X = scaler.fit_transform(
        df[fitur]
    )



    # =====================
    # KMEANS
    =====================


    model = KMeans(
        n_clusters=3,
        n_init=200,
        random_state=42
    )


    df["Cluster"] = (
        model.fit_predict(X)
    )



    # =====================
    # LABEL
    SAMA NOTEBOOK
    =====================


    profile = (
        df.groupby("Cluster")
        [["PDRB","Kemiskinan"]]
        .mean()
    )


    maju = (
        profile["PDRB"]
        .idxmax()
    )


    tertinggal = (
        profile["Kemiskinan"]
        .idxmax()
    )


    def label(x):

        if x == maju:
            return "Maju"

        elif x == tertinggal:
            return "Tertinggal"

        else:
            return "Berkembang"



    df["Label"] = (
        df["Cluster"]
        .apply(label)
    )



    st.success(
        "Clustering berhasil"
    )



    # =====================
    # HASIL
    =====================


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
    )



    # =====================
    # SCATTER
    =====================


    pca = PCA(
        n_components=2
    )

    X_pca = pca.fit_transform(X)



    viz = pd.DataFrame(
        {
        "PC1":X_pca[:,0],
        "PC2":X_pca[:,1],
        "Provinsi":df["Provinsi"],
        "Label":df["Label"]
        }
    )



    fig = px.scatter(
        viz,
        x="PC1",
        y="PC2",
        color="Label",
        hover_name="Provinsi",
        title="Cluster Development Indonesia"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )



    # =====================
    # PROFILING
    =====================


    st.subheader(
        "Profil Cluster"
    )


    st.dataframe(
        df.groupby("Label")[fitur]
        .mean()
        .round(2)
    )



    # =====================
    # PETA
    =====================


    st.subheader(
        "Peta Prioritas Pembangunan"
    )


    try:

        geo = open(
            "indonesia-map-geojson (1).json"
        )

        geojson = json.load(geo)


        st.map(
            df,
            latitude=None,
            longitude=None
        )


        st.info(
        "GeoJSON siap diintegrasikan untuk pewarnaan provinsi berdasarkan Label"
        )


    except:

        st.warning(
        "File GeoJSON belum masuk ke folder app"
        )



    # simpan

    st.session_state["cluster_result"] = df
