import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


st.title("Development Priority Engine")


file = st.file_uploader(
    "Upload Data Pembangunan",
    type=["csv"]
)


if file:

    pembangunan = pd.read_csv(file)


    st.subheader("Data Pembangunan")

    st.dataframe(
        pembangunan.head()
    )


    fitur = [
        "Persentase Penduduk Miskin (P0) Menurut Provinsi dan Daerah (Persen), 2025 Perkotaan",
        "Tingkat Pengangguran Terbuka Menurut Provinsi (Persen), 2025",
        "Rata-rata Lama Sekolah (Tahun), 2025"
    ]


    for col in fitur:

        pembangunan[col] = pd.to_numeric(
            pembangunan[col],
            errors="coerce"
        )


    pembangunan = pembangunan.dropna(
        subset=fitur
    )


    scaler = StandardScaler()


    X = scaler.fit_transform(
        pembangunan[fitur]
    )


    model = KMeans(
        n_clusters=3,
        random_state=42
    )


    pembangunan["Cluster"] = model.fit_predict(X)


    st.success(
        "Clustering berhasil"
    )


    fig = px.scatter(
        pembangunan,
        x=fitur[0],
        y=fitur[1],
        color="Cluster",
        hover_name="Provinsi"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )