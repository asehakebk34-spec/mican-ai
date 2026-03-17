import streamlit as st
import time

try:
    import google.generativeai as genai
except ImportError:
    st.error("Requirements eksik!")

# ==========================================
# 🧠 GİZLİ KASADAN ŞİFREYİ ÇEKME (OTOMATİK)
# ==========================================
try:
    # Şifreyi Streamlit Secrets kasasından çekiyoruz. Kodda şifre yok!
    GIZLI_SIFRE = st.secrets["AIzaSyBpEpTUcyahbv1x0yg9wHR8JXkBRurU3Ic"]
    genai.configure(api_key=GIZLI_SIFRE)
    
    # GARDAŞ SENİN DEDİĞİN GİBİ 404 HATASI VERMESİN DİYE KLASİK MODELİ KOYDUM:
    model = genai.GenerativeModel('gemini-pro')
except:
    model = None

# ==========================================
# ⚙️ SAYFA VE HAFIZA
# ==========================================
st.set_page_config(page_title="Mican AI Ultra Premium", page_icon="🚀", layout="wide")

if "giris" not in st.session_state:
    st.session_state.giris = False
if "isim" not in st.session_state:
    st.session_state.isim = ""
if "foto" not in st.session_state:
    st.session_state.foto = None
if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = [{"role": "assistant", "content": "Gardaş hoş geldin! Ben Mican AI. Tüm sistemlerim senin için aktif!"}]
if "program" not in st.session_state:
    st.session_state.program = ""
if "tema_rengi" not in st.session_state:
    st.session_state.tema_rengi = "#00ffcc"

st.markdown(f"<style>.stApp {{ border-top: 5px solid {st.session_state.tema_rengi}; }}</style>", unsafe_allow_html=True)

# ==========================================
# 🔐 GİRİŞ EKRANI (HERKESE AÇIK KAYIT SİSTEMİ)
# ==========================================
if not st.session_state.giris:
    st.markdown("<h1 style='text-align: center; color: #00ffcc;'>🚀 Mican AI Yönetim Paneli</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Sisteme erişmek için kayıt olun veya giriş yapın. Şifre gerekmez!")
        islem = st.radio("İşlem Türü:", ["Giriş Yap", "Yeni Hesap Aç"])
        
        eposta = st.text_input("📧 E-Posta Adresiniz:")
        sifre = st.text_input("🔑 Hesabınız İçin Bir Şifre Belirleyin:", type="password")
        
        if st.button("Sistemleri Ateşle! 🔥", use_container_width=True):
            if "@" in eposta and len(sifre) >= 4:
                st.session_state.giris = True
                st.session_state.isim = eposta.split("@")[0].capitalize()
                st.success(f"Hoş geldin {st.session_state.isim}! Kapılar açılıyor...")
                time.sleep(1.5)
                st.rerun()
            else:
                st.error("Geçerli bir e-posta ve en az 4 haneli şifre girin!")
    st.stop()

# ==========================================
# 📱 SOL MENÜ VE PROFİL AYARLARI
# ==========================================
with st.sidebar:
    st.title("👤 VIP Profilim")
    
    if st.session_state.foto:
        st.image(st.session_state.foto, width=150, caption=f"Aktif Kullanıcı: {st.session_state.isim}")
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
    
    yeni_renk = st.color_picker("🎨 Sitenin Tema Rengini Seç", st.session_state.tema_rengi)
    if yeni_renk != st.session_state.tema_rengi:
        st.session_state.tema_rengi = yeni_renk
        st.rerun()

    if model:
        st.success("🟢 Zeka Motoru: KUSURSUZ ÇALIŞIYOR")
    else:
        st.error("🔴 Zeka: KAPALI (Yönetici Gizli Kasaya Şifre Girmeli)")
        
    st.markdown("---")
    if st.button("🚪 Sistemi Kapat (Çıkış)"):
        st.session_state.giris = False
        st.rerun()

# ==========================================
# 💎 ANA EKRAN VE DEVASA SEKMELER
# ==========================================
st.title(f"🌌 Mican AI - Ultra Yapay Zeka Merkezi")
st.caption("Arkadaşlarınla paylaşabilirsin. Arka planda devasa Google zekası çalışır.")

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Yapay Zeka Sohbet", 
    "📚 Akıllı Ders Programı", 
    "🛠️ İcat & Proje Atölyesi", 
    "⏱️ Odaklanma Modu"
])

# --- SEKME 1: SOHBET EKRANI ---
with tab1:
    for msg in st.session_state.mesajlar:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("İstediğin her şeyi sorabilirsin..."):
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
                        st.error("Sunucu yoğunluğu. Lütfen tekrar dene.")
            else:
                st.error("Zeka motoru geçici olarak devre dışı. Lütfen kurucuya haber verin.")

# --- SEKME 2: SINIF SEÇMELİ PROGRAM VE DISLIKE TUŞU ---
with tab2:
    st.header("🎯 Sana Özel Çalışma Programı")
    st.write("Sınıfını seç, saniyesinde özel 2 program çıkarayım.")
    
    sinif = st.selectbox("Kaçıncı Sınıfsın?", ["Sınıf Seç...", "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf (LGS)", "9. Sınıf", "10. Sınıf", "11. Sınıf", "12. Sınıf (YKS)"])
    
    if sinif != "Sınıf Seç...":
        colA, colB = st.columns(2)
        with colA:
            if st.button("✨ Bana Program Hazırla", use_container_width=True):
                if model:
                    with st.spinner(f"{sinif} için programlar çiziliyor..."):
                        soru = f"Ben {sinif} öğrencisiyim. Bana ders çalışmam için 2 farklı, saat saat planlanmış detaylı çalışma programı hazırla."
                        st.session_state.program = model.generate_content(soru).text
                else:
                    st.error("Zeka motoru kapalı.")
                    
        with colB:
            if st.session_state.program != "":
                if st.button("👎 Hiç Beğenmedim, Başka Ver!", use_container_width=True):
                    with st.spinner("Hemen çöpe atıp yepyeni program yazıyorum..."):
                        soru = f"Ben {sinif} öğrencisiyim. Önceki çalışma programlarını hiç beğenmedim. Bana TAMAMEN FARKLI 2 tane daha günlük çalışma programı hazırla."
                        st.session_state.program = model.generate_content(soru).text
        
        if st.session_state.program != "":
            st.markdown("---")
            st.write(st.session_state.program)

# --- SEKME 3: İCAT VE PROJE ATÖLYESİ ---
with tab3:
    st.header("🛠️ Elektronik ve Yazılım Atölyesi")
    st.write("Elindeki malzemeleri yaz, bu malzemelerle yapabileceğin mühendislik icatlarını adım adım anlatayım!")
    malzemeler = st.text_area("Elindeki Malzemeler (Örn: ESP32, kablo, ekran, motor...)", height=100)
    
    if st.button("🚀 Bu Malzemelerle Ne Yapabilirim?"):
        if model and malzemeler:
            with st.spinner("Projeler bulunuyor..."):
                icat_sorusu = f"Elimde şu malzemeler var: {malzemeler}. Lütfen bu malzemelerle yapabileceğim çok yaratıcı 2 farklı kendin-yap (DIY) projesi öner. Adım adım anlat."
                st.write(model.generate_content(icat_sorusu).text)
        elif not malzemeler:
            st.warning("Malzemeleri yazmayı unuttun!")

# --- SEKME 4: ODAKLANMA SAYACI ---
with tab4:
    st.header("⏱️ Derse Odaklanma Modu (Pomodoro)")
    st.write("Dikkatini dağıtan her şeyi kapat ve kampa gir!")
    dakika = st.slider("Kaç Dakika Çalışacaksın?", 10, 120, 40)
    
    if st.button("⏳ Sayacı Başlat"):
        st.warning(f"Dikkat! {dakika} dakika odaklanma başladı.")
        bar = st.progress(0)
        for i in range(100):
            time.sleep((dakika * 60) / 100)
            bar.progress(i + 1)
        st.success("Helal olsun! Süre bitti, artık mola verebilirsin.")
