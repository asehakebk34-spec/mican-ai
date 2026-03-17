import streamlit as st
import google.generativeai as genai
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mican AI Ultra", page_icon="🚀", layout="wide")

# --- AKILLI MODEL SEÇİCİ ---
if "model_ismi" not in st.session_state:
    st.session_state.model_ismi = None

def model_bul():
    try:
        api_key = st.secrets["api_sifresi"]
        genai.configure(api_key=api_key)
        # Mevcut modelleri listele ve çalışan ilk modeli seç
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
        return None
    except:
        return None

# --- ZEKA MOTORU BAĞLANTISI ---
try:
    if not st.session_state.model_ismi:
        st.session_state.model_ismi = model_bul()
    
    if st.session_state.model_ismi:
        model = genai.GenerativeModel(st.session_state.model_ismi)
        zeka_aktif = True
    else:
        zeka_aktif = False
except:
    zeka_aktif = False

# --- HAFIZA VE GİRİŞ ---
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
        st.success(f"🟢 Zeka: AKTİF ({st.session_state.model_ismi})")
    else:
        st.error("🔴 Zeka: KAPALI")
        st.info("Lütfen Secrets (Gizli Kasa) kısmını kontrol et!")

tab1, tab2, tab3 = st.tabs(["💬 Sohbet", "📚 Program", "🛠️ Atölye"])

with tab1:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])

    if prompt := st.chat_input("İstediğini sor, sistem otomatik bağlanacak..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        
        with st.chat_message("assistant"):
            if zeka_aktif:
                try:
                    response = model.generate_content(prompt)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {str(e)}")
            else:
                st.warning("Zeka motoru şu an meşgul veya şifre hatalı.")

with tab2:
    st.header("🎯 7. Sınıf Programı")
    if st.button("Program Önerisi Al"):
        st.write("1. 17:00 - Ödevler\n2. 19:00 - Akşam Yemeği\n3. 20:00 - 45dk Matematik\n4. 21:00 - Kitap Okuma")

with tab3:
    st.header("🛠️ İcat Atölyesi")
    st.write("Gardaş, ESP32 ve motorlarla efsane projeler yapabiliriz!")
