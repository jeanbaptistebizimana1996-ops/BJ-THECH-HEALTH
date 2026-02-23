import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF
import re

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

# MASTER KEYS
MASTER_RECOVERY_KEY = "ndihanomysystem"
HACK_KEYWORDS = ["DROP", "DELETE", "SELECT *", "<script>", "OR 1=1"]

# Configure Google Generative AI
genai.configure(api_key="AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
model = genai.GenerativeModel("gemini-pro")

# Helper function for login attempts
def handle_login_attempt():
    st.session_state.login_attempts += 1
    if st.session_state.login_attempts >= 4:
        st.session_state.system_locked = True
    st.rerun()

# 2. PDF GENERATOR
def create_pdf(p_id, p_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=st.session_state.hosp_name, ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Report ID: BJ-{p_id} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, txt=f"PATIENT: {p_data['izina']}", ln=True, fill=True)
    pdf.cell(0, 10, txt=f"Phone: {p_data['phone']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="DIAGNOSIS & PRESCRIPTION:", ln=True)
    pdf.set_font("Arial", size=11)
    clean_res = p_data['results'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_res)
    pdf.ln(20)
    pdf.cell(0, 10, txt="Hospital Stamp & Signature: ____________________", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# 3. SECURITY MONITOR
def check_for_hacking(user_input):
    for word in HACK_KEYWORDS:
        if word.upper() in user_input.upper():
            return True
    return False

# 4. MOBILE-FRIENDLY UI STYLE
st.set_page_config(
    page_title="BJ TECH Smart Health",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Responsive adjustment for Mobile */
    @media (max-width: 600px) {
        .main-title { font-size: 22px !important; }
        .stButton button { width: 100% !important; border-radius: 10px; }
        .hacker-alert { font-size: 20px !important; padding: 20px !important; }
    }
    
    @keyframes blinker { 50% { opacity: 0; } }
    .hacker-alert { background-color: #ff0000; color: white; padding: 30px; text-align: center; font-size: 30px; font-weight: bold; animation: blinker 0.8s linear infinite; border-radius: 15px; border: 4px solid black; }
    
    header {visibility: hidden;} 
    #MainMenu
