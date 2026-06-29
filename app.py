import streamlit as st


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


/* tulisan menu sidebar */
[data-testid="stSidebar"] *{
    color:white;
}


/* hover menu */
[data-testid="stSidebarNavLink"]:hover{
    background-color:#2563eb;
    border-radius:10px;
}


/* menu aktif */
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
