import streamlit as st
from datetime import datetime
import pytz
import random
import pandas as pd
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="BJ TECH HEALTH OS V8", layout="wide")
KIGALI = pytz.timezone("Africa/Kigali")

# =========================
# SESSION INIT
# =========================
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False

if "page" not in st.session_state:
    st.session_state.page = "HOME"

# =========================
# DARK MEDICAL BLUE THEME
# =========================
st.markdown("""
<style>
header, footer {visibility:hidden;}

.stApp {
background-color:#071a2f;
color:#ffffff;
}

.cyber-title {
font-size:48px;
font-weight:bold;
text-align:center;
color:#00c3ff;
text-shadow:0 0 25px #00c3ff;
animation: moveText 4s infinite alternate;
}

@keyframes moveText {
0%{letter-spacing:2px;}
100%{letter-spacing:8px;}
}

.medical-box {
background-color:#0d2a4a;
padding:20px;
border-radius:15px;
box-shadow:0 0 15px #008cff;
text-align:center;
font-size:18px;
font-weight:bold;
color:#00c3ff;
}

.stButton>button {
background-color:#003366;
color:#00c3ff;
border-radius:12px;
height:70px;
font-size:16px;
font-weight:bold;
}

.locked {
background:black;
color:red;
position:fixed;
top:0;left:0;
width:100vw;height:100vh;
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
font-size:28px;
z-index:9999;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOCKDOWN MODE
# =========================
if st.session_state.locked:
    st.markdown("""
    <div class="locked">
    🚨 SYSTEM LOCKED 🚨<br>
    Unauthorized Access
    </div>
    """, unsafe_allow_html=True)

    key = st.text_input("ENTER MASTER KEY", type="password")
    if st.button("REBOOT SYSTEM"):
        if key == "V8MASTER":
            st.session_state.locked = False
            st.session_state.attempts = 0
            st.rerun()
        else:
            st.error("INVALID KEY")
    st.stop()

# =========================
# HEADER
# =========================
st.markdown("<div class='cyber-title'>BJ TECH HEALTH OS V8</div>", unsafe_allow_html=True)

now = datetime.now(KIGALI).strftime("%H:%M:%S")
st.markdown(f"<h4 style='text-align:center;color:#00c3ff;'>KIGALI TIME: {now}</h4>", unsafe_allow_html=True)

st.divider()

# =========================
# HOME SCREEN (APP STYLE)
# =========================
if st.session_state.page == "HOME":

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🩺 PATIENTS"):
            st.session_state.page = "PATIENTS"

    with col2:
        if st.button("🧪 LAB"):
            st.session_state.page = "LAB"

    with col3:
        if st.button("💊 PHARMACY"):
            st.session_state.page = "PHARMACY"

    with col4:
        if st.button("⚙️ ADMIN"):
            st.session_state.page = "ADMIN"

# =========================
# LIVE MONITORING (NO PLOTLY)
# =========================
elif st.session_state.page == "PATIENTS":

    st.subheader("📊 LIVE HEART MONITOR")

    data = pd.DataFrame({
        "BPM": [random.randint(60,100) for _ in range(30)]
    })

    st.line_chart(data)

    if st.button("BACK"):
        st.session_state.page = "HOME"

# =========================
# LAB LOGIN
# =========================
elif st.session_state.page == "LAB":
    pw = st.text_input("LAB PASSWORD", type="password")
    if st.button("LOGIN"):
        if pw == "labV8":
            st.success("LAB ACCESS GRANTED")
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.locked = True
                st.rerun()
            st.error("WRONG PASSWORD")

# =========================
# PHARMACY LOGIN
# =========================
elif st.session_state.page == "PHARMACY":
    pw = st.text_input("PHARMACY PASSWORD", type="password")
    if st.button("LOGIN"):
        if pw == "pharV8":
            st.success("PHARMACY ACCESS GRANTED")
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.locked = True
                st.rerun()
            st.error("WRONG PASSWORD")

# =========================
# ADMIN LOGIN
# =========================
elif st.session_state.page == "ADMIN":
    pw = st.text_input("ADMIN PASSWORD", type="password")
    if st.button("LOGIN"):
        if pw == "adminV8":
            st.success("ADMIN ACCESS GRANTED")
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 3:
                st.session_state.locked = True
                st.rerun()
            st.error("WRONG PASSWORD")

st.markdown("---")
st.caption("BJ TECH HEALTH OS V8 ULTRA | DARK MEDICAL BLUE EDITION")
