import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Rasio Keuangan", page_icon="📊")

# ======================
# GROQ CLIENT
# ======================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("📊 AI Perhitungan & Analisis Rasio Keuangan")

st.write("Masukkan data keuangan perusahaan, lalu AI akan menghitung dan memberikan analisis otomatis.")


# ======================
# INPUT DATA
# ======================
col1, col2 = st.columns(2)

with col1:
    aset_lancar = st.number_input("Aset Lancar", min_value=0.0, step=1000.0)
    persediaan = st.number_input("Persediaan", min_value=0.0, step=1000.0)

with col2:
    kewajiban_lancar = st.number_input("Kewajiban Lancar", min_value=0.0, step=1000.0)
    penjualan = st.number_input("Penjualan", min_value=0.0, step=1000.0)
    total_aset = st.number_input("Total Aset", min_value=0.0, step=1000.0)


# ======================
# HITUNG RASIO
# ======================
if st.button("Hitung & Analisis AI"):

    try:
        current_ratio = aset_lancar / kewajiban_lancar if kewajiban_lancar != 0 else 0
        quick_ratio = (aset_lancar - persediaan) / kewajiban_lancar if kewajiban_lancar != 0 else 0
        total_asset_turnover = penjualan / total_aset if total_aset != 0 else 0

        st.subheader("📌 Hasil Perhitungan Rasio")
        st.write(f"**Current Ratio:** {current_ratio:.2f}")
        st.write(f"**Quick Ratio:** {quick_ratio:.2f}")
        st.write(f"**Total Asset Turnover:** {total_asset_turnover:.2f}")

        # ======================
        # PROMPT AI
        # ======================
        prompt = f"""
        Analisislah rasio keuangan berikut:

        1. Current Ratio: {current_ratio:.2f}
        2. Quick Ratio: {quick_ratio:.2f}
        3. Total Asset Turnover: {total_asset_turnover:.2f}

        Berikan analisis profesional mencakup:
        - Kesehatan likuiditas
        - Efisiensi penggunaan aset
        - Risiko keuangan
        - Rekomendasi perbaikan

        Buat dengan bahasa yang mudah dipahami.
        """

        # ======================
        # PANGGIL AI GROQ
        # ======================
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Kamu adalah analis keuangan profesional."},
                {"role": "user", "content": prompt}
            ]
        )

        # ======================
        # AMBIL HASIL DENGAN CARA BENAR
        # ======================
        ai_answer = response.choices[0].message.content

        st.subheader("🤖 Analisis AI")
        st.write(ai_answer)

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
