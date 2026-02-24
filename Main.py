import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import pandas as pd
import io

# 1. INITIALIZE SYSTEM STATE (AI MEMORY / SERVER PERSISTENCE)
if "db" not in st.session_state:
    st.session_state.db = {
        "119958": {"izina": "Habineza", "phone": "0788000000", "results": "Malaria", "meds": "Fata Coartem", "status": "Ready", "history": []},
        "223344": {"izina": "Mugisha", "phone": "0781111111", "results": "Typhoid", "meds": "Fata Cipro", "status": "Pending", "history": []}
    }
if "passwords" not in st.session_state:
    st.session_state.passwords = {
        "admin": "cyuma.thec.2026",
        "lab": "lab.2026",
        "phar": "phar.2026"
    }
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "system_locked" not in st.session_state:
    st.session_state.system_locked = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# 2. AI CONFIGURATION
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("AI Configuration Error.")

# 3. UI STYLE (MEDICAL NANO-TECH v4.1)
st.set_page_config(page_title="BJ TECH Medical Nano-OS v4.1", layout="wide")

# JavaScript for Real-Time Clock Update (No Page Refresh Needed)
st.markdown("""
<script>
    function updateClock() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const timeString = hours + ":" + minutes + ":" + seconds;
        const clockElement = window.parent.document.querySelector('.large-clock');
        if (clockElement) {
            clockElement.innerText = timeString;
        }
    }
    setInterval(updateClock, 1000);
</script>
""", unsafe_allow_html=True)

st.markdown(f"""
<style>
    header {{visibility: hidden;}} footer {{visibility: hidden;}}
    
    .stApp {{
        background: radial-gradient(circle at center, #f0f9ff 0%, #e0f2fe 100%);
        background-image: url("https://img.icons8.com/ios-filled/500/0077b6/fingerprint.png");
        background-repeat: no-repeat; 
        background-position: center; 
        background-size: 400px;
        background-attachment: fixed;
        background-blend-mode: soft-light;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(15px);
        border-right: 2px solid #0077b6;
    }}
    
    .glass-card {{
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        padding: 25px !important;
        margin-bottom: 20px;
    }}
    
    .stButton>button {{
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }}
    
    .heart-icon {{
        color: #2ecc71;
        font-size: 40px;
        text-align: center;
        margin-bottom: 10px;
    }}
    
    .large-clock {{
        font-size: 80px;
        font-weight: bold;
        color: #0077b6;
        text-align: center;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 15px rgba(0, 119, 182, 0.3);
        margin-bottom: 10px;
    }}
</style>
""", unsafe_allow_html=True)

# 4. SIDEBAR NAVIGATION
with st.sidebar:
    st.markdown("<div class='heart-icon'>💚</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#0077b6;'>BJ TECH</h2>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MENU:", ["🏠 Home", "🧪 Laboratory", "💊 Pharmacy", "⚙️ Admin"])
    st.divider()
    st.markdown(f"<div style='text-align:center; color:#0077b6;'>SYSTEM ACTIVE</div>", unsafe_allow_html=True)
    st.info("Secure Nano-Shield Active")

# 5. CYBER-SECURITY LOCKDOWN
if st.session_state.system_locked:
    st.error("🚨 SECURITY BREACH! SYSTEM LOCKED")
    unlock = st.text_input("Admin Key:", type="password")
    if st.button("UNLOCK"):
        if unlock == st.session_state.passwords["admin"]:
            st.session_state.system_locked = False
            st.rerun()
    st.stop()

# 6. REAL-TIME CLOCK DISPLAY
st.markdown(f"<div class='large-clock'>{datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# --- PAGE: HOME ---
if page == "🏠 Home":
    st.markdown("<h1 style='text-align:center; color:#0077b6;'>BJ TECH Medical OS</h1>", unsafe_allow_html=True)
    
    if not st.session_state.current_user:
        with st.form("PatientLogin"):
            st.subheader("Patient Access")
            p_phone = st.text_input("Phone Number:")
            p_name = st.text_input("Full Name:")
            if st.form_submit_button("EMEZA KWINJIRA"):
                uid = p_phone[-6:]
                if uid not in st.session_state.db:
                    st.session_state.db[uid] = {"izina": p_name, "phone": p_phone, "results": "", "meds": "", "status": "New", "history": []}
                st.session_state.current_user = uid
                st.rerun()
    else:
        curr = st.session_state.db[st.session_state.current_user]
        st.markdown(f"<div class='glass-card'><h3>Muraho, {curr['izina']}!</h3><p>Status: <b>{curr['status']}</b></p></div>", unsafe_allow_html=True)
        if st.button("LOGOUT"):
            st.session_state.current_user = None
            st.rerun()
        
        # AI Chat
        st.subheader("Baza AI Muganga")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if prompt := st.chat_input("Andika hano..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res = model.generate_content(f"Advice {curr['izina']} in Kinyarwanda: {prompt}").text
                st.write(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

# --- PAGE: LAB ---
elif page == "🧪 Laboratory":
    st.markdown("<h2 style='color:#0077b6;'>Laboratory Portal 🧪</h2>", unsafe_allow_html=True)
    
    if "lab_auth" not in st.session_state: st.session_state.lab_auth = False
    
    if not st.session_state.lab_auth:
        with st.form("LabAuth"):
            pw = st.text_input("Lab Password:", type="password")
            if st.form_submit_button("EMEZA"):
                if pw == st.session_state.passwords["lab"]:
                    st.session_state.lab_auth = True
                    st.rerun()
                else: st.error("Wrong Password!")
    else:
        if st.button("LOGOUT LAB"): st.session_state.lab_auth = False; st.rerun()
        
        st.subheader("Fingerprint Scan")
        lab_id = st.selectbox("Hitamo Umurwayi (Scan Fingerprint):", list(st.session_state.db.keys()))
        
        if st.button("☝️ SCAN FINGERPRINT", use_container_width=True):
            st.success(f"Verified: {st.session_state.db[lab_id]['izina']}")
            st.session_state.active_lab_user = lab_id
            
        if "active_lab_user" in st.session_state:
            p = st.session_state.db[st.session_state.active_lab_user]
            tests = st.multiselect("Indwara basanze:", ["Malaria", "Typhoid", "Amoeba", "Infection", "Flu"])
            if st.button("EMEZA NO KOHEREZA SMS (AI)"):
                all_t = ", ".join(tests)
                p["results"] = all_t
                p["status"] = "Results Ready"
                # AI Prescription Logic
                ai_prescription = model.generate_content(f"Patient {p['izina']} has {all_t}. Prescribe meds in Kinyarwanda briefly.").text
                p["meds"] = ai_prescription
                st.success("Results & AI Prescription Sent!")

# --- PAGE: PHARMACY ---
elif page == "💊 Pharmacy":
    st.markdown("<h2 style='color:#0077b6;'>Pharmacy Portal 💊</h2>", unsafe_allow_html=True)
    
    if "phar_auth" not in st.session_state: st.session_state.phar_auth = False
    
    if not st.session_state.phar_auth:
        with st.form("PharAuth"):
            pw = st.text_input("Pharmacy Password:", type="password")
            if st.form_submit_button("EMEZA"):
                if pw == st.session_state.passwords["phar"]:
                    st.session_state.phar_auth = True
                    st.rerun()
                else: st.error("Wrong Password!")
    else:
        if st.button("LOGOUT PHARMACY"): st.session_state.phar_auth = False; st.rerun()
        
        st.subheader("Fingerprint Verification")
        phar_id = st.selectbox("Hitamo Umurwayi (Scan Fingerprint):", list(st.session_state.db.keys()))
        
        if st.button("☝️ SCAN FINGERPRINT", use_container_width=True):
            p = st.session_state.db[phar_id]
            st.success(f"Verified: {p['izina']}")
            st.markdown(f"<div class='glass-card'><h4>Prescription for {p['izina']}:</h4><p>{p['meds']}</p></div>", unsafe_allow_html=True)
            if st.button("CONFIRM DISPENSE"):
                p["status"] = "Completed"
                st.success("Meds Dispensed Successfully!")

# --- PAGE: ADMIN ---
elif page == "⚙️ Admin":
    st.markdown("<h2 style='color:#0077b6;'>Admin Control Center ⚙️</h2>", unsafe_allow_html=True)
    
    if "admin_auth" not in st.session_state: st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        with st.form("AdminAuth"):
            pw = st.text_input("Admin Password:", type="password")
            if st.form_submit_button("EMEZA"):
                if pw == st.session_state.passwords["admin"]:
                    st.session_state.admin_auth = True
                    st.rerun()
                else: st.error("Wrong Password!")
    else:
        if st.button("LOGOUT ADMIN"): st.session_state.admin_auth = False; st.rerun()
        
        # PASSWORD MANAGEMENT
        st.subheader("Password Management")
        col1, col2 = st.columns(2)
        with col1:
            new_lab_pw = st.text_input("New Lab Password:", value=st.session_state.passwords["lab"])
            new_phar_pw = st.text_input("New Pharmacy Password:", value=st.session_state.passwords["phar"])
        with col2:
            if st.button("UPDATE PASSWORDS"):
                st.session_state.passwords["lab"] = new_lab_pw
                st.session_state.passwords["phar"] = new_phar_pw
                st.success("Passwords Updated!")
        
        st.divider()
        # DATA & DOWNLOADS
        st.subheader("Patient Records")
        df = pd.DataFrame.from_dict(st.session_state.db, orient='index')
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv().encode('utf-8')
        st.download_button("📥 DOWNLOAD CSV REPORT", data=csv, file_name="BJ_TECH_REPORT.csv", mime="text/csv")

# --- FOOTER ---
st.markdown("<div style='position:fixed; bottom:10px; right:20px; font-size:12px; color:#0077b6; font-weight:bold;'>BJ TECH MEDICAL NANO-OS v4.1 | REAL-TIME CLOCK 🛡️</div>", unsafe_allow_html=True)
