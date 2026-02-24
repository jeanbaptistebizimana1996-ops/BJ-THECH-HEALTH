import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz
import time
import pandas as pd
import random

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="BJ TECH MEDICAL NANO OS v6.0", layout="wide")

KIGALI_TZ = pytz.timezone("Africa/Kigali")

# ===============================
# SESSION INIT
# ===============================
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
        "admin": "admin.2026",
        "lab": "lab.2026",
        "phar": "phar.2026",
    }

if "reboot_key" not in st.session_state:
    st.session_state.reboot_key = "reboot.v6.2026"

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "shutdown" not in st.session_state:
    st.session_state.shutdown = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "HOME"

# ===============================
# AI CONFIG
# ===============================
AI_AVAILABLE = True
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    AI_AVAILABLE = False

# ===============================
# STYLE
# ===============================
st.markdown("""
<style>
header {visibility:hidden;}
footer {visibility:hidden;}

.stApp {
background: linear-gradient(135deg,#e0f7ff,#ffffff);
}

.stethoscope {
font-size:70px;
text-align:center;
}

.ai-light {
width:60px;
height:60px;
border-radius:50%;
margin:auto;
animation:spin 3s linear infinite;
background: conic-gradient(red,orange,yellow,green,blue,indigo,violet,red);
}

@keyframes spin {
100% {transform: rotate(360deg);}
}

.shutdown {
background:red;
color:white;
position:fixed;
top:0;left:0;
height:100vh;width:100vw;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
z-index:9999;
font-size:30px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# AUTO SHUTDOWN
# ===============================
if st.session_state.shutdown:
    st.markdown("""
    <div class="shutdown">
    🚨 SYSTEM SHUTDOWN ACTIVE 🚨<br>
    Unauthorized Access Detected
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input("Enter Reboot Key", type="password")
    if st.button("REBOOT SYSTEM"):
        if key == st.session_state.reboot_key:
            st.session_state.shutdown = False
            st.session_state.login_attempts = 0
            st.rerun()
        else:
            st.error("Wrong Reboot Key")
    st.stop()

# ===============================
# HEADER
# ===============================
st.markdown("<div class='stethoscope'>🩺</div>", unsafe_allow_html=True)

now = datetime.now(KIGALI_TZ).strftime("%H:%M:%S")
st.markdown(f"<h2 style='text-align:center;color:#0077b6;'>KIGALI LOCAL TIME: {now}</h2>", unsafe_allow_html=True)

if AI_AVAILABLE:
    st.markdown("<div class='ai-light'></div>", unsafe_allow_html=True)

st.divider()

# ===============================
# NAVIGATION
# ===============================
c1, c2, c3, c4 = st.columns(4)

if c1.button("HOME"):
    st.session_state.current_page = "HOME"
if c2.button("LAB"):
    st.session_state.current_page = "LAB"
if c3.button("PHARMACY"):
    st.session_state.current_page = "PHARMACY"
if c4.button("ADMIN"):
    st.session_state.current_page = "ADMIN"

st.divider()

# ===============================
# HOME
# ===============================
if st.session_state.current_page == "HOME":
    st.title("Patient AI Diagnostics")

    phone = st.text_input("Phone")
    name = st.text_input("Full Name")

    if st.button("REGISTER"):
        uid = phone[-6:]
        st.session_state.db[uid] = {
            "izina": name,
            "phone": phone,
            "results": "",
            "meds": "",
            "status": "New",
            "bp": "N/A",
            "temp": "N/A",
        }
        st.success("Registered")

# ===============================
# LAB
# ===============================
elif st.session_state.current_page == "LAB":

    pw = st.text_input("Lab Password", type="password")
    if st.button("LOGIN LAB"):
        if pw == st.session_state.passwords["lab"]:
            st.success("Access Granted")
        else:
            st.session_state.login_attempts += 1
            if st.session_state.login_attempts >= 3:
                st.session_state.shutdown = True
                st.rerun()
            st.error("Wrong Password")

# ===============================
# PHARMACY
# ===============================
elif st.session_state.current_page == "PHARMACY":

    pw = st.text_input("Pharmacy Password", type="password")
    if st.button("LOGIN PHARMACY"):
        if pw == st.session_state.passwords["phar"]:
            st.success("Access Granted")
        else:
            st.session_state.login_attempts += 1
            if st.session_state.login_attempts >= 3:
                st.session_state.shutdown = True
                st.rerun()
            st.error("Wrong Password")

# ===============================
# ADMIN ADVANCED CONTROLLER
# ===============================
elif st.session_state.current_page == "ADMIN":

    pw = st.text_input("Admin Password", type="password")

    if st.button("LOGIN ADMIN"):
        if pw == st.session_state.passwords["admin"]:
            st.success("Admin Access Granted")

            st.subheader("Change ALL Passwords")
            new_admin = st.text_input("New Admin Password")
            new_lab = st.text_input("New Lab Password")
            new_phar = st.text_input("New Pharmacy Password")
            new_reboot = st.text_input("New Reboot Key")

            if st.button("UPDATE SETTINGS"):
                if new_admin: st.session_state.passwords["admin"] = new_admin
                if new_lab: st.session_state.passwords["lab"] = new_lab
                if new_phar: st.session_state.passwords["phar"] = new_phar
                if new_reboot: st.session_state.reboot_key = new_reboot
                st.success("All Settings Updated")

            st.divider()
            st.subheader("Full Database")
            st.write(pd.DataFrame.from_dict(st.session_state.db, orient="index"))

            if st.button("SYSTEM RESET"):
                st.session_state.db = {}
                st.success("System Reset Complete")

        else:
            st.session_state.login_attempts += 1
            if st.session_state.login_attempts >= 3:
                st.session_state.shutdown = True
                st.rerun()
            st.error("Wrong Admin Password")

# ===============================
# FOOTER
# ===============================
st.markdown("<div style='position:fixed;bottom:10px;right:20px;font-size:12px;color:#0077b6;font-weight:bold;'>BJ TECH MEDICAL NANO OS v6.0 | ULTRA SECURE</div>", unsafe_allow_html=True)
