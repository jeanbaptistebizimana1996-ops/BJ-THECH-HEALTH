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

# Function to play sounds
def play_sound(sound_type):
    urls = {
        "error": "https://www.soundjay.com/buttons/beep-05.mp3",
        "success": "https://www.soundjay.com/buttons/button-3.mp3",
        "shutdown": "https://www.soundjay.com/communication/alarm-clock-elapsed-01.mp3"
    }
    st.markdown(f'<audio autoplay><source src="{urls[sound_type]}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# Dynamic Background Color based on Scan Status
bg_color = "rgba(10,10,10,0.9)"
if st.session_state.scan_status == "scanning":
    bg_color = "rgba(255, 0, 0, 0.4)" 
elif st.session_state.scan_status == "success":
    bg_color = "rgba(0, 255, 0, 0.4)"

# KOSORA: Hano nakoresheje {{ }} kugira ngo f-string itazamo error
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
</style>

<div class="scrolling-text">
    BJ Nano v8 Health Rwanda | Biometric Fingerprint System | V8 Engine | Professional European Standard
</div>
""", unsafe_allow_html=True)

# 4. CYBER SECURITY
if st.session_state.system_shutdown:
    play_sound("shutdown")
    st.markdown("<div style='background:#d00000;color:white;height:100vh;width:100vw;position:fixed;top:0;left:0;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;'><h1>🚨 SYSTEM AUTO SHUTDOWN 🚨</h1><p>Security Breach Detected</p></div>", unsafe_allow_html=True)
    reboot = st.text_input("Enter Reboot Key:", type="password")
    if st.button("REBOOT"):
        if reboot == REBOOT_KEY:
            st.session_state.system_shutdown = False
            st.rerun()
    st.stop()

# 5. HEADER
kigali_tz = pytz.timezone('Africa/Kigali')
kigali_time = datetime.now(kigali_tz).strftime("%H:%M:%S")
st.markdown("<div class='stethoscope'>🩺</div>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;color:#00d4ff;margin-top:0;'>{kigali_time}</h2>", unsafe_allow_html=True)

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
    st.subheader("📱 Patient Biometric Access")
    
    tab1, tab2 = st.tabs(["New Registration", "Fingerprint Scan"])
    
    with tab1:
        with st.form("Register"):
            name = st.text_input("Full Name")
            phone = st.text_input("Phone")
            if st.form_submit_button("REGISTER & SCAN"):
                st.session_state.scan_status = "scanning"
                # Simulating scan time
                time.sleep(1)
                fid = f"FP-{random.randint(1000, 9999)}"
                st.session_state.db[fid] = {
                    "name": name, "phone": phone, "bp": "N/A", "temp": "N/A",
                    "ai_tests": [], "lab_results": [], "prescription": "", "status": "Registered"
                }
                st.session_state.scan_status = "success"
                play_sound("success")
                st.success(f"✅ Correct! Fingerprint ID: {fid}")
                st.session_state.current_user_id = fid
                st.rerun()
                
    with tab2:
        scan_id = st.text_input("Enter ID to simulate Fingerprint Scan")
        if st.button("SCAN NOW"):
            st.session_state.scan_status = "scanning"
            time.sleep(1)
            if scan_id in st.session_state.db:
                st.session_state.scan_status = "success"
                play_sound("success")
                st.session_state.current_user_id = scan_id
                st.success(f"✅ Correct! Verified: {st.session_state.db[scan_id]['name']}")
                st.rerun()
            else:
                st.session_state.scan_status = "idle"
                play_sound("error")
                st.error("Fingerprint not recognized!")

    if st.session_state.current_user_id:
        user = st.session_state.db[st.session_state.current_user_id]
        st.info(f"Patient: {user['name']} | Status: {user['status']}")
        
        if st.button("🩺 SCAN BP & TEMP"):
            user["bp"] = f"{random.randint(110,140)}/{random.randint(70,90)} mmHg"
            user["temp"] = f"{random.uniform(36.5,38.5):.1f} °C"
            st.write(f"BP: {user['bp']} | Temp: {user['temp']}")

        query = st.chat_input("Baza AI Muganga...")
        if query:
            if model:
                try:
                    res = model.generate_content(f"Uritwa BJ Nano v8 AI. Patient: {user['name']}, BP: {user['bp']}, Temp: {user['temp']}. Subiza mu Kinyarwanda: {query}")
                    st.write(res.text)
                    if "LAB:" in res.text.upper(): user["ai_tests"] = ["General Scan"]
                    if "MITI:" in res.text.upper(): user["prescription"] = "AI Prescribed"
                except Exception:
                    st.error("Muraho neza Muganga Ai ntarihafi jya mucyumba cyisuzumiro bagufashe")
            else:
                st.error("Muraho neza Muganga Ai ntarihafi jya mucyumba cyisuzumiro bagufashe")

# =========================
# PAGE: LAB
# =========================
elif st.session_state.current_page == "🧪 LAB":
    pw = st.text_input("Lab Password", type="password")
    if st.button("LOGIN"):
        if pw == st.session_state.passwords["lab"]:
            st.session_state.lab_auth = True
            play_sound("success")
        else:
            play_sound("error")
            st.error("Wrong Password")

    if st.session_state.get("lab_auth"):
        target = st.text_input("Scan Patient ID")
        if st.button("VERIFY FINGERPRINT"):
            st.session_state.scan_status = "scanning"
            time.sleep(1)
            if target in st.session_state.db:
                st.session_state.scan_status = "success"
                play_sound("success")
                p = st.session_state.db[target]
                st.write(f"Patient: {p['name']}")
                results = st.multiselect("Results:", ["Malaria", "Typhoid", "Normal"])
                if st.button("SAVE"):
                    p["lab_results"] = results
                    st.success("✅ Saved!")
            else:
                play_sound("error")
                st.error("Not Found")

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
        st.subheader("System Control")
        if st.button("REBOOT SYSTEM"):
            st.session_state.system_shutdown = True
            st.rerun()
        df = pd.DataFrame.from_dict(st.session_state.db, orient="index")
        st.dataframe(df)
        st.download_button("Download Logs", df.to_csv(), "logs.csv")

st.markdown(f"<div style='position:fixed;bottom:10px;right:20px;font-size:12px;color:#00d4ff;'>BJ Nano v8 Health Rwanda | {kigali_time} 🇷🇼</div>", unsafe_allow_html=True)
