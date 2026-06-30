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
