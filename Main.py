import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {"119958": {"izina": "Habineza", "phone": "+250780000000", "results": "Nta kintu kirandikwa", "date": "2026-02-23"}}
if "passwords" not in st.session_state:
    st.session_state.passwords = {"lab": "lab.2026", "pharmacy": "phar.2026", "admin": "cyuma.thec.2026"}
if "hosp_name" not in st.session_state:
    st.session_state.hosp_name = "BJ TECH MEDICAL CENTER"
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. CONFIGURE AI (SECRETS MODE)
# Icyitonderwa: Ugomba gushyira GEMINI_API_KEY muri Streamlit Secrets kugira ngo iyi gice gihite gikora.
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        # Niba utarayishyira muri Secrets, koresha iyi idahuye neza (ariko gushyira muri Secrets ni bwo buryo bwiza)
        api_key = "AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
except Exception as e:
    st.error("AI Configuration Error. Reba Secrets zawe.")

# 3. UI CONFIG & DESIGN
st.set_page_config(page_title="BJ TECH Health", page_icon="🏥", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #ffffff; }
    header {visibility: hidden;}
    .main-title { font-size: 28px; color: #1a5fb4; text-align: center; font-weight: bold; margin-top: -40px; }
    .clock-container { 
        background-color: #ff4b4b; color: white; padding: 10px; 
        border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 20px;
    }
    .icon-header { text-align: center; font-size: 60px; margin-top: 10px; }
    /* Buto nini y'uburu (Blue Button) */
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        background-color: #1a5fb4 !important; color: white !important;
        border-radius: 15px !important; font-size: 20px !important; font-weight: bold !important;
    }
    .footer-text { text-align: center; color: #777; font-size: 12px; margin-top: 50px; border-top: 1px solid #eee; padding-top: 10px; }
</style>
""", unsafe_allow_html=True)

# 4. SIDEBAR (Isaha n'Menu)
with st.sidebar:
    st.markdown(f"""
    <div class='clock-container'>
        <span style='font-size: 24px;'>🕒 {datetime.now().strftime('%H:%M:%S')}</span><br>
        <span style='font-size: 14px;'>📅 {datetime.now().strftime('%d/%m/%Y')}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    role = st.radio("SELECT DEPARTMENT:", ["🏠 Patient Kiosk", "🧪 Laboratory", "💊 Pharmacy", "⚙️ Admin Panel"])
    st.markdown("---")
    st.info("BJ TECH SYSTEM v2.0")

# --- PAGE: PATIENT KIOSK ---
if role == "🏠 Patient Kiosk":
    st.markdown("<div class='icon-header'>👤</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='main-title'>{st.session_state.hosp_name}</div>", unsafe_allow_html=True)
    
    p_id_input = st.text_input("SCAN ID / ANDIKA ID (119958):", placeholder="Click hano wandike...")
    
    # Buto yo kwinjira itagombye Enter
    if st.button("🚀 LOGIN / INJIRA"):
        if p_id_input in st.session_state.db:
            st.session_state.current_user = p_id_input
            st.balloons()
        else:
            st.error("⚠️ ID Ntabwo yabonetse muri System!")

    if st.session_state.current_user:
        p = st.session_state.db[st.session_state.current_user]
        st.success(f"Ikaze, **{p['izina']}**! Baza AI ikibazo cyose ku buzima bwawe.")
        st.divider()
        
        # Chat History
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        
        # AI Input
        if prompt := st.chat_input("Andika hano (Urugero: 'Mumbwire uko navura umutwe')..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except:
                    st.error("AI ntishoboye gusubiza ubu. Reba API Key muri Secrets.")

        if st.button("❌ LOGOUT / SOHOKA"):
            st.session_state.current_user = None
            st.session_state.messages = []
            st.rerun()

# --- PAGE: LABORATORY ---
elif role == "🧪 Laboratory":
    st.markdown("<div class='icon-header'>🧪</div>", unsafe_allow_html=True)
    st.title("Laboratory Access")
    l_pwd = st.text_input("Lab Access PIN:", type="password")
    if st.button("🔓 VERIFY & ENTER"):
        if l_pwd == st.session_state.passwords["lab"]:
            st.success("Access Granted!")
            # Lab logic hano...
        else:
            st.error("PIN siyo!")

# --- PAGE: ADMIN PANEL ---
elif role == "⚙️ Admin Panel":
    st.markdown("<div class='icon-header'>⚙️</div>", unsafe_allow_html=True)
    st.title("Admin Master Control")
    a_pwd = st.text_input("Admin PIN:", type="password")
    if st.button("🔐 OPEN DASHBOARD"):
        if a_pwd == st.session_state.passwords["admin"]:
            st.write("### Patient Database:")
            st.json(st.session_state.db)
        else:
            st.error("Admin PIN incorrect!")

st.markdown("<div class='footer-text'>🚀 BJ TECH LTD - SMART HEALTH SOLUTIONS © 2026</div>", unsafe_allow_html=True)
