import streamlit as st


st.set_page_config(
page_title="NUSA DATA",
layout="wide"
)


st.title(
"NUSA DATA"
)


st.subheader(
"National Unified Statistics and Development Analytics"
)


st.write(
"""
Platform AI untuk integrasi:

📊 Data pembangunan

💬 Aspirasi masyarakat

🤖 Rekomendasi kebijakan

"""
)


a,b,c = st.columns(3)


with a:
    st.info(
    "Development Priority Engine\n\nClustering wilayah"
    )


with b:
    st.info(
    "Citizen Voice Intelligence\n\nNLP aspirasi"
    )


with c:
    st.info(
    "NUSA MATCH\n\nAI Recommendation"
    )