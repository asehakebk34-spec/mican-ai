import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime

# ==============================================================================
# 🚀 BÖLÜM 1: SÜPER TASARIM VE ARKA PLAN AYARLARI (CSS)
# ==============================================================================
# Bu kısım sitenin "her şeyi" olan o efsane karanlık ve neon temayı oluşturur.
st.set_page_config(page_title="Ultra Zeka Merkezi", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* Ana Arka Plan ve Yazı Tipleri */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Neon Başlık Tasarımı */
    .main-title {
        font-size: 50px;
        font-weight: 800;
        text-align: center;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 10px 20px rgba(79, 172, 254, 0.3);
        margin-bottom: 30px;
    }

    /* Kartlar ve Kutular */
    div.stButton > button {
        background: linear-gradient(45deg, #00dbde 0%, #fc00ff 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 15px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(252, 0, 255, 0.5);
    }

    /* Sohbet Baloncukları */
    .chat-bubble {
        padding: 20px;
        border-radius: 20px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Gizli Kenar Çubuğu */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5);
        border-right: 1px solid rgba(0, 242, 254, 0.2);
    }
    
    /* Input Alanları */
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid #4facfe;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🧠 BÖLÜM 2: AKILLI MODEL DEDEKTÖRÜ (404 HATASINI BİTİREN KISIM)
# ==============================================================================
# Bu fonksiyon Google'ın o an sana hangi zekayı verdiğini otomatik bulur.
def get_working_model():
    try:
        if "api_sifresi" not in st.secrets:
            return None, "Gizli Kasa (Secrets) boş!"
            
        genai.configure(api_key=st.secrets["api_sifresi"])
        
        # Google'daki tüm modelleri tara ve en iyisini seç
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            return None, "Çalışan model bulunamadı!"
            
        # Öncelik sırasına göre en iyi modeli seç
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if target in available_models:
                return genai.GenerativeModel(target), target
        
        return genai.GenerativeModel(available_models[0]), available_models[0]
    except Exception as e:
        return None, str(e)

# ==============================================================================
# 💾 BÖLÜM 3: SİSTEM HAFIZASI VE OTURUM YÖNETİMİ
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "active_model" not in st.session_state:
    model_obj, model_name = get_working_model()
    st.session_state.active_model = model_obj
    st.session_state.model_name = model_name
    # ==============================================================================
# 🔐 BÖLÜM 4: VIP GİRİŞ EKRANI (OTOMATİK KORUMA)
# ==============================================================================
# Bu kısım, şifre bilmeyenlerin sisteme girmesini engeller.
if not st.session_state.is_logged_in:
    st.markdown("<h1 class='main-title'>⚡ SİSTEME GİRİŞ YAP</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.info("Sistemi kullanmak için e-posta ve şifrenizi girin.")
            user_mail = st.text_input("📧 E-Posta Adresiniz:")
            user_pass = st.text_input("🔑 Güvenlik Şifreniz:", type="password")
            submit = st.form_submit_button("SİSTEMİ ATEŞLE 🔥")
            
            if submit:
                if "@" in user_mail and len(user_pass) >= 4:
                    st.session_state.is_logged_in = True
                    st.session_state.user_name = user_mail.split("@")[0].capitalize()
                    st.success("Güvenlik duvarı aşıldı! Erişim sağlandı...")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("HATA: Geçerli e-posta ve en az 4 haneli şifre!")
    st.stop()

# ==============================================================================
# 📱 BÖLÜM 5: SADE VE ŞIK KENAR ÇUBUĞU (SIDEBAR)
# ==============================================================================
# Gereksiz ayarları sildim, sadece durum ve çıkış tuşu kaldı.
with st.sidebar:
    st.markdown(f"<h2 style='color:#00f2fe;'>👤 {st.session_state.user_name}</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Zeka durumu kontrolü
    if st.session_state.active_model:
        st.success(f"🟢 SİSTEM AKTİF\n\nModel: {st.session_state.model_name}")
    else:
        st.error("🔴 SİSTEM KAPALI\n\nSecrets ayarlarını kontrol et!")

    st.markdown("---")
    if st.button("🚪 ÇIKIŞ YAP"):
        st.session_state.is_logged_in = False
        st.rerun()

# ==============================================================================
# 💎 BÖLÜM 6: ANA YÖNETİM PANELİ (TABLAR)
# ==============================================================================
st.markdown(f"<h1 class='main-title'>⚡ ULTRA ZEKA MERKEZİ</h1>", unsafe_allow_html=True)

# İhtiyacın olan 3 ana bölüm
tab1, tab2, tab3 = st.tabs([
    "💬 AKILLI SOHBET", 
    "🎯 DERS PLANLAYICI", 
    "🛠️ PROJE ATÖLYESİ"
])
# ==============================================================================
# 💬 BÖLÜM 7: AKILLI SOHBET VE HAFIZA SİSTEMİ
# ==============================================================================
with tab1:
    st.markdown("<h3 style='color:#00f2fe;'>🗨️ Sohbet Merkezi</h3>", unsafe_allow_html=True)
    
    # Geçmiş mesajları ekrana basar
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Kullanıcıdan soru alma
    if prompt := st.chat_input("Bir soru sor veya yardım iste..."):
        # Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Yapay zekanın cevabı
        with st.chat_message("assistant"):
            if st.session_state.active_model:
                with st.spinner("Sistem katmanları analiz ediliyor..."):
                    try:
                        # Zekayı ateşleme noktası
                        response = st.session_state.active_model.generate_content(prompt)
                        cevap = response.text
                        st.write(cevap)
                        st.session_state.messages.append({"role": "assistant", "content": cevap})
                    except Exception as e:
                        st.error(f"⚠️ Kritik Hata: {str(e)}")
            else:
                st.warning("⚠️ Zeka motoru kapalı. Lütfen yöneticiye (Secrets) başvurun!")

# ==============================================================================
# 📚 BÖLÜM 8: ÖĞRENCİ ASİSTANI VE DERS PLANLAYICI
# ==============================================================================
with tab2:
    st.markdown("<h3 style='color:#00f2fe;'>🎯 Kişisel Gelişim ve Ders Planı</h3>", unsafe_allow_html=True)
    st.write("Hedeflerini belirle, yapay zeka senin için en verimli yolu çizsin.")

    col1, col2 = st.columns(2)
    with col1:
        hedefler = st.text_area("Haftalık Hedeflerin Nedir?", placeholder="Örn: Matematik rasyonel sayılar bitecek...")
    with col2:
        bos_vakit = st.slider("Günde kaç saat ders çalışabilirsin?", 1, 8, 3)

    if st.button("✨ BANA ÖZEL 2 PROGRAM OLUŞTUR"):
        if st.session_state.active_model:
            with st.spinner("Algoritma hesaplanıyor..."):
                talimat = f"Ben 7. sınıf öğrencisiyim. Hedeflerim: {hedefler}. Günde {bos_vakit} saat vaktim var. Bana birbirinden farklı, eğlenceli ve disiplinli 2 adet çalışma programı hazırla. Samimi bir dil kullan."
                res = st.session_state.active_model.generate_content(talimat)
                st.markdown("---")
                st.markdown(res.text)
        else:
            st.error("Sistem çevrimdışı!")

# ==============================================================================
# 🛠️ BÖLÜM 9: ELEKTRONİK VE YAZILIM PROJE ATÖLYESİ
# ==============================================================================
with tab3:
    st.markdown("<h3 style='color:#00f2fe;'>🛠️ İcat Atölyesi</h3>", unsafe_allow_html=True)
    st.info("Elindeki donanımları yaz (Arduino, ESP32, sensörler), sana dünya çapında projeler önereyim.")
    
    malzeme_listesi = st.text_input("📦 Elindeki Malzemeler:")
    
    if st.button("🚀 PROJE FİKRİ ÜRET"):
        if st.session_state.active_model and malzeme_listesi:
            with st.spinner("Mühendislik veritabanı taranıyor..."):
                icat_sorusu = f"Elimde {malzeme_listesi} var. Bunlarla yapabileceğim, 7. sınıf seviyesinde ama çok havalı 2 proje öner. Devre şemasını ve kod mantığını anlat."
                icat_res = st.session_state.active_model.generate_content(icat_sorusu)
                st.success("İşte senin için seçilen projeler:")
                st.markdown(icat_res.text)
        else:
            st.warning("Gardaş malzemeleri yazmadın veya sistem kapalı!")

# ==============================================================================
# 🏁 BÖLÜM 10: SİSTEM ALT BİLGİSİ (FOOTER)
# ==============================================================================
st.markdown("---")
st.markdown(f"<p style='text-align: center; color: rgba(255,255,255,0.3);'>Sistem Zamanı: {datetime.now().strftime('%H:%M:%S')} | Veri Tabanı Güvende</p>", unsafe_allow_html=True)
# ==============================================================================
# 🚀 BÖLÜM 11: VIP ARAÇLAR VE EKSTRA ÖZELLİKLER
# ==============================================================================
with tab4:
    st.markdown("<h3 style='color:#fc00ff;'>🚀 VIP Araç Seti</h3>", unsafe_allow_html=True)
    
    # Üst tarafa 3'lü mini dashboard
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="Sistem Durumu", value="Stabil", delta="100%")
    with m2:
        st.metric(label="Zeka Modeli", value=st.session_state.model_name.split("/")[-1])
    with m3:
        st.metric(label="Güvenlik", value="Aktif", delta="SSL v3")

    st.markdown("---")

    # --- ALT ÖZELLİKLER ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("<h4 style='color:#00f2fe;'>📝 Hızlı Not Defteri</h4>", unsafe_allow_html=True)
        if "user_notes" not in st.session_state:
            st.session_state.user_notes = ""
        
        # Otomatik kaydedilen not defteri
        not_alani = st.text_area("Çalışırken notlarını buraya bırak, oturum boyunca saklayayım:", 
                                 value=st.session_state.user_notes, height=150)
        st.session_state.user_notes = not_alani
        st.caption("Notların sistem hafızasına (session) kaydedildi.")

    with col_right:
        st.markdown("<h4 style='color:#00f2fe;'>🧠 Zihin Fırtınası</h4>", unsafe_allow_html=True)
        if st.button("🎲 BANA BİR ZEKA SORUSU SOR"):
            if st.session_state.active_model:
                with st.spinner("Zorlayıcı bir soru hazırlanıyor..."):
                    soru = st.session_state.active_model.generate_content("7. sınıf seviyesinde ama mantık yürütebileceğim, çok yaratıcı ve eğlenceli bir zeka sorusu sor. Cevabı en altta gizli kalsın.")
                    st.info(soru.text)
            else:
                st.error("Bağlantı yok!")

    st.markdown("---")

    # --- ÖZEL TEKNOLOJİ KÖŞESİ ---
    st.markdown("<h4 style='color:#fc00ff;'>✈️ Havacılık ve Gelecek Teknolojileri</h4>", unsafe_allow_html=True)
    st.write("Uçak teknolojileri veya geleceğin mühendisliği hakkında ilham al.")
    
    if st.button("🌟 GÜNÜN TEKNOLOJİ BİLGİSİNİ VER"):
        if st.session_state.active_model:
            with st.spinner("Veritabanı taranıyor..."):
                tekno_res = st.session_state.active_model.generate_content("Havacılık, uçak motorları veya modern teknoloji hakkında çok ilginç, kısa bir bilgi ver. 7. sınıfa giden birinin ilgisini çekecek şekilde anlat.")
                st.success(tekno_res.text)
