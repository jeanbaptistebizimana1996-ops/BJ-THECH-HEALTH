import streamlit as st
from datetime import datetime
import time
import pandas as pd
import random
import pytz

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {}

if "passwords" not in st.session_state:
    st.session_state.passwords = {
        "admin": "cyuma.thec.2026",
        "lab": "lab.2026",
        "phar": "phar.2026",
    }

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
REBOOT_KEY = "ndaharimysystem2026"

# 2. AI CONFIGURATION
try:
    import google.generativeai as genai
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        model = None
except Exception:
    model = None

# 3. UI STYLE & CONFIGURATION
st.set_page_config(page_title="BJ Nano v8 Health Rwanda", layout="wide")

def play_sound(sound_type):
    urls = {
        "error": "https://www.soundjay.com/buttons/beep-05.mp3",
        "success": "https://www.soundjay.com/buttons/button-3.mp3",
        "shutdown": "https://www.soundjay.com/communication/alarm-clock-elapsed-01.mp3"
    }
    st.markdown(f'<audio autoplay><source src="{urls[sound_type]}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# Dynamic Background
bg_color = "rgba(10,10,10,0.9)"
if st.session_state.scan_status == "scanning":
    bg_color = "rgba(255, 0, 0, 0.4)" 
elif st.session_state.scan_status == "success":
    bg_color = "rgba(0, 255, 0, 0.4)"

st.markdown(f"""
<style>
    header {{ visibility:hidden; }}
    footer {{ visibility:hidden; }}
    
    .stApp {{
        background: radial-gradient(circle at center, {bg_color} 0%, rgba(26,26,26,0.95) 100%), 
                    url("https://img.icons8.com/ios-filled/500/00d4ff/fingerprint.png");
        background-repeat: no-repeat;
        background-position: center;
        background-size: 600px;
        background-attachment: fixed;
        background-blend-mode: overlay;
        color: #e0e0e0;
        transition: background 0.5s ease;
    }}

    .scrolling-text {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        animation: scroll 20s linear infinite;
        font-size: 22px;
        font-weight: bold;
        color: #00d4ff;
        padding: 10px 0;
        border-bottom: 1px solid #00d4ff;
    }}

    @keyframes scroll {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}

    .stethoscope {{
        font-size: 70px;
        text-align: center;
        animation: pulse 1.5s infinite;
        color: #00d4ff;
    }}

    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.8; }}
        50% {{ transform: scale(1.1); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.8; }}
    }}

    .ai-online-led {{
        width: 12px;
        height: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 10px #00ff00;
        animation: blink-led 1.5s infinite;
        margin-right: 8px;
    }}

    @keyframes blink-led {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
        100% {{ opacity: 1; }}
    }}
</style>

<div class="scrolling-text">
    BJ Nano v8 Health Rwanda | Biometric Fingerprint System | V8 Engine Active | European Hospital Standard
</div>
""", unsafe_allow_html=True)

# 4. CYBER SECURITY AUTO SHUTDOWN
if st.session_state.system_shutdown:
    play_sound("shutdown")
    st.markdown("<div style='background:#d00000;color:white;height:100vh;width:100vw;position:fixed;top:0;left:0;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;'><h1>🚨 SYSTEM AUTO SHUTDOWN 🚨</h1><h2 style='background:white;color:red;padding:10px;'>CYBER ATTACK DETECTED</h2><p>System is locked for security. Enter Developer Reboot Key.</p></div>", unsafe_allow_html=True)
    reboot = st.text_input("Enter Reboot Key:", type="password")
    if st.button("REBOOT SYSTEM"):
        if reboot == REBOOT_KEY:
            st.session_state.system_shutdown = False
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.error("Invalid Key!")
    st.stop()

# 5. HEADER
kigali_tz = pytz.timezone('Africa/Kigali')
kigali_time = datetime.now(kigali_tz).strftime("%H:%M:%S")
st.markdown("<div class='stethoscope'>🩺</div>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;color:#00d4ff;margin-top:0;'>{kigali_time}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'><span class='ai-online-led'></span>AI Gemini 2.5 is Online</p>", unsafe_allow_html=True)

# 6. NAVIGATION
st.divider()
c1, c2, c3, c4 = st.columns(4)
pages = [("🏠 HOME", "🏠"), ("🧪 LAB", "🧪"), ("💊 PHARMA", "💊"), ("⚙️ ADMIN", "⚙️")]
for i, (p, icon) in enumerate(pages):
    if [c1, c2, c3, c4][i].button(f"{icon} {p}", use_container_width=True):
        st.session_state.current_page = p
        st.session_state.scan_status = "idle"
        st.rerun()
st.divider()

# =========================
# PAGE: HOME
# =========================
if st.session_state.current_page == "🏠 HOME":
    st.subheader("📱 Patient Biometric Registration")
    tab1, tab2 = st.tabs(["Register New Patient", "Scan Fingerprint"])
    
    with tab1:
        with st.form("Register"):
            name = st.text_input("Full Name")
            phone = st.text_input("Phone Number")
            if st.form_submit_button("REGISTER & SCAN"):
                st.session_state.scan_status = "scanning"
                time.sleep(1)
                fid = f"FP-{random.randint(1000, 9999)}"
                st.session_state.db[fid] = {
                    "name": name, "phone": phone, "bp": "N/A", "temp": "N/A",
                    "ai_tests": [], "lab_results": [], "prescription": "", "status": "New"
                }
                st.session_state.scan_status = "success"
                play_sound("success")
                st.success(f"✅ Correct! ID: {fid}")
                st.session_state.current_user_id = fid
                st.rerun()
                
    with tab2:
        scan_id = st.text_input("Scan Fingerprint (Enter ID)")
        if st.button("VERIFY"):
            st.session_state.scan_status = "scanning"
            time.sleep(1)
            if scan_id in st.session_state.db:
                st.session_state.scan_status = "success"
                play_sound("success")
                st.session_state.current_user_id = scan_id
                st.success(f"✅ Correct! Welcome {st.session_state.db[scan_id]['name']}")
                st.rerun()
            else:
                st.session_state.scan_status = "idle"
                play_sound("error")
                st.error("Fingerprint not recognized!")

    if st.session_state.current_user_id:
        user = st.session_state.db[st.session_state.current_user_id]
        st.info(f"Active Patient: {user['name']} | Status: {user['status']}")
        if st.button("🩺 SCAN VITALS (BP & TEMP)"):
            user["bp"] = f"{random.randint(110,140)}/{random.randint(70,90)} mmHg"
            user["temp"] = f"{random.uniform(36.5,38.5):.1f} °C"
            st.write(f"BP: {user['bp']} | Temp: {user['temp']}")

        query = st.chat_input("Baza AI Muganga...")
        if query:
            if model:
                try:
                    res = model.generate_content(f"Uritwa BJ Nano v8 AI. Patient: {user['name']}, BP: {user['bp']}, Temp: {user['temp']}. Subiza mu Kinyarwanda: {query}")
                    st.write(res.text)
                    if "LAB:" in res.text.upper(): user["ai_tests"] = ["Blood Test", "Malaria Scan"]
                    if "MITI:" in res.text.upper(): user["prescription"] = "Paracetamol, Vitamins"
                except Exception:
                    st.error("Muraho neza Muganga Ai ntarihafi jya mucyumba cyisuzumiro bagufashe")
            else:
                st.error("Muraho neza Muganga Ai ntarihafi jya mucyumba cyisuzumiro bagufashe")

# =========================
# PAGE: LAB
# =========================
elif st.session_state.current_page == "🧪 LAB":
    pw = st.text_input("Lab Password", type="password")
    if st.button("LOGIN LAB"):
        if pw == st.session_state.passwords["lab"]:
            st.session_state.lab_auth = True
            play_sound("success")
        else:
            st.session_state.login_attempts += 1
            play_sound("error")
            if st.session_state.login_attempts >= 3:
                st.session_state.system_shutdown = True
                st.rerun()
            st.error(f"Wrong Password! Attempts: {st.session_state.login_attempts}/3")

    if st.session_state.get("lab_auth"):
        target = st.text_input("Scan Patient Fingerprint (ID)")
        if st.button("FETCH LAB ORDERS"):
            if target in st.session_state.db:
                p = st.session_state.db[target]
                st.write(f"Patient: {p['name']} | Tests: {p['ai_tests']}")
                results = st.multiselect("Select Results:", ["Positive", "Negative", "Normal"])
                if st.button("SAVE RESULTS"):
                    p["lab_results"] = results
                    p["status"] = "Tested"
                    st.success("Results Saved!")
            else: st.error("Fingerprint not found!")

# =========================
# PAGE: PHARMA
# =========================
elif st.session_state.current_page == "💊 PHARMA":
    pw = st.text_input("Pharmacy Password", type="password")
    if st.button("LOGIN PHARMA"):
        if pw == st.session_state.passwords["phar"]:
            st.session_state.phar_auth = True
            play_sound("success")
        else:
            st.session_state.login_attempts += 1
            play_sound("error")
            if st.session_state.login_attempts >= 3:
                st.session_state.system_shutdown = True
                st.rerun()
            st.error("Wrong Password!")

    if st.session_state.get("phar_auth"):
        target = st.text_input("Scan Patient Fingerprint for Medicine")
        if target in st.session_state.db:
            p = st.session_state.db[target]
            st.write(f"Patient: {p['name']} | Prescription: {p['prescription']}")
            if st.button("APPROVE & DISPENSE"):
                p["status"] = "Treated"
                st.balloons()
                st.success("Medicine Dispensed Successfully!")
        elif target: st.error("Invalid Fingerprint ID")

# =========================
# PAGE: ADMIN
# =========================
elif st.session_state.current_page == "⚙️ ADMIN":
    pw = st.text_input("Admin Password", type="password")
    if st.button("LOGIN ADMIN"):
        if pw == st.session_state.passwords["admin"]:
            st.session_state.admin_auth = True
        else:
            play_sound("error")
            st.error("Access Denied")

    if st.session_state.get("admin_auth"):
        st.subheader("System Administration Panel")
        if st.button("FORCE REBOOT"):
            st.session_state.system_shutdown = True
            st.rerun()
        df = pd.DataFrame.from_dict(st.session_state.db, orient="index")
        st.dataframe(df)
        st.download_button("Download Data (CSV)", df.to_csv(), "system_data.csv")

st.markdown(f"<div style='position:fixed;bottom:10px;right:20px;font-size:12px;color:#00d4ff;'>BJ Nano v8 Health Rwanda | {kigali_time} 🇷🇼</div>", unsafe_allow_html=True)
