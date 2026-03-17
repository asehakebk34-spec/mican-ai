import streamlit as st
import google.generativeai as genai
import time
from datetime import datetime
import random

# ==============================================================================
# 🚀 BÖLÜM 1: MİCAN AI "CYBER-NEON" GÖRSEL MOTORU (CSS)
# ==============================================================================
# Sitenin her hücresine Mican ruhunu ve neon ışıklarını enjekte ediyoruz.
st.set_page_config(page_title="Mican AI Ultra - Karargah", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    /* Ana Arka Plan: Uzay Boşluğu ve Derinlik */
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #0f0c29 50%, #050505 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* Mican AI Neon Başlık */
    .mican-title {
        font-size: 60px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #fc00ff, #00f2fe);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 10s linear infinite;
        text-shadow: 0 0 30px rgba(0, 242, 254, 0.4);
        margin-bottom: 10px;
    }

    @keyframes glow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sol Panel (Sidebar) Tasarımı */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.7);
        border-right: 2px solid #00f2fe;
        backdrop-filter: blur(10px);
    }

    /* Kartlar ve Mesaj Balonları */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(0, 242, 254, 0.1) !important;
        margin-bottom: 15px !important;
        transition: 0.3s;
    }
    .stChatMessage:hover {
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }

    /* Buton Tasarımları */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: #000 !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: 0.4s !important;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px #00f2fe;
    }
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 🧠 BÖLÜM 2: MİCAN ZEKA MOTORU (404 SAVAR)
# ==============================================================================
# Google'ın kaprisli model isimlerini otomatik tarayan devasa fonksiyon.
def mican_beyin_sistemi():
    if "api_sifresi" not in st.secrets:
        return None, "Şifre bulunamadı!"
    
    try:
        genai.configure(api_key=st.secrets["api_sifresi"])
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        
        # Öncelik sırasına göre en sağlam modelleri dene
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.5-pro']:
            if target in available_models:
                return genai.GenerativeModel(target), target
        
        # Hiçbiri yoksa ilk bulduğunu al
        if available_models:
            return genai.GenerativeModel(available_models[0]), available_models[0]
        return None, "Model listesi boş!"
    except Exception as e:
        return None, str(e)

# ==============================================================================
# 📂 BÖLÜM 3: DEVASA HAFIZA VE OTURUM BAŞLATMA
# ==============================================================================
# Burada her şeyi (Sohbetler, Ayarlar, Notlar) belleğe alıyoruz.
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {
        "Sohbet 1": [{"role": "assistant", "content": "Selam gardaş! Ben Mican. Bugün o Samsung'u uçuralım mı?"}]
    }

if "active_chat" not in st.session_state:
    st.session_state.active_chat = "Sohbet 1"

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "user_notes" not in st.session_state:
    st.session_state.user_notes = ""

# Zekayı ilk kez uyandır
if "mican_instance" not in st.session_state:
    obj, name = mican_beyin_sistemi()
    st.session_state.mican_instance = obj
    st.session_state.mican_model_name = name

# ==============================================================================
# 📑 BÖLÜM 4: SOL PANEL (NAVİGASYON VE GEÇMİŞ)
# ==============================================================================
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe; text-align:center;'>🤖 MİCAN PANEL</h2>", unsafe_allow_html=True)
    st.write("---")

    # YENİ SOHBET BAŞLATMA
    if st.button("➕ YENİ BİR SAYFA AÇ"):
        yeni_id = f"Sohbet {len(st.session_state.all_chats) + 1}"
        st.session_state.all_chats[yeni_id] = [{"role": "assistant", "content": "Gardaş yepyeni bir başlangıç yaptık, buyur!"}]
        st.session_state.active_chat = yeni_id
        st.rerun()

    st.write("📖 **Sohbet Arşivi**")
    # Mevcut sohbetleri listele
    for chat_name in list(st.session_state.all_chats.keys()):
        # Aktif sohbeti vurgula
        style = "border-left: 4px solid #fc00ff; padding-left: 10px;" if chat_name == st.session_state.active_chat else ""
        st.markdown(f"<div style='{style}'></div>", unsafe_allow_html=True)
        if st.button(f"💬 {chat_name}", key=f"btn_{chat_name}"):
            st.session_state.active_chat = chat_name
            st.rerun()

    st.write("---")
    # Durum Göstergeleri
    st.caption("💻 Sistem: Samsung x Mican")
    if st.session_state.mican_instance:
        st.success(f"Zeka: AKTİF")
    else:
        st.error("Zeka: BAĞLANTI YOK")
        # ==============================================================================
# 🔐 BÖLÜM 5: MİCAN VIP GÜVENLİK DUVARI (GİRİŞ EKRANI)
# ==============================================================================
# Eğer giriş yapılmadıysa, bütün sistemi kilitleyen ve şık bir giriş sunan kısım.
if not st.session_state.is_logged_in:
    st.markdown("<h1 class='mican-title'>⚡ MİCAN AI ULTRA ⚡</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#00f2fe;'>Gardaş, sisteme erişmek için kimlik doğrulaması gerekiyor.</p>", unsafe_allow_html=True)
    
    col_login_1, col_login_2, col_login_3 = st.columns([1, 1.5, 1])
    
    with col_login_2:
        with st.container():
            st.markdown("""
                <div style='background: rgba(255,255,255,0.05); padding: 30px; border-radius: 20px; border: 1px solid #00f2fe;'>
                </div>
            """, unsafe_allow_html=True)
            
            with st.form("mican_secure_access"):
                st.write("🔑 **KİMLİK DOĞRULAMA**")
                mican_mail = st.text_input("Gardaş E-Postan:", placeholder="ornek@mail.com")
                mican_pass = st.text_input("Gardaş Şifren:", type="password", placeholder="****")
                
                # Giriş Butonu
                login_trigger = st.form_submit_button("SİSTEME ERİŞİM SAĞLA")
                
                if login_trigger:
                    if "@" in mican_mail and len(mican_pass) >= 3:
                        st.session_state.is_logged_in = True
                        st.session_state.user_nick = mican_mail.split("@")[0].upper()
                        st.success(f"Hoş geldin {st.session_state.user_nick}! Mican motorları çalışıyor...")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Gardaş e-posta veya şifre hatalı, tekrar dene!")
    st.stop() # Giriş yapılana kadar altındaki hiçbir kodu çalıştırmaz.

# ==============================================================================
# 💎 BÖLÜM 6: ANA KOMUTA MERKEZİ (SEKMELER)
# ==============================================================================
# Sitenin kalbi burada atıyor. Her şeyi "Mican" ruhuyla isimlendirdik.
st.markdown(f"<h1 class='mican-title'>🤖 MİCAN AI ULTRA SÜRÜM</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Hoş geldin gardaşım <b>{st.session_state.user_nick}</b>! Aktun: {st.session_state.active_chat}</p>", unsafe_allow_html=True)

# 5 ANA BÖLÜM (SEKMELER)
tab_chat, tab_study, tab_workshop, tab_vip, tab_support = st.tabs([
    "💬 MİCAN SOHBET", 
    "🎯 DERS PLANLAYICI", 
    "🛠️ İCAT ATÖLYESİ", 
    "🚀 VIP ARAÇLAR", 
    "☎️ DESTEK MERKEZİ"
])

# ------------------------------------------------------------------------------
# 💬 TAB 1: MİCAN SOHBET (OTOMATİK HAFIZALI)
# ------------------------------------------------------------------------------
with tab_chat:
    st.markdown("<h3 style='color:#00f2fe;'>🗨️ Akıllı İletişim Hattı</h3>", unsafe_allow_html=True)
    
    # Aktif sohbetin geçmişini çekiyoruz
    current_chat_data = st.session_state.all_chats[st.session_state.active_chat]
    
    # Geçmiş mesajları baloncuklar halinde göster
    for chat_msg in current_chat_data:
        with st.chat_message(chat_msg["role"]):
            st.write(chat_msg["content"])

    # Kullanıcıdan giriş alma
    if user_input := st.chat_input("Mican'a bir şey sor gardaş..."):
        # Kullanıcı mesajını listeye ekle
        current_chat_data.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Mican'ın cevabını üretme
        with st.chat_message("assistant"):
            if st.session_state.mican_instance:
                with st.spinner("Mican veritabanına bağlanıyor..."):
                    try:
                        # Mican'ın kişiliğini burada fısıldıyoruz
                        mican_prompt = f"Senin adın Mican AI. Çok samimi, zeki ve yardımcı birisin. Kullanıcıya her zaman 'gardaş' diye hitap etmelisin. Soru: {user_input}"
                        
                        mican_resp = st.session_state.mican_instance.generate_content(mican_prompt)
                        final_text = mican_resp.text
                        
                        st.write(final_text)
                        current_chat_data.append({"role": "assistant", "content": final_text})
                    except Exception as e:
                        st.error(f"Gardaş bir aksilik oldu: {str(e)}")
            else:
                st.warning("Gardaş zeka motoru şu an uykuda, bağlantıları kontrol et!")

# ------------------------------------------------------------------------------
# 🎯 TAB 2: DERS PLANLAYICI (7. SINIF ÖZEL)
# ------------------------------------------------------------------------------
with tab_study:
    st.markdown("<h3 style='color:#00f2fe;'>🎯 Mican Ders Asistanı</h3>", unsafe_allow_html=True)
    st.write("Gardaş, 7. sınıfın o zor derslerini dert etme. Sen hedefini yaz, ben yolunu çizeyim.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        hedefler = st.text_area("Hangi konularda eksiğin var?", placeholder="Örn: Matematik rasyonel sayılar, Fen atomun yapısı...")
    with col_s2:
        calisma_saati = st.slider("Günde kaç saat vaktin var?", 1, 10, 3)

    if st.button("✨ BANA 2 ÖZEL PROGRAM HAZIRLA"):
        if st.session_state.mican_instance:
            with st.spinner("Mican algoritmaları çalıştırıyor..."):
                plan_prompt = f"Ben 7. sınıf öğrencisiyim. Eksiklerim: {hedefler}. Günde {calisma_saati} saat vaktim var. Bana birbirinden farklı 2 adet ders programı yap gardaşım. İçine mola sürelerini de ekle."
                plan_resp = st.session_state.mican_instance.generate_content(plan_prompt)
                st.markdown("---")
                st.markdown(plan_resp.text)
        else:
            st.error("Bağlantı yok!")
            # ------------------------------------------------------------------------------
# 🛠️ TAB 3: İCAT ATÖLYESİ (MÜHENDİSLİK KÖŞESİ)
# ------------------------------------------------------------------------------
with tab_workshop:
    st.markdown("<h3 style='color:#4facfe;'>🛠️ Mican Mühendislik Atölyesi</h3>", unsafe_allow_html=True)
    st.info("Gardaş, elindeki Arduino, motor, sensör ne varsa yaz; sana dünyayı değiştirecek projeler bulalım.")
    
    col_w1, col_w2 = st.columns([2, 1])
    with col_w1:
        malzemeler = st.text_input("📦 Elindeki Malzeme Listesi:", placeholder="Örn: Arduino Uno, Servo Motor, Mesafe Sensörü...")
    with col_w2:
        zorluk = st.select_slider("Proje Zorluğu", options=["Kolay", "Orta", "Zor", "Efsane"])

    if st.button("🚀 PROJE FİKRİ ÜRET"):
        if st.session_state.mican_instance and malzemeler:
            with st.spinner("Mican mühendislik veritabanını tarıyor..."):
                icat_prompt = f"Elimde {malzemeler} var. Bunlarla yapılabilecek {zorluk} seviyesinde 2 tane efsane proje öner gardaş. Devre şemasını ve kod mantığını basitçe anlat."
                icat_resp = st.session_state.mican_instance.generate_content(icat_prompt)
                st.success("İşte senin için seçilen icatlar:")
                st.markdown(icat_resp.text)
        else:
            st.warning("Gardaş malzemeleri yazmadın veya zeka bağlı değil!")

# ------------------------------------------------------------------------------
# 🚀 TAB 4: VIP ARAÇLAR (HACKER DASHBOARD & NOTLAR)
# ------------------------------------------------------------------------------
with tab_vip:
    st.markdown("<h3 style='color:#fc00ff;'>🚀 VIP Komuta Araçları</h3>", unsafe_allow_html=True)
    
    # VIP Dashboard - Sistem Metrikleri
    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
    v_col1.metric("Sistem Sağlığı", "Stabil", "100%")
    v_col2.metric("Zeka Modeli", st.session_state.mican_model_name.split("/")[-1])
    v_col3.metric("Güvenlik Katmanı", "SSL-v3", "Aktif")
    v_col4.metric("Aktif Kullanıcı", st.session_state.user_nick)

    st.markdown("---")

    # İki Sütunlu Araçlar
    v_left, v_right = st.columns(2)
    
    with v_left:
        st.markdown("<h4 style='color:#00f2fe;'>📝 Akıllı Not Defteri</h4>", unsafe_allow_html=True)
        # Notlar Session State üzerinden kaydedilir
        not_defteri = st.text_area("Çalışırken aklına gelenleri buraya karala gardaş:", 
                                   value=st.session_state.user_notes, height=200)
        st.session_state.user_notes = not_defteri
        st.caption("Notların bu oturum boyunca Mican hafızasında saklanır.")

    with v_right:
        st.markdown("<h4 style='color:#00f2fe;'>🧠 Mican Zeka Oyunları</h4>", unsafe_allow_html=True)
        st.write("Beyin fırtınası yapmak için bir soru patlat!")
        if st.button("🎲 BANA ZOR BİR SORU SOR"):
            if st.session_state.mican_instance:
                with st.spinner("Soru hazırlanıyor..."):
                    bilmece = st.session_state.mican_instance.generate_content("7. sınıf seviyesinde ama çok yaratıcı, mantık gerektiren bir zeka sorusu sor gardaş. Cevabı en altta gizli olsun.")
                    st.info(bilmece.text)
        
        st.markdown("---")
        st.markdown("<h4 style='color:#fc00ff;'>✈️ Havacılık Köşesi</h4>", unsafe_allow_html=True)
        if st.button("🌟 GÜNÜN UÇAK BİLGİSİNİ VER"):
            if st.session_state.mican_instance:
                info = st.session_state.mican_instance.generate_content("Havacılık veya uçak mühendisliği hakkında çok ilginç bir bilgi ver gardaş.")
                st.success(info.text)

# ------------------------------------------------------------------------------
# ☎️ TAB 5: DESTEK MERKEZİ (KRİTİK UYARI BÖLÜMÜ)
# ------------------------------------------------------------------------------
with tab_support:
    st.markdown("<h3 style='color:#00f2fe;'>☎️ Mican Destek Hattı</h3>", unsafe_allow_html=True)
    st.write("Sistemle veya üyeliğinle ilgili bir sıkıntı mı var? Teknik ekip burada (yani aslında henüz değil).")

    # Senin istediğin o meşhur kıpkırmızı uyarı kutusu
    st.markdown("""
        <div style='background: rgba(255, 0, 0, 0.15); padding: 40px; border-radius: 25px; border: 3px solid #ff4b4b; text-align: center; box-shadow: 0 0 30px rgba(255, 75, 75, 0.3);'>
            <h2 style='color: white; margin-bottom: 20px;'>⚠️ ERİŞİM VE BAĞLANTI HATASI</h2>
            <p style='font-size: 26px; color: #ff4b4b; font-weight: 900; text-shadow: 0 0 15px rgba(255, 75, 75, 0.6);'>
                Henüz herhangi bir numara bağlanmadı.
            </p>
            <p style='color: #cccccc; font-size: 16px; margin-top: 15px;'>
                Mican AI teknik servis altyapısı şu an bakım aşamasındadır. 
                Sabiha Gökçen Havacılık ekipleri sinyal güçlendirme çalışması yapmaktadır. 
                Lütfen daha sonra tekrar deneyin gardaşım.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("📩 **Kurumsal İletişim:** support@micanai.com")

# ==============================================================================
# 🏁 BÖLÜM 7: SİSTEM ALT BİLGİSİ (FOOTER)
# ==============================================================================
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.markdown(f"""
    <div style='text-align: center; border-top: 1px solid rgba(255, 255, 255, 0.1); padding: 20px;'>
        <p style='color: rgba(255, 255, 255, 0.4); font-size: 14px;'>
            <b>MİCAN AI ULTRA</b> - Geleceğin Yazılım Sistemi v4.5.1
        </p>
        <p style='color: #00f2fe; font-size: 12px;'>
            Oturum Zamanı: {datetime.now().strftime('%H:%M:%S')} | Sunucu: %s | © {datetime.now().year}
        </p>
    </div>
""" % ("Mican-Core-Main"), unsafe_allow_html=True)
# ------------------------------------------------------------------------------
# 🛡️ TAB 6: ADMIN PANEL & SİSTEM TERMİNALİ (HACKER MODU)
# ------------------------------------------------------------------------------
with tab_admin:
    st.markdown("<h3 style='color:#00f2fe;'>🛡️ Mican Güvenlik ve Admin Paneli</h3>", unsafe_allow_html=True)
    
    # Gerçek bir terminal simülasyonu
    st.markdown("""
        <div style='background-color: #000; color: #0f0; font-family: "Courier New", Courier, monospace; padding: 20px; border-radius: 10px; border: 1px solid #0f0; height: 300px; overflow-y: scroll;'>
            <p>>>> MICAN OS v4.5.1 BOOTING...</p>
            <p>>>> KERNEL OK. MEMORY OK. NEURAL ENGINE OK.</p>
            <p>>>> GÜVENLİK DUVARI AKTİF: SSL v3.0 ENCRYPTED.</p>
            <p>>>> [INFO] Samsung PC Bağlantısı Stabil.</p>
            <p>>>> [WARN] Sabiha Gökçen Sinyal Kuleleri ile Senkronizasyon Bekleniyor...</p>
            <p>>>> [INFO] Zeka Motoru: %s Hazır.</p>
            <p>>>> [STATUS] 7. Sınıf Ders Veritabanı Yüklendi.</p>
            <p>>>> SCANNING FOR PROJECTS... ESP32 FOUND. ARDUINO FOUND.</p>
            <p>>>> MICAN AI GARDAŞ MODU: AKTİF.</p>
            <p>>>> SYSTEM LOG: Kullanıcı %s sisteme sızdı.</p>
        </div>
    """ % (st.session_state.mican_model_name, st.session_state.user_nick), unsafe_allow_html=True)

    st.markdown("---")
    
    # Proje Bütçe Hesaplayıcı (Gardaş işi ekonomi)
    st.markdown("<h4>💰 Proje Bütçe Hesaplayıcı</h4>", unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        parca_adi = st.text_input("📦 Alınacak Parça:", placeholder="Örn: RS380 Motor")
        fiyat = st.number_input("💵 Fiyatı (TL):", min_value=0, value=0)
    with col_b2:
        miktar = st.number_input("🔢 Adet:", min_value=1, value=1)
        kargo = st.checkbox("Kargo Ücreti Var (+50 TL)")

    if st.button("💵 TOPLAM MALİYETİ HESAPLA"):
        toplam = (fiyat * miktar) + (50 if kargo else 0)
        st.write(f"**Gardaş bu projenin maliyeti:** {toplam} TL tutuyor. Değer mi? Bence değer!")

# ------------------------------------------------------------------------------
# 🔌 TAB 7: ELEKTRONİK BİLEŞEN KÜTÜPHANESİ (HIZLI REHBER)
# ------------------------------------------------------------------------------
with tab_elektronik:
    st.markdown("<h3 style='color:#4facfe;'>🔌 Mican Elektronik Rehberi</h3>", unsafe_allow_html=True)
    st.write("Projelerinde kullanacağın parçalar hakkında hızlı teknik veriler.")

    # Karşılaştırma Tablosu
    st.markdown("#### ⚡ Denetleyici Karşılaştırması")
    data = {
        "Özellik": ["Çalışma Voltajı", "Wi-Fi / BT", "İşlemci Hızı", "Kullanım Alanı"],
        "Arduino Uno": ["5V", "Yok", "16 MHz", "Basit Robotlar"],
        "ESP32": ["3.3V", "Var", "240 MHz", "Akıllı Ev / IoT"],
        "STM32": ["3.3V", "Yok", "72 MHz", "Endüstriyel Cihazlar"]
    }
    st.table(data)

    # Kariyer Köşesi - Havacılık
    st.markdown("---")
    st.markdown("<h4 style='color:#fc00ff;'>✈️ Sabiha Gökçen Havacılık Kariyer Yolu</h4>", unsafe_allow_html=True)
    st.write("Uçak teknisyeni olmak isteyen bir 7. sınıf öğrencisi için Mican tavsiyeleri:")
    
    with st.expander("📚 Hangi Liseye Gitmeliyim?"):
        st.write("Gardaş, Sabiha Gökçen MTAL veya benzeri havacılık liselerini hedefle. LGS'de matematik ve fenin canavar gibi olması lazım!")
    
    with st.expander("🔧 Maaşlar ve Gelecek"):
        st.write("Uçak teknisyenleri Türkiye'de en çok kazanan teknik personellerdendir. Ama İngilizce şart! İngilizceyi şimdiden hallet gardaşım.")

# ------------------------------------------------------------------------------
# ⚙️ BÖLÜM 15: GİZLİ MİCAN AYARLARI (MODLAR)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.write("---")
    st.write("🛠️ **Sistem Modları**")
    overdrive = st.toggle("Overdrive Modu (Fanları Çalıştır)")
    dark_neon = st.toggle("Ultra Neon Modu", value=True)
    
    if overdrive:
        st.warning("⚠️ Dikkat: Samsung PC ısınıyor! Mican performansı %200 artırıldı.")
    
    if st.button("🧹 SOHBETİ SIFIRLA"):
        st.session_state.all_chats[st.session_state.active_chat] = [{"role": "assistant", "content": "Gardaş sayfayı temizledim, emrindeyim!"}]
        st.rerun()
        # ------------------------------------------------------------------------------
# ⏳ TAB 8: GERİ SAYIM VE MOTİVASYON (LGS VE SINAV SAYAÇLARI)
# ------------------------------------------------------------------------------
with tab_countdown:
    st.markdown("<h3 style='color:#00f2fe;'>⏳ Mican Zaman Sayacı</h3>", unsafe_allow_html=True)
    st.write("Gardaş, hedefin Sabiha Gökçen Havacılık Lisesi ise zamanı iyi yönetmek lazım.")

    # Tarih Hesaplama
    bugun = datetime.now()
    # Temsili LGS Tarihi (Haziran'ın ilk haftası gibi düşünelim)
    lgs_tarihi = datetime(2027, 6, 6) # Senin 8. sınıf sonu hedefin
    kalan_gun = (lgs_tarihi - bugun).days

    # Neon Sayaç Tasarımı
    st.markdown(f"""
        <div style='background: linear-gradient(90deg, #1a1a2e, #0f0c29); padding: 30px; border-radius: 20px; border: 2px solid #00f2fe; text-align: center;'>
            <h1 style='color: #00f2fe; font-size: 80px; margin: 0;'>{kalan_gun}</h1>
            <p style='color: white; font-size: 20px;'>BÜYÜK HEDEFE KALAN GÜN</p>
            <div style='width: 100%; background-color: #333; border-radius: 10px; margin-top: 15px;'>
                <div style='width: 30%; background-color: #fc00ff; height: 10px; border-radius: 10px;'></div>
            </div>
            <p style='color: #fc00ff; font-size: 14px; margin-top: 10px;'>Gardaş yolun %30'u bitti bile, asıl şimdi gazlama vakti!</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    # Günlük Motivasyon Sözü
    if st.button("🌟 MİCAN'DAN GÜNÜN MOTİVASYONUNU AL"):
        if st.session_state.mican_instance:
            with st.spinner("Mican felsefe yapıyor..."):
                moto = st.session_state.mican_instance.generate_content("7. sınıf öğrencisi için ders çalışmaya teşvik edici, çok havalı ve samimi bir motivasyon cümlesi kur gardaş.")
                st.info(moto.text)

# ------------------------------------------------------------------------------
# 🎨 TAB 9: MEDYA, SANAT VE GÖRSEL ÜRETİCİ (MİCAN STUDIO)
# ------------------------------------------------------------------------------
with tab_media:
    st.markdown("<h3 style='color:#fc00ff;'>🎨 Mican Sanat Atölyesi</h3>", unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.markdown("#### 🖼️ Görsel Hayal Kurucu")
        st.write("Mican senin için hayalindeki görselin komutunu (prompt) hazırlasın.")
        hayal = st.text_input("Ne hayal ediyorsun?", placeholder="Örn: Mars'ta uçan bir Türk uçağı...")
        
        if st.button("🎨 GÖRSEL KOMUTU OLUŞTUR"):
            if st.session_state.mican_instance and hayal:
                with st.spinner("Hayaller işleniyor..."):
                    hayal_res = st.session_state.mican_instance.generate_content(f"Kullanıcının hayali şu: {hayal}. Bu hayali bir yapay zeka resim üreticisine (DALL-E veya Midjourney gibi) yazdırmak için profesyonel ve çok detaylı bir İngilizce prompt hazırla gardaş.")
                    st.code(hayal_res.text, language="markdown")
                    st.caption("Gardaş bu kodu kopyalayıp resim botlarına yapıştırabilirsin!")

    with col_m2:
        st.markdown("#### 🎵 Mican Müzik & Ambians")
        st.write("Ders çalışırken veya kod yazarken Mican radyosunu aç.")
        
        # Streamlit Audio özelliği ile (Örnek bir link, kendi linklerini ekleyebilirsin)
        st.markdown("**1. Odaklanma Müziği (Lo-Fi)**")
        st.markdown("[🎵 YouTube'da Aç: Mican Lo-Fi Radio](https://www.youtube.com/watch?v=jfKfPfyJRdk)")
        
        st.markdown("**2. Mühendislik Sesleri (Hangar Ambiansı)**")
        st.markdown("[✈️ Sabiha Gökçen Ambiansı](https://www.youtube.com/watch?v=xWpT9S-Uj3Y)")

    st.markdown("---")
    
    # Mican Galeri (Temsili)
    st.markdown("#### 📸 Mican İlham Galerisi")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.image("https://images.unsplash.com/photo-1581092160562-40aa08e78837", caption="Geleceğin Elektroniği")
    with m_col2:
        st.image("https://images.unsplash.com/photo-1517976487492-5750f3195933", caption="Havacılık Tutkusu")
    with m_col3:
        st.image("https://images.unsplash.com/photo-1485827404703-89b55fcc595e", caption="Yapay Zeka Devri")

# ==============================================================================
# 🧠 BÖLÜM 16: MİCAN ÖZEL "GARDAŞ" FONKSİYONLARI
# ==============================================================================
# Buraya sistemin daha akıllı çalışması için özel tetikleyiciler ekleyebilirsin.
def mican_selamla():
    saat = datetime.now().hour
    if 5 <= saat < 12: return "Günaydın gardaş, bugün Samsung'u ateşleyelim!"
    elif 12 <= saat < 18: return "İyi günler gardaş, projeler ne alemde?"
    else: return "İyi akşamlar gardaş, bugün çok çalıştık mı?"

with st.sidebar:
    st.info(mican_selamla())
    # ------------------------------------------------------------------------------
# 🎮 TAB 10: MİCAN EĞLENCE VE OYUN SALONU (STRESS RELIEF)
# ------------------------------------------------------------------------------
with tab_games:
    st.markdown("<h3 style='color:#00f2fe;'>🎮 Mican Mini-Game Zone</h3>", unsafe_allow_html=True)
    st.write("Gardaş, derslerden beynin yandıysa biraz kafa dağıtalım.")

    # Sayı Tahmin Oyunu (Gömülü Mantık)
    st.markdown("#### 🔢 Sayı Tahmin Yarışması")
    if "secret_number" not in st.session_state:
        st.session_state.secret_number = random.randint(1, 100)
        st.session_state.attempts = 0

    guess = st.number_input("1 ile 100 arasında bir sayı tuttum, bil bakalım?", min_value=1, max_value=100, key="game_guess")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        if st.button("TAHMİN ET 🎯"):
            st.session_state.attempts += 1
            if guess < st.session_state.secret_number:
                st.warning("Daha büyük bir sayı söyle gardaş!")
            elif guess > st.session_state.secret_number:
                st.warning("Daha küçük bir sayı söyle gardaş!")
            else:
                st.success(f"HELAL OLSUN! {st.session_state.attempts} kerede bildin aslanım.")
                st.balloons()
                del st.session_state.secret_number # Sayıyı sıfırla
    
    with col_g2:
        if st.button("YENİ OYUN BAŞLAT 🔄"):
            del st.session_state.secret_number
            st.rerun()

    st.markdown("---")
    st.markdown("#### 🐍 Klasik Yılan Oyunu (Harici Link)")
    st.write("Kod yazarken canın sıkılırsa Mican senin için bir yer buldu:")
    st.markdown("[🐍 Buradan Yılan Oyunu Oyna](https://www.google.com/search?q=snake+game)")

# ------------------------------------------------------------------------------
# 🔧 TAB 11: MİCAN ÖZEL ARAÇLAR (HAVA DURUMU & ÖDEV)
# ------------------------------------------------------------------------------
with tab_tools:
    st.markdown("<h3 style='color:#fc00ff;'>🔧 Mican Akıllı Araç Seti</h3>", unsafe_allow_html=True)
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.markdown("#### ☁️ Havacılık ve Hava Durumu")
        sehir = st.text_input("Şehir Yaz (Örn: İstanbul):", "İstanbul")
        if st.button("🌤️ HAVA DURUMUNU SORGULA"):
            if st.session_state.mican_instance:
                with st.spinner("Meteoroloji uydularına bağlanılıyor..."):
                    hava_prompt = f"{sehir} şehri için şu anki hava durumunu tahmin et (temsili) ve bu havanın uçuşlar (Sabiha Gökçen çıkışlı) üzerindeki etkisini bir uçak teknisyeni gibi anlat gardaş."
                    res = st.session_state.mican_instance.generate_content(hava_prompt)
                    st.info(res.text)

    with tool_col2:
        st.markdown("#### ✍️ Otomatik Ödev Yardımcısı")
        odev_sorusu = st.text_area("Ödev sorunu buraya yapıştır veya yaz:")
        if st.button("🧠 ÖDEVİ ANALİZ ET VE ÇÖZ"):
            if st.session_state.mican_instance and odev_sorusu:
                with st.spinner("Mican kütüphaneleri tarıyor..."):
                    # Mican'ın ödev çözme karakterini belirliyoruz
                    odev_prompt = f"Ben 7. sınıf öğrencisiyim. Şu ödev sorusunu bana adım adım, öğretmen gibi ama samimi bir dille anlat gardaş: {odev_sorusu}"
                    res = st.session_state.mican_instance.generate_content(odev_prompt)
                    st.success("İşte ödevin çözümü ve mantığı:")
                    st.write(res.text)

# ==============================================================================
# 📊 BÖLÜM 17: MİCAN İSTATİSTİK KATMANI (ADVANCED)
# ==============================================================================
# Sistemin ne kadar süredir açık olduğunu ve kullanım yoğunluğunu hesaplar.
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

uptime = round(time.time() - st.session_state.start_time, 2)

with st.sidebar:
    st.write("---")
    st.markdown(f"<p style='color:gray; font-size:12px;'>Sistem Çalışma Süresi: {uptime} sn</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00f2fe; font-size:10px;'>Mican Core v4.5 - Stable Build</p>", unsafe_allow_html=True)
    # ------------------------------------------------------------------------------
# 🏪 TAB 12: MİCAN MARKET (DONANIM BORSASI)
# ------------------------------------------------------------------------------
with tab_market:
    st.markdown("<h3 style='color:#00f2fe;'>🏪 Mican Donanım Pazarı</h3>", unsafe_allow_html=True)
    st.write("Gardaş, projelerin için en ucuz parçaları senin için taradım (temsili fiyatlar).")

    # Dinamik Fiyat Tablosu
    market_data = {
        "Parça Adı": ["RS380 Motor", "Arduino Uno R3", "ESP32 DevKit", "12V 7Ah Akü", "SG90 Servo", "Jumper Kablo (40lı)"],
        "Ortalama Fiyat (TL)": [120, 250, 210, 450, 45, 65],
        "Stok Durumu": ["✅ Var", "✅ Var", "⚠️ Azaldı", "✅ Var", "✅ Var", "✅ Var"],
        "Mican Önerisi": ["Kaçırma al", "Klonu da iş görür", "Gelecek burada", "Ağır ama sağlam", "Yedeğini al", "Her eve lazım"]
    }
    st.table(market_data)

    st.markdown("---")
    st.markdown("#### 🛒 Hızlı Sipariş Notu Oluştur")
    secilen_parca = st.selectbox("Hangi parçayı alacaksın gardaş?", market_data["Parça Adı"])
    if st.button("📝 LİSTEYE EKLE"):
        st.success(f"Gardaş, {secilen_parca} sipariş listene eklendi. Kumbarayı hazırla!")

# ------------------------------------------------------------------------------
# 🕵️ TAB 13: GİZLİ TERMİNAL (MATRIX MODU)
# ------------------------------------------------------------------------------
with tab_secret:
    st.markdown("<h3 style='color:#0f0;'>🕵️ Mican Gizli Operasyon Merkezi</h3>", unsafe_allow_html=True)
    st.write("Buraya sadece gerçek hackerlar (yani sen) girebilir gardaş.")

    # Matrix Efekti (CSS ile)
    st.markdown("""
        <style>
        .matrix-box {
            background-color: #000;
            color: #0f0;
            padding: 20px;
            border: 2px solid #0f0;
            font-family: 'Courier New', monospace;
            box-shadow: 0 0 20px #0f0;
            margin-bottom: 20px;
        }
        </style>
        <div class='matrix-box'>
            >>> SYSTEM OVERRIDE: ACTIVE
