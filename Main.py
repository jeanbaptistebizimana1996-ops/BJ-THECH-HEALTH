import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz
import time
import pandas as pd
import random
import plotly.graph_objects as go

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="BJ TECH HEALTH OS V8", layout="wide")
KIGALI = pytz.timezone("Africa/Kigali")

# ===============================
# SESSION INIT
# ===============================
if "patients" not in st.session_state:
    st.session_state.patients = {}

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False

if "page" not in st.session_state:
    st.session_state.page = "HOME"

# ===============================
# DARK CYBER STYLE
# ===============================
st.markdown("""
<style>
header, footer {visibility:hidden;}
.stApp {background-color:#0a0f1f;color:white;}

.cyber-title {
font-size:45px;
font-weight:bold;
text-align:center;
color:#00bfff;
animation: glowMove 4s linear infinite;
text-shadow:0 0 20px #00bfff;
}

@keyframes glowMove {
0%{transform:translateX(-10px);}
50%{transform:translateX(10px);}
100%{transform:translateX(-10px);}
}

.app-button button{
background:linear-gradient(145deg,#001f3f,#003366);
color:#00d9ff;
height:120px;
border-radius:20px;
font-size:18px;
font-weight:bold;
box-shadow:0 0 15px #00bfff;
}

.ai-ring {
width:60px;height:60px;
border-radius:50%;
margin:auto;
background:conic-gradient(#00bfff,#0044ff,#00bfff);
animation:spin 2s linear infinite;
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
# LOCKDOWN
# ===============================
if st.session_state.locked:
    st.markdown("""
    <div class="locked-screen">
    🚨 CYBER HOSPITAL SERVER LOCKED 🚨
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

# ===============================
# HEADER
# ===============================
st.markdown("<div class='cyber-title'>BJ TECH HEALTH OS V8</div>", unsafe_allow_html=True)

now = datetime.now(KIGALI).strftime("%H:%M:%S")
st.markdown(f"<h4 style='text-align:center;color:#00bfff;'>KIGALI TIME: {now}</h4>", unsafe_allow_html=True)

st.markdown("<div class='ai-ring'></div>", unsafe_allow_html=True)
st.divider()

# ===============================
# HOME – APP STYLE ICONS
# ===============================
if st.session_state.page == "HOME":

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown("<div class='app-button'>", unsafe_allow_html=True)
        if st.button("🩺 PATIENTS"):
            st.session_state.page="PATIENTS"
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='app-button'>", unsafe_allow_html=True)
        if st.button("🧪 LAB"):
            st.session_state.page="LAB"
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='app-button'>", unsafe_allow_html=True)
        if st.button("💊 PHARMACY"):
            st.session_state.page="PHARMACY"
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown("<div class='app-button'>", unsafe_allow_html=True)
        if st.button("⚙️ ADMIN"):
            st.session_state.page="ADMIN"
        st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# LIVE MONITORING DASHBOARD
# ===============================
elif st.session_state.page == "PATIENTS":

    st.subheader("📊 LIVE PATIENT MONITORING")

    x = list(range(20))
    y = [random.randint(60,100) for _ in x]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines'))
    fig.update_layout(template="plotly_dark",
                      title="Heart Rate Monitor (BPM)",
                      xaxis_title="Time",
                      yaxis_title="BPM")

    st.plotly_chart(fig, use_container_width=True)

    if st.button("BACK"):
        st.session_state.page="HOME"

# ===============================
# LAB LOGIN
# ===============================
elif st.session_state.page=="LAB":
    pw = st.text_input("LAB PASSWORD", type="password")
    if st.button("LOGIN"):
        if pw=="labV8":
            st.success("LAB ACCESS GRANTED")
        else:
            st.session_state.attempts+=1
            if st.session_state.attempts>=3:
                st.session_state.locked=True
                st.rerun()
            st.error("WRONG PASSWORD")

# ===============================
# PHARMACY LOGIN
# ===============================
elif st.session_state.page=="PHARMACY":
    pw = st.text_input("PHARMACY PASSWORD", type="password")
    if st.button("LOGIN"):
        if pw=="pharV8":
            st.success("PHARMACY ACCESS GRANTED")
        else:
            st.session_state.attempts+=1
            if st.session_state.attempts>=3:
                st.session_state.locked=True
                st.rerun()
            st.error("WRONG PASSWORD")

# ===============================
# ADMIN
# ===============================
elif st.session_state.page=="ADMIN":
    pw = st.text_input("ADMIN PASSWORD", type="password")
    if st.button("LOGIN"):
        if pw=="adminV8":
            st.success("ADMIN ACCESS GRANTED")
            st.write("SERVER CONTROL PANEL ACTIVE")
        else:
            st.session_state.attempts+=1
            if st.session_state.attempts>=3:
                st.session_state.locked=True
                st.rerun()
            st.error("WRONG PASSWORD")

st.markdown("---")
st.caption("BJ TECH HEALTH OS V8 ULTRA | CYBER DARK HOSPITAL EDITION")
