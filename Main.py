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
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "system_locked" not in st.session_state:
    st.session_state.system_locked = False
if "messages" not in st.session_state:
    st.session_state.messages = []

MASTER_RECOVERY_KEY = "ndihanomysystem"

# Configure Google AI
genai.configure(api_key="AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
model = genai.GenerativeModel("gemini-pro")

# 2. UI CONFIG
st.set_page_config(page_title="BJ TECH Smart Health", layout="wide", initial_sidebar_state="collapsed")

# CSS KOSOYE (Nta kosa ririmo)
st.markdown("""
<style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .main-title { font-size: 28px; color: #1a5fb4; text-align: center; font-weight: bold; }
    .stButton button { width: 100%; border-radius: 10px; }
    .footer-bj { position: fixed; left: 10px; bottom: 5px; color: #888; font-size: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR
st.sidebar.title("🏥 BJ TECH")
st.sidebar.write(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
role = st.sidebar.selectbox("HITAMO:", ["🏠 Kiosk (Patient)", "🧪 Laboratory", "💊 Pharmacy", "⚙️ Admin Panel"])

# --- PAGE: KIOSK ---
if role == "🏠 Kiosk (Patient)":
    st.markdown(f"<div class='main-title'>{st.session_state.hosp_name}</div>", unsafe_allow_html=True)
    p_id = st.text_input("Enter Patient ID (119958):", placeholder="Type ID here...")
    
    if p_id in st.session_state.db:
        p = st.session_state.db[p_id]
        st.success(f"Muraho {p['izina']}!")
        
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        
        if prompt := st.chat_input("Bwira AI uko umerewe..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            try:
                response = model.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("AI Error")
            st.rerun()

# --- PAGE: LABORATORY ---
elif role == "🧪 Laboratory":
    st.title("🧪 Lab Access")
    pwd = st.text_input("Lab PIN:", type="password")
    if pwd == st.session_state.passwords["lab"]:
        lab_id = st.text_input("Patient ID:")
        if lab_id in st.session_state.db:
            res = st.multiselect("Diagnostic:", ["Malaria", "Typhoid", "Negative"])
            if st.button("Save Results"):
                st.session_state.db[lab_id]["results"] = f"Lab: {', '.join(res)}"
                st.success("Byabitswe!")

# --- PAGE: ADMIN PANEL ---
elif role == "⚙️ Admin Panel":
    st.title("⚙️ Admin")
    a_pwd = st.text_input("Admin PIN:", type="password")
    if a_pwd == st.session_state.passwords["admin"]:
        st.write("Reports List:")
        for pid in st.session_state.db:
            st.write(f"ID: {pid} - {st.session_state.db[pid]['izina']}")

st.markdown("<div class='footer-bj'>POWERED BY BJ TECH LTD</div>", unsafe_allow_html=True)
