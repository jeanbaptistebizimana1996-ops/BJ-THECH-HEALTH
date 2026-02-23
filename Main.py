import streamlit as st
import google.generativeai as genai
from datetime import datetime

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {"119958": {"izina": "Habineza", "phone": "0780000000", "results": "Nta bizamini", "meds": "Nta miti", "date": "2026-02-24"}}
if "passwords" not in st.session_state:
    st.session_state.passwords = {"lab": "lab.2026", "pharmacy": "phar.2026", "admin": "cyuma.thec.2026"}
if "hosp_name" not in st.session_state:
    st.session_state.hosp_name = "BJ TECH MEDICAL CENTER"
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# 2. CONFIGURE AI (SECURITY MODE)
# Iyi code izajya isoma urufunguzo washyize muri SECRETS
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
    else:
        st.warning("⚠️ AI Key missing in Secrets. Please add GEMINI_API_KEY.")
except Exception as e:
    st.error(f"Security Connection Error: {e}")

# 3. UI DESIGN (Medical & Biometric)
st.set_page_config(page_title="BJ TECH Medical OS", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    header {visibility: hidden;}
    .stApp { background-color: #f4f7f6; }
    .signin-box {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 20px;
        border: 1px solid #d1d9e6;
        box-shadow: 10px 10px 20px #d1d9e6, -10px -10px 20px #ffffff;
        background-image: url("https://www.transparenttextures.com/patterns/pinstriped-suit.png");
    }
    .main-title { color: #1a5fb4; text-align: center; font-weight: bold; font-size: 32px; }
    div.stButton > button {
        background-color: #1a5fb4 !important; color: white !important;
        border-radius: 12px !important; height: 50px !important; width: 100% !important;
        font-weight: bold !important; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 4. SIDEBAR
with st.sidebar:
    st.markdown(f"<div style='background:#28a745; color:white; padding:10px; border-radius:10px; text-align:center;'>🕒 {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
    role = st.radio("GATEWAY:", ["🏠 Patient Kiosk", "🧪 Laboratory", "💊 Pharmacy", "⚙️ Admin Panel"])

# --- PATIENT KIOSK ---
if role == "🏠 Patient Kiosk":
    st.markdown(f"<div class='main-title'>{st.session_state.hosp_name}</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#28a745;'>🛡️ SECURE BIOMETRIC GATEWAY</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="signin-box">', unsafe_allow_html=True)
    p_id = st.text_input("ENTER PATIENT ID:", placeholder="Scan fingerprint or ID...")
    if st.button("AUTHORIZE ACCESS"):
        if p_id in st.session_state.db:
            st.session_state.current_user = p_id
            st.balloons()
        else: st.error("Access Denied.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_user:
        u = st.session_state.db[st.session_state.current_user]
        st.success(f"Verified: {u['izina']}")
        
        # AI CHAT
        if prompt := st.chat_input("Baza AI ikibazo..."):
            with st.chat_message("user"): st.write(prompt)
            try:
                response = model.generate_content(prompt)
                with st.chat_message("assistant"): st.write(response.text)
            except: st.error("AI is unreachable. Check your Secrets.")

# Ibindi bice (Lab, Pharmacy) bimeze nka mbere...
else:
    st.info(f"Welcome to {role}. Please authenticate to continue.")

st.markdown("<div style='text-align:center; margin-top:50px; font-size:10px;'>BJ TECH CYBER-SHIELD ACTIVE</div>", unsafe_allow_html=True)
