font-size:30px;
z-index:9999;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOCKDOWN MODE
# ===============================
if st.session_state.locked:
    st.markdown("""
    <div class="locked-screen">
    🚨 HOSPITAL import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import pandas as pd
import random

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
    st.session_state.current_page = "🏠 Home"

# SECURITY KEYS
REBOOT_KEY = "ndaharimysystem2026"

# 2. AI CONFIGURATION
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    st.error("AI Configuration Error.")

# 3. UI STYLE
st.set_page_config(page_title="BJ TECH Medical Nano-OS v5.0", layout="wide")

st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
    background: radial-gradient(circle at center, #f0f9ff 0%, #e0f2fe 100%);
    background-image: url("https://img.icons8.com/ios-filled/500/0077b6/fingerprint.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 400px;
    background-attachment: fixed;
    background-blend-mode: soft-light;
}

@keyframes heartbeat {
    0% { transform: scale(1); }
    20% { transform: scale(1.3); }
    40% { transform: scale(1); }
    60% { transform: scale(1.3); }
    80% { transform: scale(1); }
    100% { transform: scale(1); }
}

.heart-beat {
    color:#2ecc71;
    font-size:60px;
    text-align:center;
    animation: heartbeat 1.2s infinite;
}

.shutdown-screen {
    background-color:#d00000;
    color:white;
    height:100vh;
    width:100vw;
    position:fixed;
    top:0;
    left:0;
    z-index:9999;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
}
</style>
""", unsafe_allow_html=True)

# 4. CYBER SECURITY AUTO SHUTDOWN
if st.session_state.system_shutdown:
    st.markdown("""
    <div class="shutdown-screen">
        <h1>🚨 SYSTEM AUTO SHUTDOWN 🚨</h1>
        <h2 style="color:black;background:white;padding:10px;">
        SOMEONE TRYING TO HACK
        </h2>
        <p>Security Breach Detected. System is locked.</p>
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

# 5. HEADER
st.markdown("<div class='heart-beat'>💚</div>", unsafe_allow_html=True)
st.markdown(
    f"<h3 style='text-align:center;color:#0077b6;'>"
    f"{datetime.now().strftime('%H:%M:%S')}<br>"
    f"BJ TECH PROFESSIONAL AI MEDICAL OS"
    f"</h3>",
    unsafe_allow_html=True,
)

st.divider()

# 6. NAVIGATION
c1, c2, c3, c4 = st.columns(4)

if c1.button("🏠 HOME"):
    st.session_state.current_page = "🏠 Home"
    st.rerun()

if c2.button("🧪 LAB"):
    st.session_state.current_page = "🧪 Lab"
    st.rerun()

if c3.button("💊 PHARMA"):
    st.session_state.current_page = "💊 Pharmacy"
    st.rerun()

if c4.button("⚙️ ADMIN"):
    st.session_state.current_page = "⚙️ Admin"
    st.rerun()

st.divider()

# =========================
# PAGE: HOME
# =========================
if st.session_state.current_page == "🏠 Home":

    if not st.session_state.current_user:
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

        st.success(f"Muraho {curr['izina']} | Status: {curr['status']}")

        if st.button("SCAN BLOOD PRESSURE"):
            time.sleep(1)
            curr["bp"] = f"{random.randint(110,140)}/{random.randint(70,90)} mmHg"
            st.success(f"BP: {curr['bp']}")

        if st.button("SCAN TEMPERATURE"):
            time.sleep(1)
            curr["temp"] = f"{random.uniform(36.5,39.5):.1f} °C"
            st.success(f"Temp: {curr['temp']}")

        prompt = st.chat_input("Baza AI Muganga...")
        if prompt:
            with st.chat_message("assistant"):
                response = model.generate_content(
                    f"You are medical AI. Patient temp {curr['temp']} BP {curr['bp']}. "
                    f"Answer in Kinyarwanda: {prompt}"
                ).text
                st.write(response)

# =========================
# PAGE: LAB
# =========================
elif st.session_state.current_page == "🧪 Lab":

    pw = st.text_input("Lab Password", type="password")

    if st.button("LOGIN LAB"):
        if pw == st.session_state.passwords["lab"]:
            st.success("Lab Access Granted")
        else:
            st.session_state.login_attempts += 1
            st.error("Wrong Password")

# =========================
# PAGE: PHARMACY
# =========================
elif st.session_state.current_page == "💊 Pharmacy":

    pw = st.text_input("Pharmacy Password", type="password")

    if st.button("LOGIN PHARMACY"):
        if pw == st.session_state.passwords["phar"]:
            st.success("Pharmacy Access Granted")
        else:
            st.error("Wrong Password")

# =========================
# PAGE: ADMIN
# =========================
elif st.session_state.current_page == "⚙️ Admin":

    pw = st.text_input("Admin Password", type="password")

    if st.button("LOGIN ADMIN"):
        if pw == st.session_state.passwords["admin"]:
            st.success("Admin Access Granted")
            st.write(pd.DataFrame.from_dict(st.session_state.db, orient="index"))
        else:
            st.error("Wrong Password")

# FOOTER
st.markdown(
    "<div style='position:fixed;bottom:10px;right:20px;"
    "font-size:12px;color:#0077b6;font-weight:bold;'>"
    "BJ TECH AI MEDICAL OS v5.0 | SECURE 🛡️"
    "</div>",
    unsafe_allow_html=True,
) LOCKED 🚨<br>
    Security Breach Detected
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input("ENTER REBOOT KEY", type="password")
    if st.button("REBOOT SERVER"):
        if key == st.session_state.reboot_key:
            st.session_state.locked = False
            st.session_state.attempts = 0
            st.rerun()
        else:
            st.error("INVALID REBOOT KEY")
    st.stop()

# ===============================
# HEADER
# ===============================
st.title("🩺 BJ TECH REAL HOSPITAL OS v7.0")

now = datetime.now(KIGALI).strftime("%H:%M:%S")
st.markdown(f"### 🕒 Kigali Time: {now}")

if AI_ONLINE:
    st.markdown("<div class='ai-ring'></div>", unsafe_allow_html=True)
    st.success("AI SERVER ONLINE")
else:
    st.error("AI OFFLINE")

st.divider()

# ===============================
# NAVIGATION
# ===============================
c1,c2,c3,c4 = st.columns(4)
if c1.button("HOME"): st.session_state.page="HOME"
if c2.button("LAB"): st.session_state.page="LAB"
if c3.button("PHARMACY"): st.session_state.page="PHARMACY"
if c4.button("ADMIN"): st.session_state.page="ADMIN"

st.divider()

# ===============================
# HOME – PATIENT MONITOR
# ===============================
if st.session_state.page=="HOME":
    st.subheader("Patient Registration & Monitoring")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")

    if st.button("REGISTER PATIENT"):
        pid = phone[-6:]
        st.session_state.patients[pid] = {
            "Name": name,
            "BP": "N/A",
            "Temp": "N/A",
            "Status": "New"
        }
        st.success("Patient Registered Successfully")

    if st.session_state.patients:
        st.write(pd.DataFrame.from_dict(st.session_state.patients, orient="index"))

    st.divider()
    st.subheader("🖐 Fingerprint Biometric Scan")

    if st.button("SCAN PATIENT"):
        with st.spinner("Scanning Fingerprint..."):
            time.sleep(2)
            st.audio("https://www.soundjay.com/buttons/sounds/beep-07.mp3")
            bp = f"{random.randint(110,140)}/{random.randint(70,90)}"
            temp = f"{random.uniform(36.5,39.5):.1f}"
            st.success(f"BP: {bp} | Temp: {temp}")

# ===============================
# LAB
# ===============================
elif st.session_state.page=="LAB":
    pw = st.text_input("Lab Password", type="password")
    if st.button("LOGIN"):
        if pw==st.session_state.passwords["lab"]:
            st.success("Lab Access Granted")
        else:
            st.session_state.attempts+=1
            if st.session_state.attempts>=3:
                st.session_state.locked=True
                st.rerun()
            st.error("Wrong Password")

# ===============================
# PHARMACY
# ===============================
elif st.session_state.page=="PHARMACY":
    pw = st.text_input("Pharmacy Password", type="password")
    if st.button("LOGIN"):
        if pw==st.session_state.passwords["pharmacy"]:
            st.success("Pharmacy Access Granted")
        else:
            st.session_state.attempts+=1
            if st.session_state.attempts>=3:
                st.session_state.locked=True
                st.rerun()
            st.error("Wrong Password")

# ===============================
# ADMIN SERVER CONTROL
# ===============================
elif st.session_state.page=="ADMIN":
    pw = st.text_input("Admin Password", type="password")
    if st.button("LOGIN"):
        if pw==st.session_state.passwords["admin"]:
            st.success("ADMIN SERVER ACCESS GRANTED")

            st.subheader("Server Settings")

            new_admin = st.text_input("New Admin Password")
            new_lab = st.text_input("New Lab Password")
            new_phar = st.text_input("New Pharmacy Password")
            new_reboot = st.text_input("New Reboot Key")

            if st.button("UPDATE SERVER SETTINGS"):
                if new_admin: st.session_state.passwords["admin"]=new_admin
                if new_lab: st.session_state.passwords["lab"]=new_lab
                if new_phar: st.session_state.passwords["pharmacy"]=new_phar
                if new_reboot: st.session_state.reboot_key=new_reboot
                st.success("Server Updated Successfully")

            st.divider()
            st.write("LIVE DATABASE")
            st.write(pd.DataFrame.from_dict(st.session_state.patients, orient="index"))

        else:
            st.session_state.attempts+=1
            if st.session_state.attempts>=3:
                st.session_state.locked=True
                st.rerun()
            st.error("Wrong Admin Password")

st.markdown("---")
st.caption("BJ TECH REAL HOSPITAL SERVER OS v7.0 | ULTRA SECURE")
