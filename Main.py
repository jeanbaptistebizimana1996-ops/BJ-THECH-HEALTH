import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time
import re

# 1. INITIALIZE SYSTEM STATE
if "db" not in st.session_state:
    st.session_state.db = {"119958": {"izina": "Habineza", "phone": "0788000000", "results": "", "meds": "", "emergency": ""}}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "last_activity" not in st.session_state:
    st.session_state.last_activity = time.time()
if "system_locked" not in st.session_state:
    st.session_state.system_locked = False

# SECURITY KEYS
MASTER_RECOVERY_KEY = "ndihanomysystem"
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

# 4. AUTO-LOGOUT LOGIC (3 MINUTES)
timeout = 180
if time.time() - st.session_state.last_activity > timeout:
    st.session_state.current_user = None
    st.session_state.messages = []
    st.session_state.last_activity = time.time()

# 5. UI STYLE (TRANSPARENT & CLEAN)
st.set_page_config(page_title="BJ TECH Medical OS", layout="wide")
st.markdown("""
<style>
    header {visibility: hidden;} footer {visibility: hidden;}
    .stApp {
        background-image: url("https://img.icons8.com/ios-filled/500/1a5fb4/fingerprint.png");
        background-repeat: no-repeat; background-position: center; background-size: 200px;
        background-color: #f4f7f6; background-blend-mode: overlay;
    }
    /* Transparent Forms */
    [data-testid="stForm"], .stTabs, .stTab, [data-testid="stExpander"] {
        background-color: transparent !important; border: none !important; box-shadow: none !important;
    }
    /* Mobile Keyboard Optimization */
    .stTextInput input { font-size: 16px !important; }
    .icon-only { font-size: 70px; text-align: center; color: #1a5fb4; margin-bottom: 5px; }
    .emergency-btn { background-color: #ff0000 !important; color: white !important; font-weight: bold; }
    .hacker-alert { background-color: black; color: red; padding: 40px; text-align: center; border: 5px solid red; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
</style>
""", unsafe_allow_html=True)

# 6. CYBER-SECURITY LOCKDOWN
if st.session_state.system_locked:
    st.markdown('<div class="hacker-alert">🚨 SECURITY BREACH! SYSTEM LOCKED</div>', unsafe_allow_html=True)
    unlock = st.text_input("Admin Unlock Key:", type="password")
    if unlock == MASTER_RECOVERY_KEY:
        st.session_state.system_locked = False
        st.rerun()
    st.stop()

# 7. SIDEBAR
with st.sidebar:
    st.markdown(f"### 🕒 {datetime.now().strftime('%H:%M:%S')}")
    role = st.radio("GATEWAY:", ["🏠 Kiosk (Patient)", "🧪 Laboratory", "⚙️ Admin"])

# --- PAGE: KIOSK (PATIENT) ---
if role == "🏠 Kiosk (Patient)":
    st.markdown("<div class='icon-only'>🛡️</div>", unsafe_allow_html=True)
    
    if not st.session_state.current_user:
        with st.form("Login"):
            p_phone = st.text_input("Andika Nimero ya Foni (Registration):", placeholder="078...")
            p_name = st.text_input("Amazina yombi (First time):")
            if st.form_submit_button("INJIRA / REGISTER"):
                if check_for_hacking(p_phone) or check_for_hacking(p_name):
                    st.session_state.system_locked = True
                    st.rerun()
                new_id = p_phone[-6:] if p_phone else "000000"
                if new_id not in st.session_state.db:
                    st.session_state.db[new_id] = {"izina": p_name, "phone": p_phone, "results": "", "meds": ""}
                st.session_state.current_user = new_id
                update_activity()
                st.rerun()
    else:
        curr = st.session_state.db[st.session_state.current_user]
        st.success(f"Verified: {curr['izina']}")
        
        # EMERGENCY BUTTONS
        col1, col2, col3 = st.columns(3)
        if col1.button("🩸 AMARASO"): curr["emergency"] = "BLEEDING"; update_activity()
        if col2.button("🤰 INDA"): curr["emergency"] = "PREGNANCY"; update_activity()
        if col3.button("🤢 IZINDI"): curr["emergency"] = "CRITICAL"; update_activity()

        # HIGH-SPEED AI CHAT
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if prompt := st.chat_input("Baza AI...", on_submit=update_activity):
            if check_for_hacking(prompt):
                st.session_state.system_locked = True
                st.rerun()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res_placeholder = st.empty()
                full_res = ""
                response_stream = model.generate_content(f"Advice {curr['izina']} in Kinyarwanda: {prompt}", stream=True)
                for chunk in response_stream:
                    full_res += chunk.text
                    res_placeholder.markdown(full_res + "▌")
                res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

# --- PAGE: LABORATORY (MULTIPLE CHOICE) ---
elif role == "🧪 Laboratory":
    st.markdown("<div class='icon-only'>🧪</div>", unsafe_allow_html=True)
    lab_id = st.selectbox("Hitamo Umurwayi:", list(st.session_state.db.keys()))
    if lab_id:
        p = st.session_state.db[lab_id]
        st.write(f"Umurwayi: {p['izina']}")
        tests = st.multiselect("Indwara basanze (Multiple):", ["Malaria", "Typhoid", "Amoeba", "Infection", "Flu"])
        if st.button("BOHEREZA SMS (AI)"):
            all_t = ", ".join(tests)
            p["results"] = all_t
            ai_sms = model.generate_content(f"Andika SMS ya Kinyarwanda kuri {p['izina']} urwaye {all_t}. Mubwire imiti n'inama.").text
            p["meds"] = ai_sms
            st.success("SMS na Lab Results byoherejwe!")
            st.info(f"AI SMS: {ai_sms}")

st.markdown("<div style='position:fixed; bottom:10px; left:20px; font-size:10px; color:#1a5fb4;'>BJ TECH CYBER-SHIELD ACTIVE</div>", unsafe_allow_html=True)
