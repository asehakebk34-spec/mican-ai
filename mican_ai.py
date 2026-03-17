import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mican AI Ultra", page_icon="🚀", layout="wide")

# --- ZEKA MOTORU BAĞLANTISI ---
try:
    # Gizli Kasadan (Secrets) şifreyi çekiyoruz
    api_key = st.secrets["api_sifresi"]
    genai.configure(api_key=api_key)
    # GARDAŞ, 404 HATASINI ÇÖZEN ASIL MODEL İSMİ BUDUR:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    zeka_aktif = True
except Exception as e:
    zeka_aktif = False

# --- HAFIZA VE GİRİŞ SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "giris" not in st.session_state:
    st.session_state.giris = False

if not st.session_state.giris:
    st.title("🚀 Mican AI VIP Giriş")
    eposta = st.text_input("E-Posta:")
    sifre = st.text_input("Şifre:", type="password")
    if st.button("Sistemi Aç"):
        if "@" in eposta:
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

tab1, tab2, tab3 = st.tabs(["💬 Sohbet", "📚 Program", "🛠️ Atölye"])

with tab1:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("Sorunu sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            if zeka_aktif:
                try:
                    # CEVAP ÜRETME
                    response = model.generate_content(prompt)
                    cevap = response.text
                    st.write(cevap)
                    st.session_state.messages.append({"role": "assistant", "content": cevap})
                except Exception as e:
                    st.error(f"HATA OLUŞTU: {str(e)}")
            else:
                st.warning("Zeka motoru bağlı değil!")

with tab2:
    st.header("🎯 7. Sınıf Çalışma Düzenleyici")
    if st.button("Bana 2 Program Hazırla"):
        if zeka_aktif:
            try:
                res = model.generate_content("Ben 7. sınıf öğrencisiyim, bana 2 farklı çalışma programı yap.")
                st.write(res.text)
            except:
                st.error("Program üretilirken hata oluştu.")

with tab3:
    st.header("🛠️ İcat Atölyesi")
    if st.button("Proje Öner"):
        st.write("Gardaş, elindeki ESP32 ile akıllı ev sistemi kurabilirsin!")
