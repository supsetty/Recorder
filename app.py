import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: #FFFFFF; }
    .transcript-hero { font-size: 2.2rem; font-weight: 700; color: #FF4B4B; text-align: center; margin: 30px 0; }
    .timer-large { font-size: 8rem; font-weight: 900; text-align: center; color: #FF4B4B; }
    div.stButton > button { border-radius: 100px !important; height: 3.5em !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = "idle"
if 'text' not in st.session_state: st.session_state.text = ""

def trigger_audio():
    # This is the "Beep" logic
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    st.components.v1.html(f"""
        <audio autoplay loop><source src="{sound_url}" type="audio/mpeg"></audio>
    """, height=0)

st.title("Vibe Recorder")

# STATE 1: IDLE / RECORDING
if st.session_state.step == "idle":
    st.write("Ready when you are...")
    captured = speech_to_text(language='en', start_prompt="⏺️ RECORD THOUGHT", stop_prompt="⏹️ STOP", key='stt')
    if captured:
        st.session_state.text = captured
        st.session_state.step = "confirm"
        st.rerun()

# STATE 2: CONFIRMATION (This 'primes' the audio)
elif st.session_state.step == "confirm":
    st.markdown(f'<div class="transcript-hero">"{st.session_state.text}"</div>', unsafe_allow_html=True)
    st.write("### Set alarm for:")
    
    col1, col2, col3 = st.columns(3)
    # Clicking these buttons 'unlocks' the speakers for later
    with col1:
        if st.button("10s"): st.session_state.timer_end, st.session_state.step = time.time() + 10, "counting"; st.rerun()
    with col2:
        if st.button("15s"): st.session_state.timer_end, st.session_state.step = time.time() + 15, "counting"; st.rerun()
    with col3:
        if st.button("20s"): st.session_state.timer_end, st.session_state.step = time.time() + 20, "counting"; st.rerun()

# STATE 3: COUNTDOWN
elif st.session_state.step == "counting":
    remaining = int(st.session_state.timer_end - time.time())
    if remaining > 0:
        st.markdown(f'<div class="timer-large">{remaining}</div>', unsafe_allow_html=True)
        st.write(f"Vibe: **{st.session_state.text}**")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.step = "ringing"; st.rerun()

# STATE 4: RINGING
elif st.session_state.step == "ringing":
    st.markdown(f'<div class="timer-large" style="background:#FF4B4B; color:white; border-radius:30px;">🚨 DONE</div>', unsafe_allow_html=True)
    st.write(f"### {st.session_state.text}")
    trigger_audio() # This will now work because of the earlier button click!
    
    if st.button("✅ FINISHED"):
        st.session_state.step = "idle"
        st.rerun()
    if st.button("⏳ +15s"):
        st.session_state.timer_end = time.time() + 15
        st.session_state.step = "counting"
        st.rerun()
