import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Load API Key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Judul Aplikasi
st.title("📊 Aplikasi AI Perhitungan Rasio Keuangan")
st.write("Masukkan data untuk menghitung rasio keuangan secara otomatis dan mendapatkan analisis AI.")

# Input Data
st.subheader("Input Data Keuangan")

aset_lancar = st.number_input("Aset Lancar", min_value=0.0)
kewajiban_lancar = st.number_input("Kewajiban Lancar", min_value=0.0)
total_hutang = st.number_input("Total Hutang", min_value=0.0)
total_aset = st.number_input("Total Aset", min_value=0.0)
laba_bersih = st.number_input("Laba Bersih", min_value=0.0)
ekuitas = st.number_input("Ekuitas", min_value=0.0)

if st.button("Hitung Rasio"):
    
    # Menghindari pembagian 0
    current_ratio = aset_lancar / kewajiban_lancar if kewajiban_lancar > 0 else 0
    debt_asset_ratio = total_hutang / total_aset if total_aset > 0 else 0
    roe = laba_bersih / ekuitas if ekuitas > 0 else 0

    hasil = {
        "Current Ratio": current_ratio,
        "Debt to Asset Ratio": debt_asset_ratio,
        "Return on Equity (ROE)": roe
    }

    # Tampilkan hasil rasio
    st.subheader("📌 Hasil Perhitungan Rasio Keuangan")
    for nama, nilai in hasil.items():
        st.write(f"**{nama} :** {nilai:.2f}")

    # Buat prompt untuk AI
    prompt = f"""
    Analisis rasio keuangan berikut:

    - Current Ratio: {current_ratio:.2f}
    - Debt to Asset Ratio: {debt_asset_ratio:.2f}
    - Return on Equity (ROE): {roe:.2f}

    Berikan penjelasan dengan bahasa yang mudah dipahami, interpretasi kesehatan keuangan, dan rekomendasi.
    """

    # Panggil AI Groq (format terbaru)
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Ambil hasil AI
    ai_reply = response.choices[0].message.content

    st.subheader("🤖 Analisis AI")
    st.write(ai_reply)
