import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time
import re

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0F0F0F; color: white; }
    .permission-card {
        background-color: #1E1E1E; padding: 20px; border-radius: 15px;
        border: 2px solid #FF4B4B; text-align: center; margin-bottom: 20px;
    }
    button { border-radius: 50px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATES ---
if 'permissions_granted' not in st.session_state:
    st.session_state.permissions_granted = False
if 'alarm_status' not in st.session_state:
    st.session_state.alarm_status = "idle"

# --- THE PERMISSION CHECK ---
if not st.session_state.permissions_granted:
    st.markdown('''
        <div class="permission-card">
            <h3>Permission Required</h3>
            <p>To record your voice and play the alarm, please tap the button below and "Allow" microphone access.</p>
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("🔓 ENABLE MIC & AUDIO"):
        # This is a 'dummy' sound to unlock the audio channel on mobile
        st.components.v1.html("""
            <script>
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(function(stream) {
                    window.parent.postMessage({type: 'permission', status: 'granted'}, '*');
                })
                .catch(function(err) {
                    alert("Microphone access is required for this app to work.");
                });
            </script>
        """, height=0)
        st.session_state.permissions_granted = True
        st.rerun()

# --- THE MAIN APP (Only shows if permissions are granted) ---
else:
    st.title("Vibe Recorder")
    
    if st.session_state.alarm_status == "idle":
        text = speech_to_text(language='en', start_prompt="⏺️ RECORD TASK", stop_prompt="⏹️ STOP", key='STT')
        if text:
            st.session_state.task_name = text
            nums = re.findall(r'\d+', text)
            secs = int(nums[0]) if nums else 30
            st.session_state.timer_end = time.time() + secs
            st.session_state.alarm_status = "counting"
            st.rerun()

    elif st.session_state.alarm_status == "counting":
        remaining = int(st.session_state.timer_end - time.time())
        if remaining > 0:
            st.metric("T-Minus", f"{remaining}s", st.session_state.task_name)
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.alarm_status = "ringing"
            st.rerun()

    elif st.session_state.alarm_status == "ringing":
        st.error(f"🚨 {st.session_state.task_name.upper()}")
        # High-pitched alarm beep
        st.components.v1.html('<audio autoplay loop><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mp3"></audio>', height=0)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ DONE"):
                st.session_state.alarm_status = "idle"
                st.rerun()
        with col2:
            if st.button("⏳ +5 MINS"):
                st.session_state.timer_end = time.time() + 300
                st.session_state.alarm_status = "counting"
                st.rerun()
