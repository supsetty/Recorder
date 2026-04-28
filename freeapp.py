import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

# --- FIGMA-INSPIRED STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    .transcript-hero { 
        font-size: 2.5rem; font-weight: 800; color: #FF4B4B; 
        text-align: center; margin: 40px 0; line-height: 1.2;
    }
    div.stButton > button { 
        border-radius: 100px !important; height: 4em !important; 
        background-color: #1E1E1E !important; color: white !important;
        border: 1px solid #333 !important; font-size: 1.2rem !important;
    }
    .timer-text { font-size: 5rem; font-weight: 900; text-align: center; color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)

# --- APP STATE ---
if 'step' not in st.session_state: st.session_state.step = "idle"
if 'text' not in st.session_state: st.session_state.text = ""

def play_alarm():
    # Forced interaction beep
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    st.components.v1.html(f'<audio autoplay loop><source src="{sound_url}" type="audio/mpeg"></audio>', height=0)

st.title("Vibe Recorder")

# STEP 1: CAPTURE
if st.session_state.step == "idle":
    st.write("Recording your thought...")
    captured = speech_to_text(language='en', start_prompt="⏺️ TAP TO SPEAK", stop_prompt="⏹️ STOP", key='stt')
    if captured:
        st.session_state.text = captured
        st.session_state.step = "confirm"
        st.rerun()

# STEP 2: DISPLAY & SET (The "Figma" Transcription Screen)
elif st.session_state.step == "confirm":
    st.markdown(f'<div class="transcript-hero">"{st.session_state.text}"</div>', unsafe_allow_html=True)
    st.write("### Set reminder for:")
    
    # These clicks 'unlock' the audio permission for the beep
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("10s"): st.session_state.timer_end, st.session_state.step = time.time() + 10, "counting"; st.rerun()
    with c2:
        if st.button("15s"): st.session_state.timer_end, st.session_state.step = time.time() + 15, "counting"; st.rerun()
    with c3:
        if st.button("20s"): st.session_state.timer_end, st.session_state.step = time.time() + 20, "counting"; st.rerun()

# STEP 3: THE ACTUAL COUNTDOWN
elif st.session_state.step == "counting":
    remaining = int(st.session_state.timer_end - time.time())
    if remaining > 0:
        st.markdown(f'<div class="timer-text">{remaining}</div>', unsafe_allow_html=True)
        st.write(f"Remaining for: **{st.session_state.text}**")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.step = "ringing"; st.rerun()

# STEP 4: ALARM STATE
elif st.session_state.step == "ringing":
    st.markdown(f'<div class="transcript-hero" style="color:white; background:#FF4B4B; padding:50px; border-radius:30px;">🚨 {st.session_state.text.upper()}</div>', unsafe_allow_html=True)
    play_alarm()
    
    if st.button("✅ FINISHED"):
        st.session_state.step = "idle"; st.rerun()
    if st.button("⏳ +5 MINS"):
        st.session_state.timer_end = time.time() + 300
        st.session_state.step = "counting"; st.rerun()
