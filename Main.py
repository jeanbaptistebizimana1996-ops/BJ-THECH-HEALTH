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
    # Use the user's key or a default if available
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

# 5. UI STYLE (MEDICAL NANO-TECH THEME)
st.set_page_config(page_title="BJ TECH Medical Nano-OS", layout="wide")

# Custom CSS for Medical/Nano-Tech Look
st.markdown("""
<style>
    header {visibility: hidden;} footer {visibility: hidden;}
    
    /* Background with Fingerprint and Medical Colors */
    .stApp {
        background: radial-gradient(circle at center, #f0f9ff 0%, #e0f2fe 100%);
        background-image: url("https://img.icons8.com/ios-filled/500/0077b6/fingerprint.png");
        background-repeat: no-repeat; 
        background-position: center; 
        background-size: 400px;
        background-attachment: fixed;
        background-blend-mode: soft-light;
    }
    
    /* Glassmorphism for Containers (Nano-Tech Feel) */
    [data-testid="stForm"], .stTabs, .stTab, [data-testid="stExpander"], .stChatMessage {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px !important;
        border: 1px solid rgba(0, 119, 182, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1) !important;
        padding: 20px !important;
    }
    
    /* Medical Blue Accents */
    .stButton>button {
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0096c7 !important;
        transform: scale(1.02);
    }
    
    /* Emergency Button */
    .emergency-btn {
        background-color: #d00000 !important;
        color: white !important;
        font-weight: bold !important;
        border: 2px solid white !important;
    }
    
    /* Nano-Tech Input Styling */
    .stTextInput input {
        border-radius: 10px !important;
        border: 1px solid #0077b6 !important;
        font-size: 16px !important;
    }
    
    /* Fingerprint Icon for Headers */
    .fingerprint-header {
        font-size: 80px;
        text-align: center;
        color: #0077b6;
        margin-top: -20px;
        filter: drop-shadow(0 0 10px rgba(0, 119, 182, 0.5));
    }
    
    .hacker-alert { 
        background-color: #1a1a1a; 
        color: #ff4b4b; 
        padding: 50px; 
        text-align: center; 
        border: 10px solid #ff4b4b; 
        border-radius: 20px;
        animation: blinker 0.8s linear infinite; 
        font-family: 'Courier New', Courier, monospace;
    }
    @keyframes blinker { 50% { opacity: 0.3; } }
</style>
""", unsafe_allow_html=True)

# 6. CYBER-SECURITY LOCKDOWN
if st.session_state.system_locked:
    st.markdown('<div class="hacker-alert">🚨 SECURITY BREACH! SYSTEM LOCKED<br>Please Contact Admin</div>', unsafe_allow_html=True)
    unlock = st.text_input("Fungura Sisitemu (Admin Key):", type="password")
    if st.button("EMEZA"):
        if unlock == MASTER_RECOVERY_KEY:
            st.session_state.system_locked = False
            st.rerun()
        else:
            st.error("Urufunguzo si rwo!")
    st.stop()

# 7. SIDEBAR (NANO-TECH STYLE)
with st.sidebar:
    st.markdown(f"<h2 style='color:#0077b6; text-align:center;'>🏥 BJ TECH</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;'>🕒 {datetime.now().strftime('%H:%M:%S')}</p>", unsafe_allow_html=True)
    st.divider()
    role = st.radio("HITAMO AHO WINJIRA:", ["🏠 Patient Kiosk", "🧪 Laboratory", "⚙️ Admin Dashboard"])
    st.divider()
    st.info("BJ TECH Nano-Shield v2.0 is Active.")

# --- PAGE: KIOSK (PATIENT) ---
if role == "🏠 Patient Kiosk":
    st.markdown("<div class='fingerprint-header'>☝️</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#0077b6;'>Patient Access</h1>", unsafe_allow_html=True)
    
    if not st.session_state.current_user:
        with st.form("Login"):
            st.subheader("Kwiyandikisha / Kwinjira")
            p_phone = st.text_input("Nimero ya Foni:", placeholder="078...")
            p_name = st.text_input("Amazina yombi:")
            
            # Confirmation Button
            submit = st.form_submit_button("EMEZA KWINJIRA")
            
            if submit:
                if not p_phone or not p_name:
                    st.warning("Uzuza neza imyirondoro yawe!")
                elif check_for_hacking(p_phone) or check_for_hacking(p_name):
                    st.session_state.system_locked = True
                    st.rerun()
                else:
                    new_id = p_phone[-6:] if p_phone else "000000"
                    if new_id not in st.session_state.db:
                        st.session_state.db[new_id] = {"izina": p_name, "phone": p_phone, "results": "", "meds": ""}
                    st.session_state.current_user = new_id
                    update_activity()
                    st.success("Winjijwe neza!")
                    time.sleep(1)
                    st.rerun()
    else:
        curr = st.session_state.db[st.session_state.current_user]
        st.markdown(f"<h3 style='color:#0077b6;'>Muraho, {curr['izina']}!</h3>", unsafe_allow_html=True)
        
        # Logout button
        if st.button("SOHOKA (LOGOUT)"):
            st.session_state.current_user = None
            st.session_state.messages = []
            st.rerun()

        # EMERGENCY BUTTONS
        st.write("---")
        st.subheader("Ukeneye ubufasha bwihuse?")
        col1, col2, col3 = st.columns(3)
        if col1.button("🩸 AMARASO (Bleeding)", use_container_width=True): 
            curr["emergency"] = "BLEEDING"; update_activity(); st.error("Ubufasha buraje!")
        if col2.button("🤰 INDA (Pregnancy)", use_container_width=True): 
            curr["emergency"] = "PREGNANCY"; update_activity(); st.error("Ubufasha buraje!")
        if col3.button("🤢 IZINDI (Other)", use_container_width=True): 
            curr["emergency"] = "CRITICAL"; update_activity(); st.error("Ubufasha buraje!")

        # HIGH-SPEED AI CHAT
        st.write("---")
        st.subheader("Baza AI Muganga (Medical Assistant)")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if prompt := st.chat_input("Andika hano...", on_submit=update_activity):
            if check_for_hacking(prompt):
                st.session_state.system_locked = True
                st.rerun()
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            with st.chat_message("assistant"):
                res_placeholder = st.empty()
                full_res = ""
                try:
                    response_stream = model.generate_content(f"Advice {curr['izina']} in Kinyarwanda about this medical concern: {prompt}", stream=True)
                    for chunk in response_stream:
                        full_res += chunk.text
                        res_placeholder.markdown(full_res + "▌")
                    res_placeholder.markdown(full_res)
                except:
                    full_res = "AI ntabwo iri kuboneka ubu. Gerageza nyuma."
                    res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})

# --- PAGE: LABORATORY (MULTIPLE CHOICE) ---
elif role == "🧪 Laboratory":
    st.markdown("<div class='fingerprint-header'>🧪</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#0077b6;'>Laboratory Portal</h1>", unsafe_allow_html=True)
    
    lab_id = st.selectbox("Hitamo Umurwayi:", list(st.session_state.db.keys()))
    if lab_id:
        p = st.session_state.db[lab_id]
        st.info(f"Umurwayi: **{p['izina']}** | Phone: {p['phone']}")
        
        with st.container():
            tests = st.multiselect("Indwara basanze (Hitamo izo ubonye):", ["Malaria", "Typhoid", "Amoeba", "Infection", "Flu", "UTI", "Diabetes"])
            
            # Confirm Button for Lab
            if st.button("EMEZA NO KOHEREZA SMS (AI)"):
                if not tests:
                    st.warning("Hitamo nibura indwara imwe!")
                else:
                    all_t = ", ".join(tests)
                    p["results"] = all_t
                    with st.spinner("AI iri gutegura ubutumwa..."):
                        try:
                            ai_sms = model.generate_content(f"Andika SMS ya Kinyarwanda kuri {p['izina']} urwaye {all_t}. Mubwire imiti n'inama mu ncamake.").text
                            p["meds"] = ai_sms
                            st.success("Ibipimo na SMS byoherejwe!")
                            st.markdown(f"**AI SMS yoherejwe:** {ai_sms}")
                        except:
                            st.error("AI ntabwo ibashije kwandika SMS ubu.")

# --- FOOTER ---
st.markdown("<div style='position:fixed; bottom:10px; right:20px; font-size:12px; color:#0077b6; font-weight:bold;'>BJ TECH MEDICAL NANO-OS v2.0 | SECURE 🛡️</div>", unsafe_allow_html=True)
