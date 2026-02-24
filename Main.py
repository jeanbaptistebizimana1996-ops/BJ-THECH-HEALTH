import streamlit as st
from datetime import datetime
import time
import pandas as pd
import random
from openai import OpenAI

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {
        "119958": {
            "izina": "Habineza",
            "phone": "0788000000",
            "results": "",
            "meds": "",
            "status": "New",
            "bp": "N/A",
            "temp": "N/A",
        }
    }

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

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 HOME"

# SECURITY KEYS
REBOOT_KEY = "ndaharimysystem2026"

# 2. AI CONFIGURATION (GEMINI 2.5 FLASH)
client = OpenAI()

# 3. UI STYLE & CONFIGURATION
st.set_page_config(page_title="BJ Nano v8 Health Rwanda", layout="wide")

# CSS for App Icons, Scrolling Text, and AI Indicator
st.markdown("""
<style>
    header {visibility:hidden;}
    footer {visibility:hidden;}
    
    .stApp {
        background: radial-gradient(circle at center, #0a0a0a 0%, #1a1a1a 100%);
        color: #e0e0e0;
    }

    /* Scrolling Name */
    .scrolling-text {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        animation: scroll 15s linear infinite;
        font-size: 24px;
        font-weight: bold;
        color: #00d4ff;
        padding: 10px 0;
    }

    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Stethoscope Animation */
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }
    
    .stethoscope {
        font-size: 60px;
        text-align: center;
        animation: pulse 1.5s infinite;
        color: #00d4ff;
    }

    /* AI Status Indicator */
    .ai-indicator {
        width: 15px;
        height: 15px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
        box-shadow: 0 0 10px #00ff00;
        animation: blink 2s infinite;
    }

    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.3; }
        100% { opacity: 1; }
    }

    /* Prevent Sleeping Mode */
    .no-sleep {
        display: none;
    }
</style>

<div class="scrolling-text">
    BJ Nano v8 Health Rwanda | Advanced AI Medical System | Professional Healthcare Solutions | V8 Speed Active
</div>
""", unsafe_allow_html=True)

# 4. CYBER SECURITY AUTO SHUTDOWN
if st.session_state.system_shutdown:
    st.markdown("""
    <div style="background-color:#d00000; color:white; height:100vh; width:100vw; position:fixed; top:0; left:0; z-index:9999; display:flex; flex-direction:column; justify-content:center; align-items:center;">
        <h1>🚨 SYSTEM AUTO SHUTDOWN 🚨</h1>
        <h2 style="color:black;background:white;padding:10px;">SECURITY BREACH DETECTED</h2>
        <p>System is locked due to unauthorized access attempts.</p>
    </div>
    """, unsafe_allow_html=True)

    reboot = st.text_input("Enter Developer Reboot Key:", type="password")
    if st.button("REBOOT SYSTEM"):
        if reboot == REBOOT_KEY:
            st.session_state.system_shutdown = False
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.error("Invalid Reboot Key!")
    st.stop()

# 5. HEADER WITH STETHOSCOPE & LOCAL TIME
st.markdown("<div class='stethoscope'>🩺</div>", unsafe_allow_html=True)

# Local Time Updated
now = datetime.now().strftime("%H:%M:%S")
st.markdown(
    f"<h3 style='text-align:center;color:#00d4ff;'>"
    f"🕒 Local Time: {now}<br>"
    f"<span style='font-size: 14px; color: #00ff00;'><div class='ai-indicator'></div> AI Available (Gemini 2.5)</span>"
    f"</h3>",
    unsafe_allow_html=True,
)

st.divider()

# 6. NAVIGATION (APP SCREEN STYLE)
cols = st.columns(4)
nav_items = [
    ("🏠 HOME", "🏠"),
    ("🧪 LAB", "🧪"),
    ("💊 PHARMA", "💊"),
    ("⚙️ ADMIN", "⚙️")
]

for i, (label, icon) in enumerate(nav_items):
    if cols[i].button(f"{icon} {label}", use_container_width=True):
        st.session_state.current_page = label
        st.rerun()

st.divider()

# =========================
# PAGE: HOME
# =========================
if st.session_state.current_page == "🏠 HOME":
    if not st.session_state.current_user:
        st.markdown("### 📱 Login to System")
        with st.form("Login"):
            phone = st.text_input("Nimero ya Foni")
            name = st.text_input("Amazina yombi")
            if st.form_submit_button("EMEZA"):
                uid = phone[-6:]
                if uid not in st.session_state.db:
                    st.session_state.db[uid] = {
                        "izina": name,
                        "phone": phone,
                        "results": "",
                        "meds": "",
                        "status": "New",
                        "bp": "N/A",
                        "temp": "N/A",
                    }
                st.session_state.current_user = uid
                st.rerun()
    else:
        curr = st.session_state.db[st.session_state.current_user]
        st.success(f"Muraho {curr['izina']} | System Speed: V8 ⚡")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🩺 SCAN BLOOD PRESSURE", use_container_width=True):
                with st.spinner("Scanning..."):
                    time.sleep(0.5)
                    curr["bp"] = f"{random.randint(110,140)}/{random.randint(70,90)} mmHg"
                    st.info(f"BP: {curr['bp']}")
        with c2:
            if st.button("🌡️ SCAN TEMPERATURE", use_container_width=True):
                with st.spinner("Scanning..."):
                    time.sleep(0.5)
                    curr["temp"] = f"{random.uniform(36.5,39.5):.1f} °C"
                    st.info(f"Temp: {curr['temp']}")

        st.markdown("---")
        prompt = st.chat_input("Baza AI Muganga (Gemini 2.5)...")
        if prompt:
            with st.chat_message("assistant"):
                try:
                    # System prompt for European Hospital standard
                    sys_prompt = f"Uritwa BJ Nano v8 Health AI. Ukora nk'ibitaro bikomeye byo mu Burayi. Patient data: Temp {curr['temp']}, BP {curr['bp']}. Subiza mu Kinyarwanda neza kandi kinyamwuga."
                    response = client.chat.completions.create(
                        model="gpt-4.1-mini",
                        messages=[
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.write(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")

# =========================
# PAGE: LAB
# =========================
elif st.session_state.current_page == "🧪 LAB":
    st.markdown("### 🧪 Laboratory Access")
    pw = st.text_input("Lab Password", type="password")
    if st.button("LOGIN LAB"):
        if pw == st.session_state.passwords["lab"]:
            st.success("Lab Access Granted - V8 Speed Active")
        else:
            st.session_state.login_attempts += 1
            if st.session_state.login_attempts >= 3:
                st.session_state.system_shutdown = True
                st.rerun()
            st.error("Wrong Password")

# =========================
# PAGE: PHARMA
# =========================
elif st.session_state.current_page == "💊 PHARMA":
    st.markdown("### 💊 Pharmacy Management")
    pw = st.text_input("Pharmacy Password", type="password")
    if st.button("LOGIN PHARMACY"):
        if pw == st.session_state.passwords["phar"]:
            st.success("Pharmacy Access Granted")
        else:
            st.error("Wrong Password")

# =========================
# PAGE: ADMIN
# =========================
elif st.session_state.current_page == "⚙️ ADMIN":
    st.markdown("### ⚙️ System Administration")
    pw = st.text_input("Admin Password", type="password")
    if st.button("LOGIN ADMIN"):
        if pw == st.session_state.passwords["admin"]:
            st.success("Admin Access Granted")
            st.dataframe(pd.DataFrame.from_dict(st.session_state.db, orient="index"))
        else:
            st.error("Wrong Password")

# FOOTER
st.markdown(
    "<div style='position:fixed;bottom:10px;right:20px;font-size:12px;color:#00d4ff;font-weight:bold;'>"
    "BJ Nano v8 Health Rwanda | Professional European Standard 🇪🇺"
    "</div>",
    unsafe_allow_html=True,
)
