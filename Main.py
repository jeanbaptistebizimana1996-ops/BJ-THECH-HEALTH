import streamlit as st
import google.generativeai as genai
import qrcode
from io import BytesIO
from datetime import datetime

# 1. INITIALIZE DATABASE & SECURITY
if "db" not in st.session_state:
    st.session_state.db = {
        "119958": {"izina": "Habineza", "phone": "+250780000000", "amateka": "Asanzwe arwara igifu", "results": "", "meds": ""}
    }
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# 2. AI CONFIGURATION (Urufunguzo rwawe rurimo neza)
API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. UI DESIGN (Medical Aesthetics)
st.set_page_config(page_title="Smart Health by BJ TECH", page_icon="🏥", layout="wide")

st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Background ya Fingerprint yose */
    .stApp {
        background-image: url("https://img.icons8.com/ios-filled/500/000000/fingerprint.png");
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-size: 300px;
        background-color: rgba(244, 247, 250, 0.96);
        background-blend-mode: overlay;
    }

    /* Sign-in Box (Umukara werurutse / Light Grey) */
    .signin-card {
        background-color: #f8f9fa;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .main-title { color: #1a5fb4; text-align: center; font-weight: bold; font-size: 32px; }
    .medical-green { color: #28a745; text-align: center; font-weight: bold; }

    /* Buttons (Blue to Green Hover) */
    div.stButton > button {
        background-color: #1a5fb4 !important;
        color: white !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #28a745 !important;
        border: 1px solid white !important;
    }

    .footer-bj {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #ffffff; color: #1a5fb4;
        text-align: center; font-size: 12px; padding: 5px;
        border-top: 2px solid #1a5fb4; z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR (Isaha n'impuruza)
with st.sidebar:
    st.markdown(f"<div style='background:#28a745; color:white; padding:10px; border-radius:10px; text-align:center;'>🕒 {datetime.now().strftime('%H:%M:%S')}<br>{datetime.now().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)
    st.markdown("---")
    role = st.radio("SISTEME Y'IBITARO:", ["🏠 Kiosk (Patient)", "🧪 Laboratory", "💊 Pharmacy"])
    st.divider()
    st.caption("BJ TECH CYBER-SHIELD v5.0")

# ---------------------------------------------------------
# PAGE 1: KIOSK (Registration & AI)
# ---------------------------------------------------------
if role == "🏠 Kiosk (Patient)":
    st.markdown("<div class='main-title'>BJ TECH MEDICAL CENTER</div>", unsafe_allow_html=True)
    st.markdown("<div class='medical-green'>🛡️ SECURE BIOMETRIC ACCESS</div>", unsafe_allow_html=True)
    
    # Sign-in Section (Umukara werurutse)
    st.markdown('<div class="signin-card">', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Sign In", "📝 New Registration"])
    
    with tab1:
        p_id = st.text_input("Scan ID / Fingerprint:", placeholder="Urugero: 119958")
        if st.button("VERIFY IDENTITY"):
            if p_id in st.session_state.db:
                st.session_state.current_user = p_id
                st.balloons()
            else: st.error("ID ntabwo yabonetse. Banza wiyandikishe.")
            
    with tab2:
        new_id = st.text_input("Hitamo ID nshya:")
        new_name = st.text_input("Amazina yombi:")
        if st.button("CREATE SECURE PROFILE"):
            if new_id and new_name:
                st.session_state.db[new_id] = {"izina": new_name, "phone": "N/A", "amateka": "New Patient", "results": "", "meds": ""}
                st.success(f"Byagenze neza! ID yawe ni {new_id}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat AI niba yinjiye
    if st.session_state.current_user:
        patient = st.session_state.db[st.session_state.current_user]
        st.info(f"✅ Verified: **{patient['izina']}**")
        
        # Chat History
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        
        if prompt := st.chat_input("Baza muganga AI ikibazo..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                response = model.generate_content(f"Uri muganga kuri BJ TECH Rwanda. Subiza {patient['izina']} mu Kinyarwanda: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

# ---------------------------------------------------------
# PAGE 2: LABORATORY
# ---------------------------------------------------------
elif role == "🧪 Laboratory":
    st.markdown("<h1 style='text-align:center; color:#28a745;'>🧪 Lab Management</h1>", unsafe_allow_html=True)
    lab_id = st.text_input("Scan QR Code y'umurwayi:")
    
    if lab_id in st.session_state.db:
        st.write(f"Umurwayi: **{st.session_state.db[lab_id]['izina']}**")
        test_res = st.selectbox("Ibisubizo:", ["Negative", "Malaria Positive", "Typhoid Positive"])
        if st.button("Emeza Ibisubizo"):
            st.session_state.db[lab_id]["results"] = test_res
            st.success("Byabitswe!")

# ---------------------------------------------------------
# PAGE 3: PHARMACY
# ---------------------------------------------------------
elif role == "💊 Pharmacy":
    st.title("💊 Smart Pharmacy")
    p_id = st.text_input("Enter Patient ID:")
    if p_id in st.session_state.db:
        res = st.session_state.db[p_id]["results"]
        if res:
            st.warning(f"Ibizamini bya Lab: {res}")
            if st.button("Confirm Medicine Delivery"):
                st.balloons()
        else: st.info("Nta bizamini biraboneka.")

# FOOTER
st.markdown("<div class='footer-bj'>POWERED BY BJ TECH LTD © 2026</div>", unsafe_allow_html=True)
