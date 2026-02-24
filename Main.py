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

# CSS for Biometric Background, Scrolling Text, and Animations
st.markdown(\"\"\"
<style>
    header {visibility:hidden;}
    footer {visibility:hidden;}
    
    .stApp {
        background: radial-gradient(circle at center, rgba(10,10,10,0.9) 0%, rgba(26,26,26,0.95) 100%), 
                    url("https://img.icons8.com/ios-filled/500/00d4ff/fingerprint.png");
        background-repeat: no-repeat;
        background-position: center;
        background-size: 600px;
        background-attachment: fixed;
        background-blend-mode: overlay;
        color: #e0e0e0;
    }

    .scrolling-text {
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
    }

    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .stethoscope {
        font-size: 70px;
        text-align: center;
        animation: pulse 1.5s infinite;
        color: #00d4ff;
        margin-bottom: -10px;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 0.8; }
    }

    .ai-indicator {
        width: 12px;
        height: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #00ff00;
        animation: blink 2s infinite;
    }

    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
</style>

<div class="scrolling-text">
    BJ Nano v8 Health Rwanda | Biometric Fingerprint System | European Hospital Standard | V8 Engine Active
</div>
\"\"\", unsafe_allow_html=True)

# 4. CYBER SECURITY
if st.session_state.system_shutdown:
    st.markdown("<div style='background:#d00000;color:white;height:100vh;width:100vw;position:fixed;top:0;left:0;z-index:9999;display:flex;flex-direction:column;justify-content:center;align-items:center;'><h1>🚨 SYSTEM LOCKED 🚨</h1><p>Security Breach Detected</p></div>", unsafe_allow_html=True)
    reboot = st.text_input("Enter Reboot Key:", type="password")
    if st.button("REBOOT"):
        if reboot == REBOOT_KEY:
            st.session_state.system_shutdown = False
            st.session_state.login_attempts = 0
            st.rerun()
    st.stop()

# 5. HEADER (KIGALI TIME & STETHOSCOPE)
kigali_tz = pytz.timezone('Africa/Kigali')
kigali_time = datetime.now(kigali_tz).strftime("%H:%M:%S")

st.markdown("<div class='stethoscope'>🩺</div>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center;color:#00d4ff;margin-top:0;'>{kigali_time}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'><span class='ai-indicator'></span> AI Available (Gemini 2.5)</p>", unsafe_allow_html=True)

# 6. NAVIGATION
st.divider()
c1, c2, c3, c4 = st.columns(4)
pages = [("🏠 HOME", "🏠"), ("🧪 LAB", "🧪"), ("💊 PHARMA", "💊"), ("⚙️ ADMIN", "⚙️")]
for i, (p, icon) in enumerate(pages):
    if [c1, c2, c3, c4][i].button(f"{icon} {p}", use_container_width=True):
        st.session_state.current_page = p
        st.rerun()
st.divider()

# =========================
# PAGE: HOME (REGISTRATION & SCAN)
# =========================
if st.session_state.current_page == "🏠 HOME":
    st.subheader("📱 Patient Registration & Biometric Scan")
    
    tab1, tab2 = st.tabs(["New Patient (Register)", "Existing Patient (Scan Fingerprint)"])
    
    with tab1:
        with st.form("Register"):
            name = st.text_input("Full Name (Amazina yombi)")
            phone = st.text_input("Phone Number")
            if st.form_submit_button("REGISTER & SCAN FINGERPRINT"):
                fid = f"FP-{random.randint(1000, 9999)}"
                st.session_state.db[fid] = {
                    "name": name, "phone": phone, "bp": "N/A", "temp": "N/A",
                    "ai_tests": [], "lab_results": [], "prescription": [], "status": "Registered",
                    "timestamp": datetime.now(kigali_tz).strftime("%Y-%m-%d %H:%M:%S")
                }
                st.success(f"Registered! Your Fingerprint ID: {fid}")
                st.session_state.current_user_id = fid
                
    with tab2:
        scan_id = st.text_input("Place Finger on Scanner (Enter Fingerprint ID)")
        if st.button("SCAN FINGERPRINT"):
            if scan_id in st.session_state.db:
                st.session_state.current_user_id = scan_id
                st.success(f"Fingerprint Verified: {st.session_state.db[scan_id]['name']}")
            else:
                st.error("Fingerprint not recognized!")

    if st.session_state.current_user_id:
        user = st.session_state.db[st.session_state.current_user_id]
        st.info(f"Active Patient: {user['name']} | ID: {st.session_state.current_user_id}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🩺 SCAN BLOOD PRESSURE"):
                user["bp"] = f"{random.randint(110,140)}/{random.randint(70,90)} mmHg"
                st.write(f"BP: {user['bp']}")
        with col2:
            if st.button("🌡️ SCAN TEMPERATURE"):
                user["temp"] = f"{random.uniform(36.5,38.5):.1f} °C"
                st.write(f"Temp: {user['temp']}")

        st.markdown("---")
        query = st.chat_input("Baza AI Muganga...")
        if query:
            if model:
                try:
                    sys_msg = f"Uritwa BJ Nano v8 Health AI. Patient: {user['name']}, BP: {user['bp']}, Temp: {user['temp']}. Tanga inama n'ibizamini byo gupimwa (Lab tests) n'imiti (Prescription) niba bikenewe. Subiza mu Kinyarwanda."
                    response = model.generate_content(f"{sys_msg}\\n\\nUser: {query}")
                    res_text = response.text
                    st.write(res_text)
                    
                    if "LAB:" in res_text.upper():
                        tests = [t.strip() for t in res_text.upper().split("LAB:")[1].split("\\n")[0].split(",")]
                        user["ai_tests"] = tests
                    if "MITI:" in res_text.upper() or "PRESCRIPTION:" in res_text.upper():
                        key = "MITI:" if "MITI:" in res_text.upper() else "PRESCRIPTION:"
                        meds = res_text.upper().split(key)[1].split("\\n")[0]
                        user["prescription"] = meds
                except Exception:
                    st.error("Muraho neza Muganga Ai ntarihafi jya mucyumba cyisuzumiro bagufashe")
            else:
                st.error("Muraho neza Muganga Ai ntarihafi jya mucyumba cyisuzumiro bagufashe")

# =========================
# PAGE: LAB (TESTING)
# =========================
elif st.session_state.current_page == "🧪 LAB":
    st.subheader("🧪 Laboratory (Biometric Access)")
    pw = st.text_input("Lab Password", type="password")
    if st.button("LOGIN LAB"):
        if pw == st.session_state.passwords["lab"]:
            st.session_state.lab_auth = True
        else: st.error("Wrong Password")

    if st.session_state.get("lab_auth"):
        st.success("Lab Access Granted")
        target_fid = st.text_input("Scan Patient Fingerprint (ID)")
        if target_fid in st.session_state.db:
            p = st.session_state.db[target_fid]
            st.write(f"**Patient:** {p['name']} | **Tests Requested by AI:** {', '.join(p['ai_tests']) if p['ai_tests'] else 'None'}")
            
            results = st.multiselect("Select Lab Results (Confirmed Diseases):", 
                                    ["Malaria", "Typhoid", "Flu", "Infection", "Diabetes", "Normal"])
            if st.button("SUBMIT RESULTS"):
                p["lab_results"] = results
                p["status"] = "Tested"
                st.success("Results saved to Fingerprint ID!")
        elif target_fid:
            st.error("Fingerprint not found!")

# =========================
# PAGE: PHARMA (MEDICINE)
# =========================
elif st.session_state.current_page == "💊 PHARMA":
    st.subheader("💊 Pharmacy (Biometric Access)")
    pw = st.text_input("Pharmacy Password", type="password")
    if st.button("LOGIN PHARMACY"):
        if pw == st.session_state.passwords["phar"]:
            st.session_state.phar_auth = True
        else: st.error("Wrong Password")

    if st.session_state.get("phar_auth"):
        st.success("Pharmacy Access Granted")
        target_fid = st.text_input("Scan Patient Fingerprint (ID)")
        if target_fid in st.session_state.db:
            p = st.session_state.db[target_fid]
            st.write(f"**Patient:** {p['name']}")
            st.write(f"**Lab Results:** {', '.join(p['lab_results'])}")
            st.write(f"**AI Prescription:** {p['prescription'] if p['prescription'] else 'No prescription yet'}")
            
            if st.button("APPROVE & DISPENSE"):
                p["status"] = "Treated"
                st.balloons()
                st.success(f"Fingerprint ID {target_fid} has been treated successfully!")
        elif target_fid:
            st.error("Fingerprint not found!")

# =========================
# PAGE: ADMIN (SETTINGS)
# =========================
elif st.session_state.current_page == "⚙️ ADMIN":
    st.subheader("⚙️ System Administration")
    pw = st.text_input("Admin Password", type="password")
    if st.button("LOGIN ADMIN"):
        if pw == st.session_state.passwords["admin"]:
            st.session_state.admin_auth = True
        else: st.error("Wrong Password")

    if st.session_state.get("admin_auth"):
        st.success("Admin Panel Active")
        
        with st.expander("Change Passwords"):
            new_admin = st.text_input("New Admin PW")
            new_lab = st.text_input("New Lab PW")
            new_phar = st.text_input("New Pharma PW")
            if st.button("UPDATE PASSWORDS"):
                if new_admin: st.session_state.passwords["admin"] = new_admin
                if new_lab: st.session_state.passwords["lab"] = new_lab
                if new_phar: st.session_state.passwords["phar"] = new_phar
                st.success("Passwords updated!")

        with st.expander("System Logs & Data"):
            df = pd.DataFrame.from_dict(st.session_state.db, orient="index")
            st.dataframe(df)
            csv = df.to_csv().encode('utf-8')
            st.download_button("DOWNLOAD SYSTEM DATA (CSV)", csv, "bj_nano_v8_data.csv", "text/csv")

        if st.button("FORCE SYSTEM REBOOT"):
            st.session_state.system_shutdown = True
            st.rerun()

# FOOTER
st.markdown(f"<div style='position:fixed;bottom:10px;right:20px;font-size:12px;color:#00d4ff;'>BJ Nano v8 Health Rwanda | {kigali_time} 🇷🇼</div>", unsafe_allow_html=True)
