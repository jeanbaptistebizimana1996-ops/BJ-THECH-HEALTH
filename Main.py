import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz
import time
import pandas as pd
import random

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(page_title="BJ TECH HOSPITAL OS v7.0", layout="wide")

KIGALI = pytz.timezone("Africa/Kigali")

# ===============================
# SESSION INIT
# ===============================
if "patients" not in st.session_state:
    st.session_state.patients = {}

if "passwords" not in st.session_state:
    st.session_state.passwords = {
        "admin": "admin.v7",
        "lab": "lab.v7",
        "pharmacy": "phar.v7"
    }

if "reboot_key" not in st.session_state:
    st.session_state.reboot_key = "reboot.v7"

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False

if "page" not in st.session_state:
    st.session_state.page = "HOME"

# ===============================
# AI CONFIG
# ===============================
AI_ONLINE = True
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except:
    AI_ONLINE = False

# ===============================
# STYLE
# ===============================
st.markdown("""
<style>
header, footer {visibility:hidden;}

.stApp {
background: linear-gradient(135deg,#dff6ff,#ffffff);
}

.ai-ring {
width:70px;height:70px;border-radius:50%;
margin:auto;
background:conic-gradient(red,orange,yellow,green,blue,violet,red);
animation:spin 3s linear infinite;
}

@keyframes spin {100%{transform:rotate(360deg);}}

.locked-screen{
background:black;color:red;
position:fixed;top:0;left:0;
width:100vw;height:100vh;
display:flex;justify-content:center;
align-items:center;
flex-direction:column;
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
    🚨 HOSPITAL SERVER LOCKED 🚨<br>
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
