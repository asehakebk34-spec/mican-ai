import streamlit as st
import time

try:
    import google.generativeai as genai
except ImportError:
    st.error("Sistem hatası: google-generativeai kütüphanesi bulunamadı!")

# ==========================================
# 🧠 1. ÇOK GİZLİ BEYİN ŞİFRESİ (TEK YER)
# ==========================================
# GARDAŞ, AIza İLE BAŞLAYAN ŞİFREYİ SADECE BURADAKİ TIRNAKLARIN İÇİNE YAPŞTIR:
BEYIN_SIFRESI = "AIzaSyBoR2QbQv7GHDa0dBv6xidla7QnJTLXLXc"

if len(BEYIN_SIFRESI) > 20:
    genai.configure(api_key=BEYIN_SIFRESI)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# ==========================================
# ⚙️ 2. SAYFA VE HAFIZA AYARLARI
# ==========================================
st.set_page_config(page_title="Mican AI Ultra Premium", page_icon="🚀", layout="wide")

# Tüm hafıza (Session State) değişkenleri
if "giris" not in st.session_state:
    st.session_state.giris = False
if "isim" not in st.session_state:
    st.session_state.isim = ""
if "foto" not in st.session_state:
    st.session_state.foto = None
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{"role": "assistant", "content": "Gardaş hoş geldin! Ben Mican AI. Tüm sistemlerim tam kapasite aktif!"}]
if "program" not in st.session_state:
    st.session_state.program = ""
if "tema_rengi" not in st.session_state:
    st.session_state.tema_rengi = "#000000"

# Tema Rengi Uygulama
st.markdown(f"""
    <style>
    .stApp {{ border-top: 5px solid {st.session_state.tema_rengi}; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 3. GİRİŞ VE KAYIT EKRANI (VIP KAPI)
# ==========================================
if not st.session_state.giris:
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 Mican AI Ultra VIP Merkezi</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🔒 Sisteme erişmek için kayıt olun veya giriş yapın.")
        islem = st.radio("İşlem Türü:", ["Sisteme Giriş Yap", "Yeni Hesap Aç"])
        
        eposta = st.text_input("📧 E-Posta Adresiniz:")
        sifre = st.text_input("🔑 Güvenlik Şifreniz:", type="password")
        
        if st.button("Sistemleri Ateşle! 🔥", use_container_width=True):
            if "@" in eposta and len(sifre) >= 4:
                st.session_state.giris = True
                st.session_state.isim = eposta.split("@")[0].capitalize()
                st.success("Güvenlik duvarı aşıldı! İçeri giriyorsun gardaş...")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("HATA: E-posta adresinde '@' olmalı ve şifre en az 4 hane olmalı!")
    st.stop()

# ==========================================
# 📱 4. SOL KONTROL MENÜSÜ VE PROFİL
# ==========================================
with st.sidebar:
    st.title("👤 VIP Profilim")
    
    # Galeri ve Fotoğraf
    if st.session_state.foto:
        st.image(st.session_state.foto, width=150, caption=f"VIP: {st.session_state.isim}")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150, caption="Fotoğraf Bekleniyor")
    
    yuklenen = st.file_uploader("🖼️ Galeriden Fotoğraf Yükle", type=["png", "jpg", "jpeg"])
    if yuklenen is not None:
        st.session_state.foto = yuklenen.getvalue()
        st.success("Profil efsane oldu!")
        time.sleep(1)
        st.rerun()
        
    st.markdown("---")
    st.title("⚙️ Ekstra Özellikler")
    
    # Tema Ayarı
    yeni_renk = st.color_picker("🎨 Sitenin Üst Çizgi Rengini Seç", st.session_state.tema_rengi)
    if yeni_renk != st.session_state.tema_rengi:
        st.session_state.tema_rengi = yeni_renk
        st.rerun()

    # Zeka Durumu
    if model:
        st.success("🟢 Zeka: SÜPER AKTİF")
    else:
        st.error("🔴 Zeka: KAPALI (10. Satırdaki şifreyi kontrol et)")
        
    st.markdown("---")
    if st.button("🚪 Sistemi Kapat (Çıkış)"):
        st.session_state.giris = False
        st.rerun()

# ==========================================
# 💎 5. ANA EKRAN VE DEVASA SEKMELER
# ==========================================
st.title(f"🌌 Mican AI - Ultra Yönetim Paneli")
st.caption(f"Hoş geldin, {st.session_state.isim}. Bütün sistemler emrine amade.")

# 4 Tane sekme ekledik!
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Yapay Zeka", 
    "📚 Akıllı Ders Programı", 
    "🛠️ İcat & Proje Atölyesi", 
    "⏱️ Odaklanma Modu"
])

# --- SEKME 1: SOHBET EKRANI ---
with tab1:
    for msg in st.session_state.mesajlar:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Dünyanın en zor sorusunu buraya yaz gardaş..."):
        st.session_state.mesajlar.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if model:
                with st.spinner("Beyin fırtınası yapılıyor..."):
                    try:
                        cevap = model.generate_content(prompt).text
                        st.markdown(cevap)
                        st.session_state.mesajlar.append({"role": "assistant", "content": cevap})
                    except Exception as e:
                        st.error("Bağlantı hatası gardaş. Google sunucuları yoğun olabilir.")
            else:
                st.error("10. satıra şifreyi girmedin gardaş!")

# --- SEKME 2: SINIF SEÇMELİ PROGRAM VE DISLIKE TUŞU ---
with tab2:
    st.header("🎯 Sana Özel 2 Farklı Çalışma Programı")
    st.write("Sınıfını seç, sana saniyesinde özel 2 tane program çıkarayım.")
    
    sinif = st.selectbox("Kaçıncı Sınıfsın?", ["Sınıf Seç...", "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf (YKS)"])
    
    if sinif != "Sınıf Seç...":
        colA, colB = st.columns(2)
        
        with colA:
            if st.button("✨ Bana 2 Efsane Program Hazırla", use_container_width=True):
                if model:
                    with st.spinner(f"{sinif} için programlar çiziliyor..."):
                        soru = f"Ben {sinif} öğrencisiyim. Bana ders çalışmam için 2 farklı, saat saat planlanmış detaylı çalışma programı hazırla. Samimi bir dil kullan."
                        st.session_state.program = model.generate_content(soru).text
                else:
                    st.error("Şifre eksik!")
                    
        with colB:
            if st.session_state.program != "":
                # DISLIKE TUŞU BURADA!
                if st.button("👎 Bunları Hiç Beğenmedim, Başka Ver!", use_container_width=True):
                    with st.spinner("Hemen çöpe atıp 2 yepyeni program yazıyorum..."):
                        soru = f"Ben {sinif} öğrencisiyim. Önceki verdiğin çalışma programlarını hiç beğenmedim. Bana TAMAMEN FARKLI, esnek ve yepyeni 2 tane daha günlük çalışma programı hazırla."
                        st.session_state.program = model.generate_content(soru).text
        
        if st.session_state.program != "":
            st.markdown("---")
            st.success("✅ Alttaki programlardan sana uyanı seç gardaş!")
            st.write(st.session_state.program)

# --- SEKME 3: İCAT VE PROJE ATÖLYESİ (EKSTRA ÖZELLİK) ---
with tab3:
    st.header("🛠️ Elektronik ve Yazılım Atölyesi")
    st.write("Gardaş elindeki malzemeleri yaz, bu malzemelerle yapabileceğin en manyak mühendislik icatlarını sana adım adım anlatayım!")
    malzemeler = st.text_area("Elindeki Malzemeler (Örn: ESP32, kablo, ekran, motor, pil...)", height=100)
    
    if st.button("🚀 Bu Malzemelerle Ne Yapabilirim?"):
        if model and malzemeler:
            with st.spinner("Malzemeler analiz ediliyor, efsane projeler bulunuyor..."):
                icat_sorusu = f"Elimde şu malzemeler var: {malzemeler}. Lütfen bu malzemelerle yapabileceğim çok yaratıcı 2 farklı elektronik/mekanik kendin-yap (DIY) projesi öner. Adım adım anlat."
                st.write(model.generate_content(icat_sorusu).text)
        elif not malzemeler:
            st.warning("Gardaş malzemeleri yazmayı unuttun!")

# --- SEKME 4: ODAKLANMA SAYACI (EKSTRA ÖZELLİK) ---
with tab4:
    st.header("⏱️ Derse Odaklanma Modu (Pomodoro)")
    st.write("Dikkatini dağıtan her şeyi kapat, süreyi başlat ve kampa gir!")
    dakika = st.slider("Kaç Dakika Çalışacaksın?", 10, 120, 40)
    
    if st.button("⏳ Sayacı Başlat"):
        st.warning(f"Dikkat! {dakika} dakika dış dünyayla iletişim kesildi. Kolay gelsin!")
        bar = st.progress(0)
        for i in range(100):
            time.sleep((dakika * 60) / 100)
            bar.progress(i + 1)
        st.success("Helal olsun gardaş! Süre bitti, artık mola verebilirsin.")
