import streamlit as st
import time

try:
    import google.generativeai as genai
except ImportError:
    st.error("Gardaş requirements.txt dosyasında google-generativeai eksik!")

# ==========================================
# ⚙️ SAYFA VE HAFIZA
# ==========================================
st.set_page_config(page_title="Mican AI Premium", page_icon="🚀", layout="wide")

if "giris" not in st.session_state:
    st.session_state.giris = False
if "isim" not in st.session_state:
    st.session_state.isim = ""
if "foto" not in st.session_state:
    st.session_state.foto = None
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{"role": "assistant", "content": "Gardaş hoş geldin! Sol menüden yeni şifreni gir, sistemi ateşle."}]
if "program" not in st.session_state:
    st.session_state.program = ""
if "api_sifresi" not in st.session_state:
    st.session_state.api_sifresi = ""

# ==========================================
# 🔐 GİRİŞ EKRANI
# ==========================================
if not st.session_state.giris:
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 Mican AI VIP Merkezi</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        eposta = st.text_input("📧 E-Posta Adresiniz:")
        sifre = st.text_input("🔑 Güvenlik Şifreniz:", type="password")
        
        if st.button("Sistemleri Ateşle! 🔥", use_container_width=True):
            if "@" in eposta and len(sifre) >= 4:
                st.session_state.giris = True
                st.session_state.isim = eposta.split("@")[0].capitalize()
                st.success("Güvenlik duvarı aşıldı! İçeri giriyorsun...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Geçerli e-posta ve en az 4 haneli şifre gir!")
    st.stop()

# ==========================================
# 📱 SOL MENÜ VE YENİ ŞİFRE GİRİŞİ
# ==========================================
with st.sidebar:
    st.title("👤 Profilim")
    
    if st.session_state.foto:
        st.image(st.session_state.foto, width=150)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=150)
    
    yuklenen = st.file_uploader("🖼️ Fotoğraf Yükle", type=["png", "jpg", "jpeg"])
    if yuklenen is not None:
        st.session_state.foto = yuklenen.getvalue()
        st.rerun()
        
    st.markdown("---")
    st.title("🧠 Zeka Motoru Bağlantısı")
    st.warning("Google eski şifreyi iptal etti. Lütfen YENİ aldığın şifreyi buraya gir:")
    
    # ŞİFRE BURADAN GİRİLECEK!
    yeni_sifre = st.text_input("Yeni API Şifresi:", type="password", value=st.session_state.api_sifresi)
    if yeni_sifre != st.session_state.api_sifresi:
        st.session_state.api_sifresi = yeni_sifre
        st.rerun()

    if st.session_state.api_sifresi.startswith("AIza"):
        genai.configure(api_key=st.session_state.api_sifresi)
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.success("🟢 Zeka: SÜPER AKTİF")
    else:
        model = None
        st.error("🔴 Zeka: KAPALI (Şifre Bekleniyor)")
        
    st.markdown("---")
    if st.button("🚪 Çıkış Yap"):
        st.session_state.giris = False
        st.rerun()

# ==========================================
# 💎 ANA EKRAN SEKMELERİ
# ==========================================
st.title(f"🌌 Mican AI - Ultra Yönetim Paneli")

tab1, tab2, tab3 = st.tabs(["💬 Yapay Zeka", "📚 Ders Programı", "🛠️ İcat Atölyesi"])

# --- SEKME 1: GERÇEK SOHBET ---
with tab1:
    for msg in st.session_state.mesajlar:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("İstediğini sor gardaş..."):
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
                        st.error(f"Bağlantı koptu. Hata: {e}")
            else:
                st.error("Gardaş sol menüden o yeni şifreyi girmedin!")

# --- SEKME 2: PROGRAM ---
with tab2:
    st.header("🎯 Sana Özel Çalışma Programı")
    sinif = st.selectbox("Kaçıncı Sınıfsın?", ["Sınıf Seç...", "7. Sınıf", "8. Sınıf (LGS)"])
    if sinif != "Sınıf Seç...":
        if st.button("✨ Bana Program Hazırla", use_container_width=True):
            if model:
                with st.spinner("Program çiziliyor..."):
                    try:
                        st.session_state.program = model.generate_content(f"Ben {sinif} öğrencisiyim. Bana ders çalışmam için çok detaylı çalışma programı hazırla.").text
                    except:
                        st.error("Hata oluştu.")
            else:
                st.error("Şifre eksik!")
        
        if st.session_state.program != "":
            st.write(st.session_state.program)

# --- SEKME 3: İCAT ---
with tab3:
    st.header("🛠️ İcat Atölyesi")
    malzemeler = st.text_area("Elindeki Malzemeler:")
    if st.button("🚀 Ne Yapabilirim?"):
        if model and malzemeler:
            with st.spinner("Projeler bulunuyor..."):
                try:
                    st.write(model.generate_content(f"Şu malzemelerle ne icat edebilirim: {malzemeler}").text)
                except:
                    st.error("Hata oluştu.")
        else:
            st.warning("Eksik bilgi veya şifre yok.")
