import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF
import re

# 1. INITIALIZE SYSTEM STATE (Kugira ngo system itagira ibyo ibura)
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
# Shaka API Key yawe hano: https://aistudio.google.com/app/apikey
genai.configure(api_key="AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
model = genai.GenerativeModel("gemini-pro")

# Helper function for login attempts
def handle_login_attempt():
    st.session_state.login_attempts += 1
    if st.session_state.login_attempts >= 4:
        st.session_state.system_locked = True
    st.rerun()

# 2. PDF GENERATOR (Kunoza raporo itagira error)
def create_pdf(p_id, p_data):
    pdf = FPDF()
    # Add a font if Arial is not found by default. For example:
    # pdf.add_font('Arial', '', 'Arial.ttf', uni=True)
    # pdf.add_font('Arial', 'B', 'Arialbd.ttf', uni=True)
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
    # Gukuramo inyuguti zatera error muri PDF (Unicode Fix)
    clean_res = p_data['results'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_res)
    pdf.ln(20)
    pdf.cell(0, 10, txt="Hospital Stamp & Signature: ____________________", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# 3. SECURITY MONITOR (Kumenya niba bari gu-hackinga)
def check_for_hacking(user_input):
    for word in HACK_KEYWORDS:
        if word.upper() in user_input.upper():
            return True
    return False

# 4. UI STYLE (Hacker Alert & Branding)
st.set_page_config(page_title="BJ TECH Smart Health", layout="wide")
st.markdown(\"\"\"
    <style>
    @keyframes blinker { 50% { opacity: 0; } }
    .hacker-alert { background-color: #ff0000; color: white; padding: 40px; text-align: center; font-size: 35px; font-weight: bold; animation: blinker 0.8s linear infinite; border-radius: 15px; border: 5px solid black; }
    header {visibility: hidden;} #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .stApp { background-image: url("https://img.icons8.com/ios-filled/500/1a5fb4/fingerprint.png"); background-repeat: no-repeat; background-position: center; background-size: 250px; background-color: rgba(255,255,255,0.96); background-blend-mode: overlay; }
    .footer-bj { position: fixed; left: 20px; bottom: 10px; color: #333; font-size: 11px; font-weight: bold; font-family: monospace; }
    </style>
    \"\"\", unsafe_allow_html=True)

# 5. LOCKDOWN SCREEN
if st.session_state.system_locked:
    st.markdown('<div class="hacker-alert">🚨 HACKER ATTACKS DETECTED!<br>SYSTEM AUTO SHUTDOWN<br>ONLY ADMIN OR DEVELOPER CAN UNLOCK</div>', unsafe_allow_html=True)
    unlock = st.text_input("ENTER MASTER RECOVERY KEY:", type="password")
    if unlock == MASTER_RECOVERY_KEY:
        st.session_state.system_locked = False
        st.session_state.login_attempts = 0
        st.rerun()
    st.stop()

# 6. SIDEBAR (Isaha n'Itariki)
st.sidebar.markdown(f"### 🕒 {datetime.now().strftime('%H:%M:%S')}")
st.sidebar.markdown(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
st.sidebar.markdown("---")
role = st.sidebar.radio("BJ TECH MENU:", ["🏠 Kiosk (Patient)", "🧪 Laboratory", "💊 Pharmacy", "⚙️ Admin Panel"])

# --- PAGE: KIOSK (With Input Security) ---
if role == "🏠 Kiosk (Patient)":
    st.markdown(f"<h1 style='color:#1a5fb4; text-align:center;'>{st.session_state.hosp_name}</h1>", unsafe_allow_html=True)
    p_id = st.text_input("Scan ID / Fingerprint:", key="kiosk_id_input")
    
    if check_for_hacking(p_id):
        st.session_state.system_locked = True
        st.rerun()

    if p_id in st.session_state.db:
        p = st.session_state.db[p_id]
        st.success(f"Muraho {p['izina']}! Bwira AI uko umerewe:")
        if st.button("LOGOUT / SOZA"):
            st.session_state.messages = []
            st.rerun()
        
        # Chat Interface
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
        
        if prompt := st.chat_input("Andika hano..."):
            if check_for_hacking(prompt):
                st.session_state.system_locked = True
                st.rerun()
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # AI Response logic (Gemini Integration)
            try:
                response = model.generate_content(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {e}")
            st.rerun()

# --- PAGE: LABORATORY ---
elif role == "🧪 Laboratory":
    st.title("🧪 Laboratory Access")
    pwd = st.text_input("Lab PIN:", type="password")
    if pwd == st.session_state.passwords["lab"]:
        st.session_state.login_attempts = 0
        lab_id = st.text_input("Patient ID:")
        if lab_id in st.session_state.db:
            results = st.multiselect("Diagnostic:", ["Malaria", "Typhoid", "Mitezi", "Mburugu", "Negative"])
            if st.button("Emeza & SMS"):
                res_str = ", ".join(results)
                st.session_state.db[lab_id]["results"] = f"Ibisubizo bya Lab: {res_str}"
                st.success("✅ Byabitswe neza!")
    elif pwd != "":
        if st.button("Verify PIN"):
            handle_login_attempt()

# --- PAGE: PHARMACY ---
elif role == "💊 Pharmacy":
    st.title("💊 Pharmacy Access")
    pwd = st.text_input("Pharmacy PIN:", type="password")
    if pwd == st.session_state.passwords["pharmacy"]:
        st.session_state.login_attempts = 0
        st.info("Pharmacy section is under development.")
    elif pwd != "":
        if st.button("Verify PIN"):
            handle_login_attempt()

# --- PAGE: ADMIN PANEL ---
elif role == "⚙️ Admin Panel":
    st.title("⚙️ System Control Center")
    a_pwd = st.text_input("Admin PIN:", type="password")
    if a_pwd == st.session_state.passwords["admin"]:
        st.session_state.login_attempts = 0
        tab1, tab2 = st.tabs(["📊 Documentation", "🔐 Security Settings"])
        with tab1:
            for pid, pinfo in st.session_state.db.items():
                col1, col2 = st.columns([3, 1])
                col1.write(f"📄 Report: {pinfo['izina']} (ID: {pid})")
                pdf_bytes = create_pdf(pid, pinfo)
                col2.download_button("📥 Download PDF", data=pdf_bytes, file_name=f"BJ_Report_{pid}.pdf", mime="application/pdf", key=f"pdf_{pid}")
        with tab2:
            st.session_state.hosp_name = st.text_input("Update Hospital Name:", st.session_state.hosp_name)
            st.session_state.passwords["lab"] = st.text_input("Update Lab PIN:", st.session_state.passwords["lab"])
            st.session_state.passwords["pharmacy"] = st.text_input("Update Pharmacy PIN:", st.session_state.passwords["pharmacy"])
            st.session_state.passwords["admin"] = st.text_input("Update Admin PIN:", st.session_state.passwords["admin"])
    elif a_pwd != "":
        if st.button("Verify Admin PIN"):
            handle_login_attempt()

st.markdown("<div class='footer-bj'>POWERED BY BJ TECH LTD</div>", unsafe_allow_html=True)
