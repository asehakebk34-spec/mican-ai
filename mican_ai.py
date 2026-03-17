import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mican AI Ultra", page_icon="🚀", layout="wide")

# --- ZEKA MOTORU BAĞLANTISI ---
# Şifreyi Streamlit Secrets'tan (o gizli kasadan) çekiyoruz
try:
    # Kasadaki ismin 'api_sifresi' olduğundan emin ol gardaş
    api_key = st.secrets["api_sifresi"]
    genai.configure(api_key=api_key)
    # 404 hatası vermeyen en sağlam model:
    model = genai.GenerativeModel('gemini-1.5-flash')
    zeka_aktif = True
except Exception as e:
    zeka_aktif = False
    hata_mesaji = str(e)

# --- HAFIZA ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Gardaş selam! Ben Mican AI. Tüm sistemlerim senin için hazır!"}]

# --- GİRİŞ EKRANI ---
if "giris" not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.title("🚀 Mican AI VIP Giriş")
    eposta = st.text_input("E-Posta:")
    sifre = st.text_input("Şifre:", type="password")
    if st.button("Sistemi Aç"):
        if "@" in eposta and len(sifre) >= 3:
            st.session_state.giris = True
            st.rerun()
    st.stop()

# --- ANA EKRAN ---
with st.sidebar:
    st.title("👤 Profilim")
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.write(f"Hoş geldin gardaş!")
    st.markdown("---")
    if zeka_aktif:
        st.success("🟢 Zeka: AKTİF")
    else:
        st.error("🔴 Zeka: KAPALI")
        st.info("Secrets (Gizli Kasa) kısmına api_sifresi eklediğinden emin ol!")

tab1, tab2, tab3 = st.tabs(["💬 Sohbet", "📚 Program", "🛠️ Atölye"])

with tab1:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Sorunu sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            if zeka_aktif:
                try:
                    response = model.generate_content(prompt)
                    cevap = response.text
                    st.write(cevap)
                    st.session_state.messages.append({"role": "assistant", "content": cevap})
                except:
                    st.error("Bağlantı hatası! Şifreni kontrol et.")
            else:
                st.warning("Şu an cevap veremiyorum, sistem kapalı.")

with tab2:
    st.header("🎯 7. Sınıf Programı")
    if st.button("Program Hazırla"):
        st.write("16:00 - Dinlenme\n17:00 - Ders Tekrarı\n19:00 - Ödevler\n21:00 - Kitap Okuma")

with tab3:
    st.header("🛠️ İcat Atölyesi")
    st.write("Elindeki malzemeleri yaz, projeni bulayım!")
