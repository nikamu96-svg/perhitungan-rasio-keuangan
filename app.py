import streamlit as st
from groq import Groq

# ==========================
# KONFIGURASI API KEY
# ==========================
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

client = Groq(api_key=GROQ_API_KEY)

# ==========================
# TITLE APLIKASI
# ==========================
st.title("📊 AI Perhitungan Rasio Keuangan Mahasiswa")

st.write("Masukkan data laporan keuangan, lalu AI akan menghitung rasio dan memberikan analisis otomatis.")

# ==========================
# INPUT DATA
# ==========================
st.header("Input Data Keuangan")

try:
    aset_lancar = float(st.number_input("Aset Lancar", min_value=0.0))
    kewajiban_lancar = float(st.number_input("Kewajiban Lancar", min_value=0.0))
    laba_bersih = float(st.number_input("Laba Bersih", min_value=0.0))
    penjualan = float(st.number_input("Penjualan", min_value=0.0))
    total_aset = float(st.number_input("Total Aset", min_value=0.0))
except:
    st.error("Pastikan semua input berupa angka.")
    st.stop()

if st.button("Hitung Rasio dan Analisis AI"):
    
    # ==========================
    # PERHITUNGAN RASIO
    # ==========================
    try:
        current_ratio = aset_lancar / kewajiban_lancar if kewajiban_lancar != 0 else 0
        net_profit_margin = laba_bersih / penjualan if penjualan != 0 else 0
        roa = laba_bersih / total_aset if total_aset != 0 else 0
    except:
        st.error("Terjadi kesalahan dalam perhitungan.")
        st.stop()

    # Tampilkan hasil perhitungan
    st.subheader("📘 Hasil Perhitungan Rasio")
    st.write(f"**Current Ratio:** {current_ratio:.2f}")
    st.write(f"**Net Profit Margin:** {net_profit_margin:.2f}")
    st.write(f"**Return on Assets (ROA):** {roa:.2f}")

    # ==========================
    # PANGGIL AI UNTUK ANALISIS
    # ==========================
    prompt = f"""
    Berikut adalah rasio keuangan yang telah dihitung:

    Current Ratio: {current_ratio:.2f}
    Net Profit Margin: {net_profit_margin:.2f}
    ROA: {roa:.2f}

    Tolong berikan analisis lengkap dan mudah dipahami mengenai:
    - Kesehatan likuiditas perusahaan
    - Efisiensi operasional
    - Kemampuan menghasilkan laba
    - Saran perbaikan berdasarkan angka di atas

    Jelaskan dengan gaya yang ringkas namun jelas.
    """

   response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Kamu analis keuangan profesional."},
        {"role": "user", "content": prompt}
    ]
)

# Ambil hasil dengan cara yang benar
hasil = response.choices[0].message.content
st.write(hasil)

        ai_output = response.choices[0].message["content"]

        st.subheader("🤖 Analisis AI")
        st.write(ai_output)

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memanggil AI: {e}")
