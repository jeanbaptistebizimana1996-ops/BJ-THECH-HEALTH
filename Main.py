import streamlit as st
import google.generativeai as genai
from datetime import datetime
from fpdf import FPDF
import re

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {"119958": {"izina": "Habineza", "phone": "+250780000000", "results": "Nta kintu kirandikwa", "meds": "Nta miti", "date": "2026-02-24"}}
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
if "current_user" not in st.session_state:
    st.session_state.current_user = None

# MASTER KEYS & SECURITY
MASTER_RECOVERY_KEY = "ndihanomysystem"
HACK_KEYWORDS = ["DROP", "DELETE", "SELECT *", "<script>", "OR 1=1", "UNION ALL"]

# 2. CONFIGURE AI (Using Gemini 1.5 Flash Free Tier)
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("AI Configuration failed. Check Secrets.")

# 3. PDF GENERATOR
def create_pdf(p_id, p_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=st.session_state.hosp_name, ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Report ID: BJ-{p_id} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, txt=f"PATIENT: {p_data['izina']}", ln=True, fill=True)
    pdf.cell(0, 10, txt=f"Phone: {p_data['phone']}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="LAB RESULTS & PRESCRIPTION:", ln=True)
    pdf.set_font("Arial", size=11)
    clean_res = f"Results: {p_data['results']}\nPrescription: {p_data.get('meds', 'Nta miti')}"
    pdf.multi_cell(0, 10, txt=clean_res.encode('latin-1', 'ignore').decode('latin-1'))
    pdf.ln(20)
    pdf.cell(0, 10, txt="Authorized by BJ TECH System", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# 4. SECURITY MONITOR
def check_for_hacking(user_input):
    if not user_input: return False
    for word in HACK_KEYWORDS:
        if word.upper() in user_input.upper():
            return True
    return False

# 5. UI STYLE
st.set_page_config(page_title="BJ TECH Smart Health", layout="wide", page_icon="🏥")
st.markdown("""
<style>
@keyframes blinker { 50% { opacity: 0; } }
.hacker-alert { background-color: #ff0000; color: white; padding: 40px; text-align: center; font-size: 35px; font-weight: bold; animation: blinker 0.8s linear infinite; border-radius: 15px; border: 5px solid black; }
header {visibility: hidden;} footer {visibility: hidden;}
.stApp { 
    background-image: url("https://img.icons8.com/ios-filled/500/1a5fb4/fingerprint.png"); 
    background-repeat: no-repeat; background-position: center; background-size: 250px; 
    background-color: rgba(244,247,250,0.97); background-blend-mode: overlay; 
}
.signin-box {
    background-color: #f1f3f5; padding: 30px; border-radius: 20px; 
    border: 1px solid #dee2e6; box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 25px;
}
.footer-bj { position: fixed; left: 20px; bottom: 10px; color: #1a5fb4; font-size: 11px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 6. LOCKDOWN SCREEN
if st.session_state.system_locked:
    st.markdown('<div class="hacker-alert">🚨 HACKER ATTACK DETECTED!<br>SYSTEM AUTO SHUTDOWN<br>ONLY BJ TECH ADMIN CAN UNLOCK</div>', unsafe_allow_html=True)
    unlock = st.text_input("ENTER MASTER RECOVERY KEY:", type="password")
    if unlock == MASTER_RECOVERY_KEY:
        st.session_state.system_locked = False
        st.session_state.login_attempts = 0
        st.rerun()
    st.stop()

# 7. SIDEBAR
with st.sidebar:
    st.markdown(f"### 🕒 {datetime.now().strftime('%H:%M:%S')}")
    st.markdown(f"📅 {datetime.now().strftime('%d/%m/%Y')}")
    st.divider()
    role = st.sidebar.radio("BJ TECH MENU:", ["🏠 Home (Patient)", "🧪 Laboratory", "💊 Pharmacy", "⚙️ Admin Panel"])
    st.divider()
    if st.button("🔄 Reset Session"): st.rerun()

# --- PAGE: PATIENT KIOSK ---
if role == "🏠 Home (Patient)":
    st.markdown(f"<h1 style='color:#1a5fb4; text-align:center;'>{st.session_state.hosp_name}</h1>", unsafe_allow_html=True)
    
    st.markdown('<div class="signin-box">', unsafe_allow_html=True)
    p_id = st.text_input("Scan ID / Fingerprint:", key="kiosk_id_input")
    
    if p_id:
        if check_for_hacking(p_id):
            st.session_state.system_locked = True
            st.rerun()
        
        if p_id in st.session_state.db:
            st.session_state.current_user = p_id
            st.success(f"Verified: {st.session_state.db[p_id]['izina']}")
        else:
            st.warning("ID not found. Use Admin to register.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.current_user:
        curr = st.session_state.db[st.session_state.current_user]
        st.info(f"Welcome, {curr['izina']}. Ask AI anything about your health.")
        
        # Chat Interface
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.markdown(m["content"])
            
        if prompt := st.chat_input("How are you feeling today?"):
            if check_for_hacking(prompt):
                st.session_state.system_locked = True
                st.rerun()
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                try:
                    full_prompt = f"Patient {curr['izina']} says: {prompt}. Give a medical advice in Kinyarwanda."
                    response = model.generate_content(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except:
                    st.error("AI is busy. Please check connection.")
        
        if st.button("❌ LOGOUT"):
            st.session_state.current_user = None
            st.session_state.messages = []
            st.rerun()

# --- PAGE: LABORATORY ---
elif role == "🧪 Laboratory":
    st.title("🧪 Laboratory Access")
    pwd = st.text_input("Lab PIN:", type="password")
    if pwd == st.session_state.passwords["lab"]:
        st.session_state.login_attempts = 0
        lab_id = st.selectbox("Select Patient ID:", [""] + list(st.session_state.db.keys()))
        if lab_id:
            st.write(f"Patient: **{st.session_state.db[lab_id]['izina']}**")
            results = st.multiselect("Diagnostic:", ["Malaria", "Typhoid", "Negative", "Infection"])
            if st.button("Save Results"):
                st.session_state.db[lab_id]["results"] = ", ".join(results)
                st.success("Results updated.")
    elif pwd != "":
        st.session_state.login_attempts += 1
        if st.session_state.login_attempts >= 4:
            st.session_state.system_locked = True
            st.rerun()

# --- PAGE: PHARMACY ---
elif role == "💊 Pharmacy":
    st.title("💊 Pharmacy Unit")
    pwd = st.text_input("Pharmacy PIN:", type="password")
    if pwd == st.session_state.passwords["pharmacy"]:
        p_id = st.selectbox("Select Patient ID:", [""] + list(st.session_state.db.keys()))
        if p_id:
            p = st.session_state.db[p_id]
            st.warning(f"Lab Results: {p['results']}")
            meds = st.text_area("Enter Medication:")
            if st.button("Confirm Prescription"):
                st.session_state.db[p_id]["meds"] = meds
                st.success("Medication assigned.")

# --- PAGE: ADMIN PANEL ---
elif role == "⚙️ Admin Panel":
    st.title("⚙️ System Control")
    a_pwd = st.text_input("Admin PIN:", type="password")
    if a_pwd == st.session_state.passwords["admin"]:
        tab1, tab2 = st.tabs(["📊 Reports", "🔐 Security"])
        with tab1:
            for pid, pinfo in st.session_state.db.items():
                col1, col2 = st.columns([3, 1])
                col1.write(f"📄 {pinfo['izina']} (ID: {pid})")
                pdf_bytes = create_pdf(pid, pinfo)
                col2.download_button("📥 PDF", data=pdf_bytes, file_name=f"BJ_{pid}.pdf", key=f"pdf_{pid}")
        with tab2:
            st.session_state.hosp_name = st.text_input("Hospital Name:", st.session_state.hosp_name)
    elif a_pwd != "":
        st.session_state.login_attempts += 1
        if st.session_state.login_attempts >= 4:
            st.session_state.system_locked = True
            st.rerun()

st.markdown("<div class='footer-bj'>POWERED BY BJ TECH LTD</div>", unsafe_allow_html=True)
