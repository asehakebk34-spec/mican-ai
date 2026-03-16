import streamlit as st
import time
from datetime import datetime

# ==========================================
# 1. SİSTEM VE SAYFA AYARLARI (ULTRA MOD)
# ==========================================
st.set_page_config(
    page_title="Mican AI Ultra",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Arayüzü daha da havalı yapmak için özel tasarım (CSS) eklentisi
st.markdown("""
    <style>
    .stApp { border-top: 4px solid #00ffcc; }
    .ana-baslik { font-size: 40px; color: #00ffcc; font-weight: bold; text-shadow: 2px 2px 4px #000000; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SOL KONTROL PANELİ (ANA KUMANDA)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1786/1786159.png", width=100)
    st.markdown("## 🎛️ Ana Kumanda")
    st.write("Cihaz: **Samsung PC (Zırhlı Sürüm)**")
    
    st.markdown("---")
    st.markdown("### ⚙️ Zeka Ayarları")
    model_secim = st.radio("Aktif Çekirdek:", ["Mican Local (Hazır)", "Gemini Neural (Bağlanıyor...)"])
    hiz_ayar = st.slider("İşlemci Gücü (%)", 10, 100, 95)
    
    st.markdown("---")
    st.markdown("### 📊 Sistem Durumu")
    col1, col2 = st.columns(2)
    col1.metric("Sıcaklık", "42°C", "-2°C")
    col2.metric("RAM", "3.2 GB", "Stabil")
    
    if st.button("🚨 Sistemi Yeniden Başlat"):
        st.session_state.messages = []
        st.success("Hafıza temizlendi, sistem fırtına gibi!")
        time.sleep(1)
        st.rerun()

# ==========================================
# 3. ANA EKRAN VE SEKMELER (TABS)
# ==========================================
st.markdown('<p class="ana-baslik">⚡ Mican AI - Gelişmiş Komuta Merkezi</p>', unsafe_allow_html=True)

# Ekranı 3 farklı sayfaya bölüyoruz
tab1, tab2, tab3 = st.tabs(["💬 Yapay Zeka Sohbeti", "⏱️ 7. Sınıf Odaklanma Modu", "🛠️ İcat & Proje Planlayıcı"])

# --- TAB 1: SOHBET EKRANI ---
with tab1:
    st.info("Gardaş, şu an Local sürümdesin. Yakında buraya API anahtarını girip zekayı fulleyeceğiz!")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Sistemler devrede gardaş! Menülere bak, efsane oldu. Ne sormak istersin?"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Komut gir veya soru sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            mesaj_alani = st.empty()
            with st.spinner("Veritabanı taranıyor..."):
                time.sleep(1) # Düşünme efekti
            
            # Burada zekayı simüle ediyoruz
            if "lgs" in prompt.lower() or "ders" in prompt.lower():
                cevap = "Gardaş, 7. sınıftayız, temeli sağlam atma vakti. Yukarıdaki 'Odaklanma Modu' sekmesine geç, kronometreyi açıp çalışmaya başlayalım!"
            elif "kod" in prompt.lower() or "python" in prompt.lower():
                cevap = f"Yazdığın şey: '{prompt}'. Kodlama işleri bende! İstediğin projeyi yaz, mantığını kurayım."
            else:
                cevap = f"Gardaş, anlık olarak '%{hiz_ayar}' güçle çalışıyorum. '{prompt}' komutunu aldım. API bağlandığında buna destan gibi cevap yazacağım!"
            
            mesaj_alani.markdown(cevap)
            
        st.session_state.messages.append({"role": "assistant", "content": cevap})

# --- TAB 2: DERS ÇALIŞMA SAYACI ---
with tab2:
    st.header("⏱️ Odaklanma Modu")
    st.write("Sınavlara hazırlık ve projeler için Pomodoro sayacı.")
    
    dakika = st.number_input("Kaç dakika odaklanacaksın?", min_value=1, max_value=60, value=25)
    if st.button("▶️ Sayacı Başlat"):
        st.warning(f"Gardaş, tam {dakika} dakika dış dünyayla bağlantıyı kesiyoruz. Başarılar!")
        progress_text = "Zaman akıyor..."
        my_bar = st.progress(0, text=progress_text)
        
        for percent_complete in range(100):
            time.sleep((dakika * 60) / 100)
            my_bar.progress(percent_complete + 1, text=progress_text)
        st.success("Süre bitti gardaş! Çayını yudumlayabilirsin.")

# --- TAB 3: PROJE PLANLAYICI ---
with tab3:
    st.header("🛠️ Atölye Panosu")
    st.write("Burada yeni icatlarını (su pompası, ESP32 oyun konsolu, elektronik devreler vs.) not alabilirsin.")
    
    proje_adi = st.text_input("Proje Adı:")
    proje_detay = st.text_area("Gerekli Malzemeler ve Plan:")
    
    if st.button("💾 Projeyi Veritabanına Yaz"):
        if proje_adi:
            st.success(f"'{proje_adi}' projesi Samsung PC'nin diskine başarıyla kaydedildi! Donanım hazır olduğunda koda dökebiliriz.")
        else:
            st.error("Gardaş önce proje adını girmelisin!")

# Alt bilgi
st.markdown("---")
st.caption("© 2026 Mican AI Technologies | Eskişehir'den Dünyaya")
