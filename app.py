import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Load API Key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Judul Aplikasi
st.title("📊 AI Perhitungan Rasio Keuangan")
st.write("Masukkan data keuangan untuk menghitung rasio secara otomatis.")

# Input data keuangan
st.subheader("Input Data Keuangan")
try:
    aset_lancar = float(st.number_input("Aset Lancar", min_value=0.0))
    kewajiban_lancar = float(st.number_input("Kewajiban Lancar", min_value=0.0))
    total_hutang = float(st.number_input("Total Hutang", min_value=0.0))
    total_aset = float(st.number_input("Total Aset", min_value=0.0))
    laba_bersih = float(st.number_input("Laba Bersih", min_value=0.0))
    ekuitas = float(st.number_input("Ekuitas", min_value=0.0))

    if st.button("Hitung Rasio"):
        hasil = {
            "Current Ratio": aset_lancar / kewajiban_lancar if kewajiban_lancar else 0,
            "Debt to Asset Ratio": total_hutang / total_aset if total_aset else 0,
            "Return on Equity": laba_bersih / ekuitas if ekuitas else 0
        }

        st.subheader("📌 Hasil Perhitungan Rasio")
        for k, v in hasil.items():
            st.write(f"**{k}:** {v:.2f}")

        # Kirim hasil ke AI Groq untuk analisis
        prompt = f"""
        Jelaskan hasil rasio keuangan berikut dengan bahasa mudah:
        Current Ratio: {hasil['Current Ratio']:.2f}
        Debt to Asset Ratio: {hasil['Debt to Asset Ratio']:.2f}
        Return on Equity: {hasil['Return on Equity']:.2f}

        Berikan analisis lengkap seperti konsultan keuangan.
        """

        response = client.chat.completions.create(
