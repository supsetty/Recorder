import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

# --- FIGMA VIBE ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: white; }
    .hero-text { font-size: 2rem; font-weight: 700; text-align: center; color: #FF4B4B; margin: 20px 0; }
    .timer-huge { font-size: 8rem; font-weight: 900; text-align: center; color: #FF4B4B; }
    div.stButton > button { border-radius: 100px !important; height: 3.5em !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = "idle"
if 'text' not in st.session_state: st.session_state.text = ""

def play_alarm():
    # Forced mobile alarm trigger
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    st.components.v1.html(f"""
        <audio autoplay loop><source src="{sound_url}" type="audio/mpeg"></audio>
        <script>var a = new Audio("{sound_url}"); a.loop = true; a.play();</script>
    """, height=0)

st.title("Vibe Recorder")

# STATE 1: IDLE
if st.session_state.step == "idle":
    captured = speech_to_text(language='en', start_prompt="⏺️ RECORD TASK", stop_prompt="⏹️ STOP", key='stt')
    if captured:
        st.session_state.text = captured
        st.session_state.step = "confirm"
        st.rerun()

# STATE 2: CONFIRM & UNMUTE
elif st.session_state.step == "confirm":
    st.markdown(f'<div class="hero-text">"{st.session_state.text}"</div>', unsafe_allow_html=True)
    st.write("### Set alarm for:")
    
    col1, col2, col3 = st.columns(3)
    # Clicking these buttons unblocks the audio for later!
    with col1:
        if st.button("10s"): st.session_state.timer_end, st.session_state.step = time.time() + 10, "counting"; st.rerun()
    with col2:
        if st.button("15s"): st.session_state.timer_end, st.session_state.step = time.time() + 15, "counting"; st.rerun()
    with col3:
        if st.button("20s"): st.session_state.timer_end, st.session_state.step = time.time() + 20, "counting"; st.rerun()

# STATE 3: COUNTING
elif st.session_state.step == "counting":
    remaining = int(st.session_state.timer_end - time.time())
    if remaining > 0:
        st.markdown(f'<div class="timer-huge">{remaining}</div>', unsafe_allow_html=True)
        st.write(f"Task: **{st.session_state.text}**")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.step = "ringing"; st.rerun()

# STATE 4: RINGING
elif st.session_state.step == "ringing":
    st.markdown(f'<div class="timer-huge" style="background:#FF4B4B; color:white; border-radius:30px;">🚨 DONE</div>', unsafe_allow_html=True)
    st.write(f"### {st.session_state.text}")
    play_alarm()
    
    if st.button("✅ FINISHED"):
        st.session_state.step = "idle"; st.rerun()
    if st.button("⏳ +15s"):
        st.session_state.timer_end = time.time() + 15
        st.session_state.step = "counting"; st.rerun()
