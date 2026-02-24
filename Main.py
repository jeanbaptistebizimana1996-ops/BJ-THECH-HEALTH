import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import pandas as pd
import io

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {
        "119958": {"izina": "Habineza", "phone": "0788000000", "results": "Malaria", "meds": "Fata Coartem", "emergency": ""},
        "223344": {"izina": "Mugisha", "phone": "0781111111", "results": "Typhoid", "meds": "Fata Cipro", "emergency": ""}
    }
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()
if "system_locked" not in st.session_state:
    st.session_state.system_locked = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# SECURITY KEYS
MASTER_RECOVERY_KEY = "ndihanomysystem"
LAB_PASSWORD = "lab123"
ADMIN_PASSWORD = "admin123"
HACK_KEYWORDS = ["DROP", "DELETE", "SELECT *", "<script>", "OR 1=1", "UNION ALL"]

# 2. HIGH-SPEED AI CONFIGURATION
try:
    api_key = st.secrets.get("GEMINI_API_KEY", "AIzaSyDUxyCei7WEpFar85ShrHV5I6f7Lmzo0Oo")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("AI Configuration Error.")

# 3. SECURITY & UTILITY FUNCTIONS
def check_for_hacking(user_input):
    if not user_input: return False
    for word in HACK_KEYWORDS:
        if word.upper() in user_input.upper(): return True
    return False

def update_activity():
    st.session_state.last_activity = time.time()

# 4. UI STYLE (MEDICAL NANO-TECH THEME)
st.set_page_config(page_title="BJ TECH Medical Nano-OS", layout="wide")

st.markdown("""
<style>
    header {visibility: hidden;} footer {visibility: hidden;}
    
    .stApp {
        background: radial-gradient(circle at center, #f0f9ff 0%, #e0f2fe 100%);
        background-image: url("https://img.icons8.com/ios-filled/500/0077b6/fingerprint.png");
        background-repeat: no-repeat; 
        background-position: center; 
        background-size: 400px;
        background-attachment: fixed;
        background-blend-mode: soft-light;
    }
    
    [data-testid="stForm"], .stTabs, .stTab, [data-testid="stExpander"], .stChatMessage, .glass-card {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        padding: 25px !important;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: bold !important;
        height: 60px;
        width: 100%;
        transition: all 0.3s ease;
        font-size: 18px !important;
    }
    .stButton>button:hover {
        background-color: #0096c7 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 119, 182, 0.3);
    }
    
    .large-clock {
        font-size: 80px;
        font-weight: bold;
        color: #0077b6;
        text-align: center;
        margin-bottom: 10px;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 15px rgba(0, 119, 182, 0.3);
    }
    
    .hacker-alert { 
        background-color: #1a1a1a; 
        color: #ff4b4b; 
        padding: 50px; 
        text-align: center; 
        border: 10px solid #ff4b4b; 
        border-radius: 20px;
        animation: blinker 0.8s linear infinite; 
    }
    @keyframes blinker { 50% { opacity: 0.3; } }
</style>
""", unsafe_allow_html=True)

# 5. CYBER-SECURITY LOCKDOWN
if st.session_state.system_locked:
    st.markdown('<div class="hacker-alert">🚨 SECURITY BREACH! SYSTEM LOCKED</div>', unsafe_allow_html=True)
    unlock = st.text_input("Fungura Sisitemu (Admin Key):", type="password")
    if st.button("EMEZA"):
        if unlock == MASTER_RECOVERY_KEY:
            st.session_state.system_locked = False
            st.rerun()
    st.stop()

# 6. HEADER & CLOCK
st.markdown(f"<div class='large-clock'>{datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#0077b6; margin-top:-20px;'>BJ TECH MEDICAL NANO-OS</h3>", unsafe_allow_html=True)

# 7. NAVIGATION ICONS (ON SCREEN)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏠 HOME\n(Patient Access)", key="nav_home"):
        st.session_state.current_page = "🏠 Home"
        st.rerun()

with col2:
    if st.button("🧪 LAB\n(Staff Only)", key="nav_lab"):
        st.session_state.current_page = "🧪 Lab"
        st.rerun()

with col3:
    if st.button("⚙️ ADMIN\n(Management)", key="nav_admin"):
        st.session_state.current_page = "⚙️ Admin"
        st.rerun()

st.divider()

# --- PAGE: HOME (PATIENT) ---
if st.session_state.current_page == "🏠 Home":
    st.markdown("<h2 style='text-align:center; color:#0077b6;'>Patient Kiosk</h2>", unsafe_allow_html=True)
    
    if not st.session_state.current_user:
        with st.form("Login"):
            st.subheader("Kwinjira / Kwiyandikisha")
            p_phone = st.text_input("Nimero ya Foni:", placeholder="078...")
            p_name = st.text_input("Amazina yombi:")
            if st.form_submit_button("EMEZA KWINJIRA"):
                if not p_phone or not p_name:
                    st.warning("Uzuza neza imyirondoro yawe!")
                elif check_for_hacking(p_phone) or check_for_hacking(p_name):
                    st.session_state.system_locked = True
                    st.rerun()
                else:
                    new_id = p_phone[-6:]
                    if new_id not in st.session_state.db:
                        st.session_state.db[new_id] = {"izina": p_name, "phone": p_phone, "results": "", "meds": ""}
                    st.session_state.current_user = new_id
                    st.success("Winjijwe neza!")
                    st.rerun()
    else:
        curr = st.session_state.db[st.session_state.current_user]
        st.markdown(f"<div class='glass-card'><h3>Muraho, {curr['izina']}!</h3>", unsafe_allow_html=True)
        if st.button("SOHOKA (LOGOUT)"):
            st.session_state.current_user = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        # EMERGENCY
        st.subheader("Ubufasha bwihuse (Emergency)")
        ec1, ec2, ec3 = st.columns(3)
        if ec1.button("🩸 AMARASO"): st.error("Ubufasha buraje!"); update_activity()
        if ec2.button("🤰 INDA"): st.error("Ubufasha buraje!"); update_activity()
        if ec3.button("🤢 IZINDI"): st.error("Ubufasha buraje!"); update_activity()

        # AI CHAT
        st.subheader("Baza AI Muganga (Medical AI)")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if prompt := st.chat_input("Andika hano..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res = model.generate_content(f"Advice {curr['izina']} in Kinyarwanda: {prompt}").text
                st.write(res)
                st.session_state.messages.append({"role": "assistant", "content": res})

# --- PAGE: LAB (PASSWORD PROTECTED) ---
elif st.session_state.current_page == "🧪 Lab":
    st.markdown("<h2 style='text-align:center; color:#0077b6;'>Laboratory Portal 🧪</h2>", unsafe_allow_html=True)
    
    if "lab_auth" not in st.session_state: st.session_state.lab_auth = False
    
    if not st.session_state.lab_auth:
        with st.form("LabAuth"):
            st.info("Injiza ijambo ry'ibanga rya Lab kugira ngo ukomeze.")
            pw = st.text_input("Password:", type="password")
            if st.form_submit_button("EMEZA KWINJIRA"):
                if pw == LAB_PASSWORD:
                    st.session_state.lab_auth = True
                    st.rerun()
                else:
                    st.error("Ijambo ry'ibanga si ryo!")
    else:
        if st.button("Funga Lab (Logout)"):
            st.session_state.lab_auth = False
            st.rerun()
            
        lab_id = st.selectbox("Hitamo Umurwayi:", list(st.session_state.db.keys()))
        if lab_id:
            p = st.session_state.db[lab_id]
            st.info(f"Umurwayi: **{p['izina']}**")
            tests = st.multiselect("Indwara basanze:", ["Malaria", "Typhoid", "Amoeba", "Infection", "Flu", "UTI", "Diabetes"])
            if st.button("EMEZA NO KOHEREZA SMS (AI)"):
                if not tests:
                    st.warning("Hitamo nibura indwara imwe!")
                else:
                    all_t = ", ".join(tests)
                    p["results"] = all_t
                    ai_sms = model.generate_content(f"Andika SMS ya Kinyarwanda kuri {p['izina']} urwaye {all_t}. Mubwire imiti n'inama.").text
                    p["meds"] = ai_sms
                    st.success("Ibipimo na SMS byoherejwe!")
                    st.info(f"AI SMS: {ai_sms}")

# --- PAGE: ADMIN (PASSWORD PROTECTED) ---
elif st.session_state.current_page == "⚙️ Admin":
    st.markdown("<h2 style='text-align:center; color:#0077b6;'>Admin Dashboard ⚙️</h2>", unsafe_allow_html=True)
    
    if "admin_auth" not in st.session_state: st.session_state.admin_auth = False
    
    if not st.session_state.admin_auth:
        with st.form("AdminAuth"):
            st.info("Injiza ijambo ry'ibanga rya Admin kugira ngo ukomeze.")
            pw = st.text_input("Password:", type="password")
            if st.form_submit_button("EMEZA KWINJIRA"):
                if pw == ADMIN_PASSWORD:
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.error("Ijambo ry'ibanga si ryo!")
    else:
        if st.button("Funga Admin (Logout)"):
            st.session_state.admin_auth = False
            st.rerun()
            
        st.subheader("Amakuru y'Abarwayi Bose")
        df = pd.DataFrame.from_dict(st.session_state.db, orient='index')
        st.dataframe(df, use_container_width=True)
        
        # DOWNLOAD SECTION
        st.subheader("Manura Ama-Documents (Downloads)")
        col_d1, col_d2 = st.columns(2)
        
        with col_d1:
            csv = df.to_csv().encode('utf-8')
            st.download_button(
                label="📥 MANURA RAPORO (CSV)",
                data=csv,
                file_name=f'BJ_TECH_Report_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
            )
        
        with col_d2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=True, sheet_name='Abarwayi')
            processed_data = output.getvalue()
            st.download_button(
                label="📥 MANURA RAPORO (EXCEL)",
                data=processed_data,
                file_name=f'BJ_TECH_Report_{datetime.now().strftime("%Y%m%d")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        st.divider()
        st.subheader("System Control")
        if st.button("RESET SYSTEM DATA", type="secondary"):
            st.session_state.db = {}
            st.warning("Amakuru yose asibwe!")
            st.rerun()

# --- FOOTER ---
st.markdown("<div style='position:fixed; bottom:10px; right:20px; font-size:12px; color:#0077b6; font-weight:bold;'>BJ TECH MEDICAL NANO-OS v3.0 | SECURE 🛡️</div>", unsafe_allow_html=True)
