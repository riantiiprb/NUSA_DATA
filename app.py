import streamlit as st


st.set_page_config(
page_title="NUSA DATA",
layout="wide"
)
st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
    135deg,
    #eef6ff,
    #ffffff
    );
}


.main-title{
    font-size:55px;
    font-weight:800;
    color:#0f172a;
}


.subtitle{
    font-size:22px;
    color:#475569;
}


.card{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0px 8px 25px rgba(0,0,0,0.08);
    height:180px;
}


</style>
""",
unsafe_allow_html=True)


st.markdown(
"""
<div class="main-title">
NUSA DATA
</div>

<div class="subtitle">
National Unified Statistics and Development Analytics
</div>

""",
unsafe_allow_html=True
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
