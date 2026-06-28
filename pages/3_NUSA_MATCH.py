import streamlit as st


st.title(
"NUSA MATCH"
)


st.subheader(
"AI Policy Recommendation Engine"
)


st.write(
"""
Mengintegrasikan hasil:
- Development Priority Engine
- Citizen Voice Intelligence

untuk menghasilkan rekomendasi program.
"""
)


# input hasil analisis

cluster = st.selectbox(
"Cluster Wilayah",
[
"Prioritas Tinggi",
"Berkembang",
"Stabil"
]
)


issue = st.selectbox(
"Isu Dominan Masyarakat",
[
"Kemiskinan",
"Pengangguran",
"Infrastruktur",
"Pendidikan",
"Kesehatan",
"UMKM"
]
)



# AI decision engine sederhana

if cluster=="Prioritas Tinggi":


    score=90


elif cluster=="Berkembang":

    score=65


else:

    score=40



# tambah bobot NLP

if issue in [
    "Kemiskinan",
    "Pengangguran",
    "Infrastruktur"
]:

    score +=10



st.metric(
"AI Priority Score",
f"{score}/100"
)



st.divider()



st.subheader(
"AI Recommendation"
)



if score >=80:


    hasil=f"""
Wilayah memiliki prioritas pembangunan tinggi.

Berdasarkan:
- Cluster pembangunan: {cluster}
- Isu masyarakat: {issue}

Rekomendasi:

✓ Program peningkatan ekonomi masyarakat

✓ Pelatihan keterampilan kerja

✓ Penguatan layanan publik

✓ Monitoring pembangunan wilayah

"""


elif score>=50:


    hasil=f"""
Wilayah membutuhkan penguatan pembangunan.

Fokus:

✓ Peningkatan kualitas SDM

✓ Pengembangan infrastruktur

✓ Digitalisasi layanan publik

"""


else:


    hasil=f"""
Wilayah relatif stabil.

Fokus:

✓ Inovasi pembangunan

✓ Pemeliharaan layanan

✓ Peningkatan daya saing
"""



st.success(
hasil
)