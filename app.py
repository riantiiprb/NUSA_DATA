import streamlit as st
import pandas as pd
import joblib
import os


st.set_page_config(
    page_title="NUSA DATA",
    layout="wide"
)


# =====================
# CSS DESIGN
# =====================

st.markdown("""
<style>

/* sidebar background */
[data-testid="stSidebar"]{
    background:
    linear-gradient(
    180deg,
    #0f172a,
    #1e3a8a
    );
}


[data-testid="stSidebar"] *{
    color:white;
}


[data-testid="stSidebarNavLink"]:hover{
    background-color:#2563eb;
    border-radius:10px;
}


[data-testid="stSidebarNavLink"][aria-current="page"]{
    background-color:#3b82f6;
    border-radius:10px;
}


</style>
""",
unsafe_allow_html=True)



st.subheader(
"National Unified Statistics and Development Analytics"
)



# =====================
# DATA UPLOAD
# =====================

st.header("Upload Dataset")


pembangunan = st.file_uploader(
    "Dataset Pembangunan (BPS)",
    type=["csv","xlsx"],
    key="upload_pembangunan"
)


aspirasi = st.file_uploader(
    "Dataset Aspirasi Masyarakat",
    type=["csv","xlsx"],
    key="upload_aspirasi"
)



if pembangunan:

    if pembangunan.name.endswith(".xlsx"):
        df_pembangunan = pd.read_excel(pembangunan)

    else:
        df_pembangunan = pd.read_csv(pembangunan)


    st.session_state["pembangunan"] = df_pembangunan


    st.success(
        "Dataset pembangunan tersimpan"
    )



if aspirasi:

    if aspirasi.name.endswith(".xlsx"):
        df_aspirasi = pd.read_excel(aspirasi)

    else:
        df_aspirasi = pd.read_csv(aspirasi)


    st.session_state["aspirasi"] = df_aspirasi


    st.success(
        "Dataset aspirasi tersimpan"
    )



# =====================
# CARD KAMU TETAP
# =====================

a,b,c = st.columns(3)


with a:
    st.info(
    "Development Priority Engine"
    )


with b:
    st.info(
    "Citizen Voice Intelligence"
    )


with c:
    st.info(
    "NUSA MATCH"
    )
