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
    # GARDAŞ BAK BURAYI EN YENİ VE HIZLI MODELLE DEĞİŞTİRDİM:
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# ==========================================
# ⚙️ 2. SAYFA VE HAFIZA AYARLARI
# ==========================================
st.set_page_config(page_title="Mican AI Ultra Premium", page_icon="🚀", layout="wide")

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

st.markdown(f"""
    <style>
    .stApp {{ border-top: 5px solid {st.session_state.tema_rengi}; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 3. GİRİŞ EKRANI
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
# 📱 4. SOL MENÜ
# ==========================================
with st.sidebar:
    st.title("👤 VIP Profilim")
    
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
    
    yeni_renk = st.color_picker("🎨 Sitenin Üst Çizgi Rengini Seç", st.session_state.tema_rengi)
    if yeni_renk != st.session_state.tema_rengi:
        st.session_state.tema_rengi = yeni_renk
        st.rerun()

    if model:
        st.success("🟢 Zeka: SÜPER AKTİF")
    else:
        st.error("🔴 Zeka: KAPALI (14. Satırdaki şifreyi kontrol et)")
        
    st.markdown("---")
    if st.button("🚪 Sistemi Kapat (Çıkış)"):
        st.session_state.giris = False
        st.rerun()

# ==========================================
# 💎 5. ANA EKRAN SEKMELERİ
# ==========================================
st.title(f"🌌 Mican AI - Ultra Yönetim Paneli")

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Yapay Zeka", 
    "📚 Akıllı Ders Programı", 
    "🛠️ İcat & Proje Atölyesi", 
    "⏱️ Odaklanma Modu"
])

# --- SEKME 1: SOHBET ---
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
                        # GERÇEK HATAYI BURADA GÖRECEĞİZ!
                        st.error(f"Gardaş Google ile bağlantıda bir sorun çıktı. Hata detayı şu: {e}")
            else:
                st.error("14. satıra şifreyi girmedin gardaş!")

# --- SEKME 2: PROGRAM ---
with tab2:
    st.header("🎯 Sana Özel 2 Farklı Çalışma Programı")
    sinif = st.selectbox("Kaçıncı Sınıfsın?", ["Sınıf Seç...", "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf (YKS)"])
    
    if sinif != "Sınıf Seç...":
        colA, colB = st.columns(2)
        with colA:
            if st.button("✨ Bana 2 Efsane Program Hazırla", use_container_width=True):
                if model:
                    with st.spinner(f"{sinif} için programlar çiziliyor..."):
                        try:
                            soru = f"Ben {sinif} öğrencisiyim. Bana ders çalışmam için 2 farklı, detaylı çalışma programı hazırla. Samimi bir dil kullan."
                            st.session_state.program = model.generate_content(soru).text
                        except Exception as e:
                            st.error(f"Hata: {e}")
                else:
                    st.error("Şifre eksik!")
        with colB:
            if st.session_state.program != "":
                if st.button("👎 Bunları Hiç Beğenmedim, Başka Ver!", use_container_width=True):
                    with st.spinner("Hemen çöpe atıp 2 yepyeni program yazıyorum..."):
                        try:
                            soru = f"Ben {sinif} öğrencisiyim. Önceki verdiğin çalışma programlarını hiç beğenmedim. Bana TAMAMEN FARKLI, esnek ve yepyeni 2 tane daha günlük çalışma programı hazırla."
                            st.session_state.program = model.generate_content(soru).text
                        except Exception as e:
                            st.error(f"Hata: {e}")
        
        if st.session_state.program != "":
            st.markdown("---")
            st.write(st.session_state.program)

# --- SEKME 3: İCAT ---
with tab3:
    st.header("🛠️ Elektronik ve Yazılım Atölyesi")
    malzemeler = st.text_area("Elindeki Malzemeler (Örn: ESP32, kablo, ekran...)", height=100)
    if st.button("🚀 Bu Malzemelerle Ne Yapabilirim?"):
        if model and malzemeler:
            with st.spinner("Projeler bulunuyor..."):
                try:
                    icat_sorusu = f"Elimde şu malzemeler var: {malzemeler}. Lütfen bu malzemelerle yapabileceğim çok yaratıcı 2 farklı kendin-yap (DIY) projesi öner. Adım adım anlat."
                    st.write(model.generate_content(icat_sorusu).text)
                except Exception as e:
                    st.error(f"Hata: {e}")
        elif not malzemeler:
            st.warning("Gardaş malzemeleri yazmayı unuttun!")

# --- SEKME 4: ODAKLANMA ---
with tab4:
    st.header("⏱️ Derse Odaklanma Modu (Pomodoro)")
    dakika = st.slider("Kaç Dakika Çalışacaksın?", 10, 120, 40)
    if st.button("⏳ Sayacı Başlat"):
        st.warning(f"Dikkat! {dakika} dakika dış dünyayla iletişim kesildi. Kolay gelsin!")
        bar = st.progress(0)
        for i in range(100):
            time.sleep((dakika * 60) / 100)
            bar.progress(i + 1)
        st.success("Süre bitti, mola verebilirsin.")
