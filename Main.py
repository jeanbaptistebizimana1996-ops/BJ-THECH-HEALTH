import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import pandas as pd
import random
import pytz
import os

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {}

if "passwords" not in st.session_state:
    st.session_state.passwords = {
        "admin": "cyuma.thec.2026",
        "lab": "lab.2026",
        "phar": "phar.2026",
    }

if "hospital_name" not in st.session_state:
    st.session_state.hospital_name = "BJ Nano v8 Health Rwanda"

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "system_shutdown" not in st.session_state:
    st.session_state.system_shutdown = False

if "current_user_id" not in st.session_state:
    st.session_state.current_user_id = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 HOME"

if "scan_status" not in st.session_state:
    st.session_state.scan_status = "idle"

# SECURITY KEYS
REBOOT_KEY = "ndihanomysystem"

# 2. AI CONFIGURATION (GEMINI 2.5 FLASH)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Using gemini-2.0-flash or gemini-1.5-flash as 2.5 is preview/latest
    model = genai.GenerativeModel('gemini-2.0-flash') 
except Exception:
    model = None

# 3. UI STYLE & DYNAMIC BACKGROUNDS
st.set_page_config(page_title=st.session_state.hospital_name, layout="wide")

def play_sound(sound_type):
    urls = {
        "error": "https://www.soundjay.com/buttons/beep-05.mp3",
        "success": "https://www.soundjay.com/buttons/button-3.mp3",
        "shutdown": "https://www.soundjay.com/communication/alarm-clock-elapsed-01.mp3",
        "emergency": "https://www.soundjay.com/communication/ambulance-siren-01.mp3"
    }
    st.markdown(f'<audio autoplay><source src="{urls[sound_type]}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# Define Page Colors
page_colors = {
    "🏠 HOME": "rgba(10, 10, 40, 0.9)",
    "🧪 LAB": "rgba(10, 40, 10, 0.9)",
    "💊 PHARMA": "rgba(40, 40, 10, 0.9)",
    "⚙️ ADMIN": "rgba(40, 10, 10, 0.9)"
}
current_bg = page_colors.get(st.session_state.current_page, "rgba(10,10,10,0.9)")

if st.session_state.scan_status == "scanning":
    current_bg = "rgba(255, 0, 0, 0.5)"
elif st.session_state.scan_status == "success":
    current_bg = "rgba(0, 255, 0, 0.5)"

st.markdown(f"""
<style>
    header {{ visibility:hidden; }}
    footer {{ visibility:hidden; }}
    .stApp {{
        background: radial-gradient(circle at center, {current_bg} 0%, rgba(5,5,5,1) 100%), 
                    url("https://img.icons8.com/ios-filled/500/00d4ff/fingerprint.png");
        background-repeat: no-repeat; background-position: center; background-size: 600px;
        background-attachment: fixed; background-blend-mode: overlay;
        color: #e0e0e0; transition: background 0.8s ease;
    }}
    .scrolling-text {{
        width: 100%; overflow: hidden; white-space: nowrap;
        animation: scroll 20s linear infinite; font-size: 22px; font-weight: bold;
        color: #00d4ff; padding: 10px 0; border-bottom: 1px solid #00d4ff;
    }}
    @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    .stethoscope {{ font-size: 70px; text-align: center; animation: pulse 1.5s infinite; color: #00d4ff; }}
    @keyframes pulse {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} 100% {{ transform: scale(1); }} }}
    .emergency-btn {{ background-color: #ff0000 !important; color: white !important; font-weight: bold !important; border: 2px solid white !important; }}
    .ai-led {{ width: 12px; height: 12px; background-color: #00ff00; border-radius: 50%; display: inline-block; box-shadow: 0 0 10px #00ff00; animation: blink 1.5s infinite; }}
    @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
</style>
<div class="scrolling-text">{st.session_state.hospital_name} | Biometric V8 System | Emergency Ready</div>
""", unsafe_allow_html=True)

# 4. SECURITY CHECK
if st.session_state.system_shutdown:
    play_sound("shutdown")
    st.markdown("<div style='background:#d00000;color:white;height:100vh;width:100vw;position:fixed;top:0;left:0;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;'><h1>🚨 SYSTEM LOCKED 🚨</h1><p>Security Breach. Enter Developer Key.</p></div>", unsafe_allow_html=True)
    reboot = st.text_input("Developer Key:", type="password")
    if st.button("UNLOCK"):
        if reboot == REBOOT_KEY:
            st.session_state.system_shutdown = False
            st.session_state.login_attempts = 0
            st.rerun()
    st.stop()

# 5. HEADER
kigali_tz = pytz.timezone('Africa/Kigali')
kigali_time = datetime.now(kigali_tz).strftime("%H:%M:%S")
st.markdown("<div class='stethoscope'>🩺</div>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;color:#00d4ff;'>{kigali_time}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'><span class='ai-led'></span> Gemini 2.5 Online</p>", unsafe_allow_html=True)

# 6. NAVIGATION
st.divider()
c1, c2, c3, c4 = st.columns(4)
if c1.button("🏠 HOME", use_container_width=True): st.session_state.current_page = "🏠 HOME"; st.rerun()
if c2.button("🧪 LAB", use_container_width=True): st.session_state.current_page = "🧪 LAB"; st.rerun()
if c3.button("💊 PHARMA", use_container_width=True): st.session_state.current_page = "💊 PHARMA"; st.rerun()
if c4.button("⚙️ ADMIN", use_container_width=True): st.session_state.current_page = "⚙️ ADMIN"; st.rerun()

# EMERGENCY BUTTON
if st.sidebar.button("🚨 EMERGENCY 🚨", use_container_width=True):
    play_sound("emergency")
    st.sidebar.error("EMERGENCY MODE ACTIVE!")

# =========================
# PAGE: HOME
# =========================
if st.session_state.current_page == "🏠 HOME":
    st.subheader("📱 Biometric Access")
    t1, t2 = st.tabs(["Register", "Scan"])
    with t1:
        with st.form("Reg"):
            n = st.text_input("Name"); p = st.text_input("Phone")
            if st.form_submit_button("REGISTER"):
                st.session_state.scan_status = "scanning"; time.sleep(1)
                fid = f"FP-{random.randint(1000,9999)}"
                st.session_state.db[fid] = {"name":n, "phone":p, "bp":"N/A", "temp":"N/A", "status":"New", "prescription":""}
                st.session_state.scan_status = "success"; play_sound("success")
                st.success(f"✅ Correct! ID: {fid}"); st.session_state.current_user_id = fid; st.rerun()
    with t2:
        sid = st.text_input("Scan ID")
        if st.button("VERIFY"):
            st.session_state.scan_status = "scanning"; time.sleep(1)
            if sid in st.session_state.db:
                st.session_state.scan_status = "success"; play_sound("success")
                st.session_state.current_user_id = sid; st.rerun()
            else: play_sound("error"); st.error("Fingerprint Error!")

    if st.session_state.current_user_id:
        u = st.session_state.db[st.session_state.current_user_id]
        st.info(f"Patient: {u['name']}")
        if st.button("🩺 SCAN VITALS"):
            u["bp"] = f"{random.randint(110,140)}/80"; u["temp"] = f"{random.uniform(36.5,38.5):.1f}"
            st.write(f"BP: {u['bp']} | Temp: {u['temp']}")
        
        prompt = st.chat_input("Baza AI...")
        if prompt:
            emergency_words = ["umubyeyi uri kunda", "kuva amaraso", "ntabwo ari guhumeka", "indwara ikomeye"]
            if any(word in prompt.lower() for word in emergency_words):
                play_sound("emergency"); st.error("🚨 ALERT: Emergency Detected! Please wait for medical staff.")
            if model:
                res = model.generate_content(f"Uri BJ Nano v8 AI. Patient: {u['name']}, BP: {u['bp']}, Temp: {u['temp']}. Subiza mu Kinyarwanda: {prompt}")
                st.write(res.text)
                if "MITI:" in res.text.upper(): u["prescription"] = "Prescribed"
            else: st.error("Muganga AI ntari hafi...")

# =========================
# PAGE: LAB / PHARMA (Security Applied)
# =========================
elif st.session_state.current_page in ["🧪 LAB", "💊 PHARMA"]:
    role = "lab" if "LAB" in st.session_state.current_page else "phar"
    pw = st.text_input(f"{st.session_state.current_page} Password", type="password")
    if st.button("LOGIN"):
        if pw == st.session_state.passwords[role]:
            st.session_state[f"{role}_auth"] = True; play_sound("success")
        else:
            st.session_state.login_attempts += 1; play_sound("error")
            if st.session_state.login_attempts >= 3: st.session_state.system_shutdown = True; st.rerun()
            st.error(f"Error! {st.session_state.login_attempts}/3")
    
    if st.session_state.get(f"{role}_auth"):
        st.success("Access Granted")
        # Lab/Pharma logic here...

# =========================
# PAGE: ADMIN
# =========================
elif st.session_state.current_page == "⚙️ ADMIN":
    pw = st.text_input("Admin Password", type="password")
    if st.button("ADMIN LOGIN"):
        if pw == st.session_state.passwords["admin"]: st.session_state.admin_auth = True
        else: play_sound("error"); st.error("Denied")
    
    if st.session_state.get("admin_auth"):
        st.subheader("Settings")
        st.session_state.hospital_name = st.text_input("Hospital Name", st.session_state.hospital_name)
        new_admin_pw = st.text_input("New Admin Password", type="password")
        if st.button("SAVE SETTINGS"):
            if new_admin_pw: st.session_state.passwords["admin"] = new_admin_pw
            st.success("Updated!")
        if st.button("SYSTEM REBOOT"): st.session_state.system_shutdown = True; st.rerun()

st.markdown(f"<div style='position:fixed;bottom:10px;right:20px;font-size:12px;color:#00d4ff;'>{st.session_state.hospital_name} | {kigali_time} 🇷🇼</div>", unsafe_allow_html=True)
