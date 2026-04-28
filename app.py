import streamlit as st
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder
import time
import json
import base64

# --- FIGMA UI STYLING ---
BG_COLOR = "#0F0F0F" 
ACCENT_COLOR = "#FF4B4B" 
TEXT_COLOR = "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_COLOR}; color: {TEXT_COLOR}; }}
    button {{ 
        background-color: {ACCENT_COLOR} !important; 
        color: white !important; 
        border-radius: 50px !important; 
        border: none !important;
        height: 4em !important;
        width: 100% !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- THE "FORCE PLAY" ALARM HACK ---
def play_alarm():
    # Using a high-frequency beep that cuts through mobile silence
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    html_code = f"""
        <audio autoplay>
            <source src="{sound_url}" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(html_code, height=0)

# --- THE LOGIC ---
def get_intent_and_time(transcript):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = f"""
    Analyze: "{transcript}"
    Return ONLY JSON: {{"task": "string", "seconds": int}}
    If no time is mentioned, use 30.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.choices[0].message.content)

# --- THE INTERFACE ---
st.title("Vibe Recorder")

# MOBILE TIP: If mic fails, check browser permissions for streamlit.app
st.caption("Tap 'Allow' if your browser asks for microphone access.")

audio = mic_recorder(
    start_prompt="⏺️ START RECORDING", 
    stop_prompt="⏹️ STOP & SET", 
    key='recorder'
)

if audio:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with st.spinner("Processing..."):
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=("audio.wav", audio['bytes'])
        ).text
    
    data = get_intent_and_time(transcript)
    task = data['task']
    seconds = data['seconds']
    
    st.success(f"Task: {task} | Timer: {seconds}s")
    
    # Simple Countdown
    bar = st.progress(0)
    for i in range(seconds):
        time.sleep(1)
        bar.progress((i + 1) / seconds)
    
    # TRIGGER THE ALARM
    st.error(f"🚨 ALARM: {task}")
    play_alarm()
    st.balloons()
    
    if st.button("DISMISS"):
        st.rerun()
