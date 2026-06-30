import streamlit as st


st.title(
"NUSA MATCH"
)

st.subheader(
"Policy Recommendation Matching System"
)



cluster = st.selectbox(
"Karakteristik Wilayah",
[
"Tertinggal",
"Berkembang",
"Maju"
]
)


issue = st.selectbox(
"Isu Prioritas Masyarakat",
[
"Kemiskinan",
"Pengangguran",
"Infrastruktur",
"Pendidikan",
"Kesehatan",
"UMKM"
]
)



st.divider()



st.subheader(
"Rekomendasi Program"
)



if cluster=="Tertinggal":


    if issue=="Kemiskinan":

        rekomendasi = """
Prioritas:
Peningkatan kesejahteraan masyarakat

Program yang direkomendasikan:

✓ Bantuan sosial tepat sasaran

✓ Pemberdayaan ekonomi masyarakat

✓ Penguatan UMKM lokal
"""


    elif issue=="Pengangguran":

        rekomendasi="""
Prioritas:
Peningkatan kesempatan kerja

Program:

✓ Pelatihan keterampilan kerja

✓ Program peningkatan kompetensi

✓ Pendampingan pencari kerja
"""


    else:

        rekomendasi="""
Prioritas:
Penguatan layanan dasar wilayah

Program:

✓ Pembangunan infrastruktur

✓ Peningkatan kualitas pelayanan publik
"""



elif cluster=="Berkembang":


    rekomendasi="""
Prioritas:
Penguatan pembangunan wilayah

Program:

✓ Digitalisasi layanan

✓ Pengembangan ekonomi lokal

✓ Peningkatan kualitas SDM
"""



else:


    rekomendasi="""
Prioritas:
Optimalisasi pembangunan

Program:

✓ Inovasi pelayanan publik

✓ Peningkatan daya saing daerah

✓ Pemeliharaan fasilitas publik
"""



st.success(rekomendasi)
