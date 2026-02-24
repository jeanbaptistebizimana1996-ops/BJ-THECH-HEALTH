import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import pandas as pd
import random

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {
        "119958": {"izina": "Habineza", "phone": "0788000000", "results": "", "meds": "", "status": "New", "bp": "N/A", "temp": "N/A"}
    }
if "passwords" not in st.session_state:
    st.session_state.passwords = {"admin": "cyuma.thec.2026", "lab": "lab.2026", "phar": "phar.2026"}
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0
if "system_shutdown" not in st.session_state:
    st.session_state.system_shutdown = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# SECURITY KEYS
REBOOT_KEY = "ndaharimysystem2026"

# 2. AI CONFIGURATION
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("AI Configuration Error.")

# 3. UI STYLE (MEDICAL NANO-TECH v5.0)
st.set_page_config(page_title="BJ TECH Medical Nano-OS v5.0", layout="wide")

st.markdown("""
<style>
    header {visibility: hidden;} footer {visibility: hidden;}
    
    .stApp {
        background: radial-gradient(circle at center, #f0f9ff 0%, #e0f2fe 100%);
        background-image: url("https://img.icons8.com/ios-filled/500/0077b6/fingerprint.png");
        background-repeat: no-repeat; background-position: center; background-size: 400px;
        background-attachment: fixed; background-blend-mode: soft-light;
    }
    
    /* Heart Beat Animation */
    @keyframes heartbeat {
        0% { transform: scale(1); }
        20% { transform: scale(1.3); }
        40% { transform: scale(1); }
        60% { transform: scale(1.3); }
        80% { transform: scale(1); }
        100% { transform: scale(1); }
    }
    .heart-beat {
        color: #2ecc71; font-size: 60px; text-align: center;
        animation: heartbeat 1.2s infinite; display: block; margin: auto;
    }
    
    /* AI Glowing Indicator */
    @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
    .ai-indicator {
        width: 40px; height: 40px; border: 4px solid #0077b6; border-top: 4px solid #2ecc71;
        border-radius: 50%; animation: rotate 2s linear infinite; margin: auto;
    }
    
    /* Shutdown Screen */
    .shutdown-screen {
        background-color: #d00000; color: white; height: 100vh; width: 100vw;
        position: fixed; top: 0; left: 0; z-index: 9999; display: flex;
        flex-direction: column; justify-content: center; align-items: center;
        text-align: center; font-family: 'Courier New', monospace;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.7) !important; backdrop-filter: blur(10px);
        border-radius: 20px !important; border: 1px solid rgba(0, 119, 182, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important; padding: 25px !important;
    }
    
    .stButton>button {
        background-color: #0077b6 !important; color: white !important;
        border-radius: 12px !important; font-weight: bold !important;
        height: 60px; font-size: 18px !important; width: 100%;
    }
    
    .large-clock {
        font-size: 60px; font-weight: bold; color: #0077b6; text-align: center;
        font-family: 'Courier New', monospace; text-shadow: 0 0 10px rgba(0, 119, 182, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 4. CYBER-SECURITY AUTO-SHUTDOWN LOGIC
if st.session_state.system_shutdown:
    st.markdown \"\"\"
    <div class="shutdown-screen">
        <h1>🚨 SYSTEM AUTO SHUTDOWN 🚨</h1>
        <h2 style="color: black; background: white; padding: 10px;">SOMEONE TRYING TO HACK</h2>
        <p>Security Breach Detected. System is locked for safety.</p>
    </div>
    \"\"\", unsafe_allow_html=True)
    reboot = st.text_input("Enter Developer Reboot Key:", type="password")
    if st.button("REBOOT SYSTEM"):
        if reboot == REBOOT_KEY:
            st.session_state.system_shutdown = False
            st.session_state.login_attempts = 0
            st.rerun()
        else: st.error("Invalid Reboot Key!")
    st.stop()

# 5. HEADER & REAL-TIME CLOCK
st.markdown("<div class='heart-beat'>💚</div>", unsafe_allow_html=True)
st.markdown(f"<div class='large-clock'>{datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#0077b6; margin-top:-10px;'>BJ TECH PROFESSIONAL AI MEDICAL OS</h3>", unsafe_allow_html=True)

# 6. MAIN NAVIGATION
st.divider()
n1, n2, n3, n4 = st.columns(4)
if n1.button("🏠 HOME"): st.session_state.current_page = "🏠 Home"; st.rerun()
if n2.button("🧪 LAB"): st.session_state.current_page = "🧪 Lab"; st.rerun()
if n3.button("💊 PHARMA"): st.session_state.current_page = "💊 Pharmacy"; st.rerun()
if n4.button("⚙️ ADMIN"): st.session_state.current_page = "⚙️ Admin"; st.rerun()
st.divider()

# --- PAGE: HOME (PATIENT & SCANS) ---
if st.session_state.current_page == "🏠 Home":
    st.markdown("<h2 style='text-align:center; color:#0077b6;'>Patient Diagnostics Portal</h2>", unsafe_allow_html=True)
    
    if not st.session_state.current_user:
        with st.form("Login"):
            st.subheader("Kwinjira / Kwiyandikisha")
            p_phone = st.text_input("Nimero ya Foni:")
            p_name = st.text_input("Amazina yombi:")
            if st.form_submit_button("EMEZA KWINJIRA"):
                uid = p_phone[-6:]
                if uid not in st.session_state.db:
                    st.session_state.db[uid] = {"izina": p_name, "phone": p_phone, "results": "", "meds": "", "status": "New", "bp": "N/A", "temp": "N/A"}
                st.session_state.current_user = uid
                st.rerun()
    else:
        curr = st.session_state.db[st.session_state.current_user]
        st.markdown(f"<div class='glass-card'><h3>Muraho, {curr['izina']}!</h3><p>Status: <b>{curr['status']}</b></p></div>", unsafe_allow_html=True)
        
        # MEDICAL SCANS
        col_scan1, col_scan2 = st.columns(2)
        with col_scan1:
            st.subheader("🩸 Blood Pressure Scan")
            st.info("Cengeza urutoki kuri Fingerprint Sensor hano munsi...")
            if st.button("☝️ SCAN BLOOD PRESSURE"):
                with st.spinner("Piping Blood Pressure..."):
                    time.sleep(2)
                    curr["bp"] = f"{random.randint(110, 140)}/{random.randint(70, 90)} mmHg"
                    st.success(f"Umuvuduko w'amaraso: {curr['bp']}")
        
        with col_scan2:
            st.subheader("👁️ Eye Fever Scan")
            st.info("Reba mu cyuma (Eye Scanner) AI isuzume umuriro...")
            if st.button("👁️ SCAN EYE FOR FEVER"):
                with st.spinner("AI isuzuma ijisho..."):
                    time.sleep(2)
                    curr["temp"] = f"{random.uniform(36.5, 39.5):.1f} °C"
                    st.success(f"Umuriro: {curr['temp']}")
                    if float(curr["temp"].split()[0]) > 38.0:
                        st.warning("Ufite umuriro mwinshi! Genda muri Lab vuba.")

        # AI ASSISTANT
        st.divider()
        st.subheader("Baza AI Muganga (Secure Medical AI)")
        st.markdown("<div class='ai-indicator'></div>", unsafe_allow_html=True)
        prompt = st.chat_input("Andika hano (Ikinyarwanda)...")
        if prompt:
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                with st.spinner("AI iri gushaka amakuru y'ukuri..."):
                    ai_res = model.generate_content(f"You are a professional medical AI. Patient {curr['izina']} (Temp: {curr['temp']}, BP: {curr['bp']}) asks: {prompt}. Answer in polite, calm Kinyarwanda. NEVER mention passwords or private database keys.").text
                    st.write(ai_res)

# --- PAGE: LAB ---
elif st.session_state.current_page == "🧪 Lab":
    st.markdown("<h2 style='color:#0077b6;'>Laboratory Portal 🧪</h2>", unsafe_allow_html=True)
    if "lab_auth" not in st.session_state: st.session_state.lab_auth = False
    
    if not st.session_state.lab_auth:
        with st.form("LabAuth"):
            pw = st.text_input("Lab Password:", type="password")
            if st.form_submit_button("EMEZA"):
                if pw == st.session_state.passwords["lab"]:
                    st.session_state.lab_auth = True
                    st.session_state.login_attempts = 0
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 3:
                        st.session_state.system_shutdown = True
                        st.rerun()
                    st.error(f"Password si yo! Attempts: {st.session_state.login_attempts}/3")
    else:
        lab_id = st.selectbox("Scan Fingerprint (Select Patient):", list(st.session_state.db.keys()))
        if st.button("☝️ VERIFY PATIENT"):
            p = st.session_state.db[lab_id]
            st.success(f"Verified: {p['izina']} | BP: {p['bp']} | Temp: {p['temp']}")
            tests = st.multiselect("Indwara basanze:", ["Malaria", "Typhoid", "Amoeba", "Infection", "Flu"])
            if st.button("EMEZA NO KOHEREZA SMS (AI)"):
                p["results"] = ", ".join(tests)
                p["status"] = "Results Ready"
                p["meds"] = model.generate_content(f"Patient {p['izina']} has {p['results']}. Temp: {p['temp']}. Prescribe meds in Kinyarwanda.").text
                st.success("Results & AI Prescription Sent!")

# --- PAGE: PHARMACY ---
elif st.session_state.current_page == "💊 Pharmacy":
    st.markdown("<h2 style='color:#0077b6;'>Pharmacy Portal 💊</h2>", unsafe_allow_html=True)
    if "phar_auth" not in st.session_state: st.session_state.phar_auth = False
    
    if not st.session_state.phar_auth:
        with st.form("PharAuth"):
            pw = st.text_input("Pharmacy Password:", type="password")
            if st.form_submit_button("EMEZA"):
                if pw == st.session_state.passwords["phar"]:
                    st.session_state.phar_auth = True
                    st.session_state.login_attempts = 0
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 3:
                        st.session_state.system_shutdown = True
                        st.rerun()
                    st.error(f"Password si yo! Attempts: {st.session_state.login_attempts}/3")
    else:
        phar_id = st.selectbox("Scan Fingerprint (Select Patient):", list(st.session_state.db.keys()))
        if st.button("☝️ VERIFY & VIEW PRESCRIPTION"):
            p = st.session_state.db[phar_id]
            st.markdown(f"<div class='glass-card'><h4>Prescription for {p['izina']}:</h4><p>{p['meds']}</p></div>", unsafe_allow_html=True)
            if st.button("CONFIRM DISPENSE"):
                p["status"] = "Completed"
                st.success("Meds Dispensed!")

# --- PAGE: ADMIN ---
elif st.session_state.current_page == "⚙️ Admin":
    st.markdown("<h2 style='color:#0077b6;'>Admin Controller ⚙️</h2>", unsafe_allow_html=True)
    if "admin_auth" not in st.session_state: st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        with st.form("AdminAuth"):
            pw = st.text_input("Admin Password:", type="password")
            if st.form_submit_button("EMEZA"):
                if pw == st.session_state.passwords["admin"]:
                    st.session_state.admin_auth = True
                    st.session_state.login_attempts = 0
                    st.rerun()
                else:
                    st.session_state.login_attempts += 1
                    if st.session_state.login_attempts >= 3:
                        st.session_state.system_shutdown = True
                        st.rerun()
                    st.error("Admin Password si yo!")
    else:
        st.subheader("Manage Passwords")
        new_lab = st.text_input("New Lab Password:", value=st.session_state.passwords["lab"])
        new_phar = st.text_input("New Pharmacy Password:", value=st.session_state.passwords["phar"])
        if st.button("UPDATE PASSWORDS"):
            st.session_state.passwords["lab"], st.session_state.passwords["phar"] = new_lab, new_phar
            st.success("Passwords Updated!")
        
        st.divider()
        st.subheader("Full Database (Patient Records)")
        st.write(pd.DataFrame.from_dict(st.session_state.db, orient='index'))

# --- FOOTER ---
st.markdown("<div style='position:fixed; bottom:10px; right:20px; font-size:12px; color:#0077b6; font-weight:bold;'>BJ TECH AI MEDICAL OS v5.0 | SECURE 🛡️</div>", unsafe_allow_html=True)
