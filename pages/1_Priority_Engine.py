import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import json
from shapely.geometry import shape
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
    # RENAME
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
    # CLEANING NUMERIC
    # =====================

    kolom_numeric = [
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


    for col in kolom_numeric:

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


    # hapus Indonesia kalau ada
# hapus agregat nasional
df = df[df["Provinsi"]!="INDONESIA"]


# hapus provinsi yang tidak ada di notebook
hapus_prov = [
    "PAPUA BARAT DAYA",
    "PAPUA TENGAH",
    "PAPUA PEGUNUNGAN",
    "PAPUA SELATAN"
]


df = df[
    ~df["Provinsi"].isin(hapus_prov)
]


df = df.reset_index(drop=True)


df = df.dropna()



    # =====================
    # FEATURE ENGINEERING
    # SESUAI COLAB
    # =====================

    df["Kemiskinan"] = (
        df["Miskin_Kota"] +
        df["Miskin_Desa"]
    ) / 2


    df["UHH"] = (
        df["UHH_L"] +
        df["UHH_P"]
    ) / 2


    # khusus internet
df["Internet"] = (
    df["Internet_Kota"] +
    df["Internet_Desa"]
) / 2


# sesuai notebook
df.loc[
    df["Provinsi"]=="DKI JAKARTA",
    "Internet"
] = df.loc[
    df["Provinsi"]=="DKI JAKARTA",
    "Internet_Kota"
]


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
    # LOG TRANSFORM PDRB
    # =====================

    df["PDRB"] = np.log1p(
        df["PDRB"]
    )

# =====================
# WINSORIZE 5%-95%
# sama notebook
# =====================

for col in fitur:

    batas_bawah = df[col].quantile(0.05)
    batas_atas = df[col].quantile(0.95)

    df[col] = df[col].clip(
        batas_bawah,
        batas_atas
    )
    # =====================
    # ROBUST SCALER
    # =====================

    scaler = RobustScaler()


    X = scaler.fit_transform(
        df[fitur]
    )


    # =====================
    # KMEANS
    # =====================

    model = KMeans(
        n_clusters=3,
        n_init=200,
        random_state=42
    )


    df["Cluster"] = model.fit_predict(X)



    # =====================
    # LABEL
    # =====================

    profile = (
        df.groupby("Cluster")
        [["PDRB","Kemiskinan"]]
        .mean()
    )


    maju = profile["PDRB"].idxmax()

    tertinggal = profile["Kemiskinan"].idxmax()



    def label_cluster(x):

        if x == maju:
            return "Maju"

        elif x == tertinggal:
            return "Tertinggal"

        return "Berkembang"



    df["Label"] = (
        df["Cluster"]
        .apply(label_cluster)
    )


    st.success(
        "Clustering berhasil"
    )



    # =====================
    # OUTPUT
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
    )



    # =====================
    # SCATTER
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
# PETA INDONESIA
# =====================

st.subheader(
    "Peta Persebaran Cluster Indonesia"
)


geo_url = (
"https://raw.githubusercontent.com/"
"williamedwardhahn/indonesia-geojson/"
"master/indonesia.geojson"
)


try:

    fig_map = px.choropleth(
        df,
        geojson=geo_url,
        locations="Provinsi",
        featureidkey="properties.Propinsi",
        color="Label",
        color_discrete_map={
            "Maju":"green",
            "Berkembang":"orange",
            "Tertinggal":"red"
        },
        title="Development Cluster Map"
    )


    fig_map.update_geos(
        fitbounds="locations",
        visible=False
    )


    st.plotly_chart(
        fig_map,
        use_container_width=True
    )


except Exception as e:

    st.warning(
        f"Peta belum tampil: {e}"
    )

    # =====================
    # PROFIL
    # =====================

    st.subheader(
        "Profil Cluster"
    )


    st.dataframe(
        df.groupby("Label")[fitur]
        .mean()
        .round(2)
    )



    # simpan untuk NUSA MATCH

    st.session_state["cluster_result"] = df
