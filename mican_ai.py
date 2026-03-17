import streamlit as st
import time

try:
    import google.generativeai as genai
except ImportError:
    st.error("Gardaş 'google-generativeai' eksik, requirements.txt dosyasını kontrol et!")

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Mican AI VIP", page_icon="🔥", layout="wide")

# --- HAFIZA (SESSION STATE) AYARLARI ---
if "giris_yapildi" not in st.session_state:
    st.session_state.giris_yapildi = False
if "eposta" not in st.session_state:
    st.session_state.eposta = ""
if "profil_fotosu" not in st.session_state:
    st.session_state.profil_fotosu = None
if "api_anahtari" not in st.session_state:
    st.session_state.api_anahtari = ""
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{"role": "assistant", "content": "Gardaş hoş geldin! Ben Mican AI. Beynimi taktın mı?"}]
if "calisma_programlari" not in st.session_state:
    st.session_state.calisma_programlari = ""

# ==========================================
# 1. GİRİŞ VE KAYIT EKRANI (KİLİT SİSTEMİ)
# ==========================================
if not st.session_state.giris_yapildi:
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🌌 Mican AI Güvenlik Kapısı</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Sisteme erişmek için kayıt ol veya giriş yap.")
        islem = st.radio("Ne yapmak istersin?", ["Giriş Yap", "Yeni Kayıt Ol"])
        
        girilen_eposta = st.text_input("📧 E-Posta Adresin:")
        girilen_sifre = st.text_input("🔑 Şifren:", type="password")
        
        if st.button("🚀 Sisteme Dalış Yap!", use_container_width=True):
            if "@" in girilen_eposta and len(girilen_sifre) > 3:
                st.session_state.giris_yapildi = True
                st.session_state.eposta = girilen_eposta
                st.success("Kapılar açılıyor gardaş, bekle...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("E-posta veya şifre hatalı! Geçerli bir şeyler yaz.")
    st.stop() # Giriş yapılmadıysa aşağıdakileri GÖSTERME

# ==========================================
# 2. SOL MENÜ (PROFİL, API VE AYARLAR)
# ==========================================
with st.sidebar:
    st.title("👤 Profilim")
    
    # Profil Fotoğrafı Gösterme
    if st.session_state.profil_fotosu:
        st.image(st.session_state.profil_fotosu, width=150, caption=st.session_state.eposta)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150, caption="Profil Fotosu Yok")
    
    st.markdown("---")
    st.title("⚙️ Ayarlar & Zeka Bağlantısı")
    
    # Gerçek Zeka Şifresi
    yeni_api = st.text_input("🧠 API Anahtarını Buraya Gir:", type="password", value=st.session_state.api_anahtari)
    if yeni_api != st.session_state.api_anahtari:
        st.session_state.api_anahtari = yeni_api
        st.success("Zeka şifresi hafızaya alındı!")
    
    if st.session_state.api_anahtari:
        genai.configure(api_key=st.session_state.api_anahtari)
        model = genai.GenerativeModel('gemini-pro')
        st.caption("🟢 Sistem Durumu: SÜPER ZEKİ")
    else:
        model = None
        st.caption("🔴 Sistem Durumu: BEYİN BEKLENİYOR")

    st.markdown("---")
    st.subheader("🖼️ Profil Fotoğrafı Değiştir")
    yuklenen_foto = st.file_uploader("Galeriden bir fotoğraf seç", type=["png", "jpg", "jpeg"])
    if yuklenen_foto is not None:
        st.session_state.profil_fotosu = yuklenen_foto.getvalue()
        st.success("Fotoğraf güncellendi!")
    
    st.markdown("---")
    if st.button("🚪 Hesaptan Çıkış Yap"):
        st.session_state.giris_yapildi = False
        st.rerun()

# ==========================================
# 3. ANA EKRAN SEKMELERİ
# ==========================================
st.title("🔥 Mican AI - Premium Zeka Merkezi")
tab1, tab2 = st.tabs(["💬 Yapay Zeka ile Sohbet", "📚 Akıllı Çalışma Programı Üretici"])

# --- TAB 1: GERÇEK SOHBET ---
with tab1:
    for msg in st.session_state.mesajlar:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Gardaş, aklındaki her soruyu buraya yaz..."):
        st.session_state.mesajlar.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            mesaj_alani = st.empty()
            if not st.session_state.api_anahtari:
                cevap = "Gardaş sol menüye o kopyaladığın uzun şifreyi (API Anahtarını) yapıştırmadın! Şifreyi gir ki sana gerçek cevaplar verebileyim."
                mesaj_alani.markdown(cevap)
                st.session_state.mesajlar.append({"role": "assistant", "content": cevap})
            else:
                with st.spinner("Mican AI Derin Düşünüyor..."):
                    try:
                        response = model.generate_content(prompt)
                        cevap = response.text
                        mesaj_alani.markdown(cevap)
                        st.session_state.mesajlar.append({"role": "assistant", "content": cevap})
                    except Exception as e:
                        mesaj_alani.error("Gardaş şifreyi yanlış girmiş olabilirsin veya internet koptu.")

# --- TAB 2: SINIFINA ÖZEL ÇALIŞMA PROGRAMI (BEĞENMEME TUŞLU) ---
with tab2:
    st.header("🎯 Sana Özel Çalışma Programı Üretici")
    st.write("Kaçıncı sınıfsın gardaş? Söyle, sana efsane 2 tane program çıkarayım.")
    
    secilen_sinif = st.selectbox("Sınıfını Seç:", ["5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf (YKS)"], index=2)
    
    colA, colB = st.columns(2)
    
    with colA:
        if st.button("✨ Bana 2 Tane Program Çıkar"):
            if not st.session_state.api_anahtari:
                st.error("Sol menüden API şifreni girmelisin!")
            else:
                with st.spinner("Sana özel efsane programlar yazılıyor..."):
                    try:
                        soru = f"Ben {secilen_sinif} öğrencisiyim. Bana ders çalışmam için 2 farklı ve çok detaylı günlük çalışma programı hazırla. Samimi bir dil kullan."
                        cevap = model.generate_content(soru).text
                        st.session_state.calisma_programlari = cevap
                    except:
                        st.error("Program üretilirken hata oluştu.")
                        
    with colB:
        if st.session_state.calisma_programlari != "":
            if st.button("👎 Bunları Beğenmedim, Yeni 2 Tane Ver!"):
                with st.spinner("Hemen değiştiriyorum gardaş, bekle..."):
                    try:
                        soru = f"Ben {secilen_sinif} öğrencisiyim. Önceki verdiğin çalışma programlarını hiç beğenmedim. Bana TAMAMEN FARKLI, yepyeni 2 tane daha günlük çalışma programı hazırla."
                        cevap = model.generate_content(soru).text
                        st.session_state.calisma_programlari = cevap
                    except:
                        st.error("Yeni program üretilirken hata oluştu.")

    if st.session_state.calisma_programlari != "":
        st.markdown("---")
        st.markdown("### 📋 İşte Programların:")
        st.write(st.session_state.calisma_programlari)
