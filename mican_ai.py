import streamlit as st
import time
import google.generativeai as genai

# ==========================================
# 🧠 ÇOK GİZLİ BEYİN ŞİFRESİ (KİMSE GÖRMEYECEK)
# ==========================================
# GARDAŞ, AIza İLE BAŞLAYAN O UZUN ŞİFREYİ AŞAĞIDAKİ TIRNAKLARIN İÇİNE YAPŞTIR:
BEYIN_SIFRESI = "AIzaSyBoR2QbQv7GHDa0dBv6xidla7QnJTLXLXc"

# Şifre kontrolü ve zekayı başlatma
if BEYIN_SIFRESI != "AIzaSyBoR2QbQv7GHDa0dBv6xidla7QnJTLXLXc" and len(BEYIN_SIFRESI) > 10:
    genai.configure(api_key=BEYIN_SIFRESI)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

# ==========================================
# ⚙️ SAYFA TASARIMI VE HAFIZA
# ==========================================
st.set_page_config(page_title="Mican AI Premium", page_icon="🌌", layout="wide")

if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
if "kullanici_adi" not in st.session_state:
    st.session_state.kullanici_adi = ""
if "profil_fotosu" not in st.session_state:
    st.session_state.profil_fotosu = None
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{"role": "assistant", "content": "Hoş geldin gardaş! Zeka sistemim devrede. Ne sormak istersin?"}]
if "calisma_programi" not in st.session_state:
    st.session_state.calisma_programi = ""

# ==========================================
# 🔐 1. GİRİŞ VE KAYIT EKRANI (İLK KARŞILAMA)
# ==========================================
if not st.session_state.giris_yapildi:
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>✨ Mican AI Hoş Geldiniz</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Sisteme erişmek için lütfen giriş yapın veya kayıt olun.</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        islem = st.radio("İşlem Seçiniz:", ["Giriş Yap", "Yeni Kayıt Ol"])
        eposta = st.text_input("📧 E-Posta Adresiniz:")
        sifre = st.text_input("🔑 Şifreniz:", type="password")
        
        if st.button("🚀 Sistemi Başlat", use_container_width=True):
            if "@" in eposta and len(sifre) > 3:
                st.session_state.giris_yapildi = True
                st.session_state.kullanici_adi = eposta.split("@")[0] # E-postanın başını isim yapar
                st.success("Giriş Başarılı! Premium Özellikler Açılıyor...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Gardaş lütfen geçerli bir e-posta ve en az 4 haneli şifre gir!")
    st.stop() # Giriş yapılmadıysa aşağıyı gösterme

# ==========================================
# 📱 2. SOL MENÜ (AYARLAR VE PROFİL)
# ==========================================
with st.sidebar:
    st.title("👤 Profil & Ayarlar")
    
    # Profil Fotoğrafı Alanı
    if st.session_state.profil_fotosu:
        st.image(st.session_state.profil_fotosu, width=150, caption=f"Kullanıcı: {st.session_state.kullanici_adi}")
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150, caption="Fotoğraf Yok")
    
    st.markdown("### 🖼️ Galeriye Eriş")
    yuklenen_foto = st.file_uploader("Profil Fotoğrafı Seç", type=["png", "jpg", "jpeg"])
    if yuklenen_foto is not None:
        st.session_state.profil_fotosu = yuklenen_foto.getvalue()
        st.success("Profil fotoğrafı güncellendi!")
        time.sleep(1)
        st.rerun()
        
    st.markdown("---")
    st.markdown("### ⚙️ Sistem Durumu")
    if model:
        st.success("🟢 Zeka Motoru: AKTİF")
    else:
        st.error("🔴 Zeka Motoru: KAPALI (Kodun içindeki şifreyi kontrol et)")
        
    if st.button("🚪 Çıkış Yap"):
        st.session_state.giris_yapildi = False
        st.rerun()

# ==========================================
# 💎 3. ANA EKRAN VE SEKMELER
# ==========================================
st.title(f"🌌 Mican AI - Premium Sürüm (Kullanıcı: {st.session_state.kullanici_adi})")

tab1, tab2 = st.tabs(["💬 Yapay Zeka Sohbeti", "📚 Akıllı Çalışma Programı Üretici"])

# --- TAB 1: SOHBET EKRANI ---
with tab1:
    for msg in st.session_state.mesajlar:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("İstediğin her şeyi buraya yazabilirsin..."):
        st.session_state.mesajlar.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if model:
                with st.spinner("Mican Düşünüyor..."):
                    try:
                        cevap = model.generate_content(prompt).text
                        st.markdown(cevap)
                        st.session_state.mesajlar.append({"role": "assistant", "content": cevap})
                    except Exception as e:
                        st.error("Bağlantı koptu, tekrar dene gardaş.")
            else:
                st.error("Zeka motoru kapalı! Kodun içine o AIza ile başlayan şifreyi yapıştırmayı unuttun.")

# --- TAB 2: SINIF SEÇMELİ DERS PROGRAMI ÜRETİCİ ---
with tab2:
    st.header("🎯 Sana Özel Akıllı Çalışma Programı")
    st.write("Kaçıncı sınıfsın? Seçimini yap, sana en uygun 2 farklı programı hazırlayayım.")
    
    secilen_sinif = st.selectbox("Sınıfını Seç:", ["Seçim Yapınız...", "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf (YKS)"])
    
    if secilen_sinif != "Seçim Yapınız...":
        colA, colB = st.columns(2)
        
        with colA:
            if st.button("✨ Bana 2 Tane Program Hazırla", use_container_width=True):
                if model:
                    with st.spinner(f"{secilen_sinif} için efsane programlar yazılıyor..."):
                        soru = f"Ben {secilen_sinif} öğrencisiyim. Bana ders çalışmam için 2 farklı, çok detaylı ve motive edici günlük çalışma programı hazırla. Samimi bir dil kullan."
                        st.session_state.calisma_programi = model.generate_content(soru).text
                else:
                    st.error("Şifre eksik gardaş!")
                    
        with colB:
            if st.session_state.calisma_programi != "":
                if st.button("👎 Beğenmedim, Yenisini Ver!", use_container_width=True):
                    with st.spinner("Hemen değiştiriyorum gardaş, bekle..."):
                        soru = f"Ben {secilen_sinif} öğrencisiyim. Önceki verdiğin programları beğenmedim. Bana TAMAMEN FARKLI, yepyeni 2 tane daha günlük çalışma programı hazırla."
                        st.session_state.calisma_programi = model.generate_content(soru).text
        
        if st.session_state.calisma_programi != "":
            st.markdown("---")
            st.markdown("### 📋 İşte Senin Programların:")
            st.write(st.session_state.calisma_programi)
