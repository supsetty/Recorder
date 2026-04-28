import streamlit as st
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder
import time
import json

# --- UI STYLING (Figma-ish) ---
BG_COLOR = "#0F0F0F" 
ACCENT_COLOR = "#FF4B4B" 

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_COLOR}; color: white; }}
    button {{ 
        background-color: {ACCENT_COLOR} !important; 
        color: white !important; 
        border-radius: 50px !important; 
        border: none !important;
        height: 4em !important;
        width: 100% !important;
        font-weight: bold !important;
    }}
    .transcript-box {{
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid {ACCENT_COLOR};
        margin-bottom: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

def play_alarm():
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    html_code = f'<audio autoplay><source src="{sound_url}" type="audio/mp3"></audio>'
    st.components.v1.html(html_code, height=0)

st.title("Vibe Recorder")

# --- RECORDER COMPONENT ---
audio = mic_recorder(
    start_prompt="⏺️ START RECORDING", 
    stop_prompt="⏹️ STOP & TRANSCRIBE", 
    key='recorder'
)

if audio:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    with st.spinner("Transcribing..."):
        # 1. WHISPER TRANSCRIPTION
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=("audio.wav", audio['bytes'])
        ).text
    
    # --- NEW: DISPLAY TRANSCRIPTION TO USER ---
    st.markdown(f"""
        <div class="transcript-box">
            <small style="color: {ACCENT_COLOR}; text-transform: uppercase;">What I heard:</small><br>
            <i>"{transcript}"</i>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. LOGIC ROUTER (GPT-4o)
    with st.spinner("Extracting intent..."):
        prompt = f"Analyze: '{transcript}'. Return ONLY JSON: {{\"task\": \"string\", \"seconds\": int}}. If no time mentioned, use 60."
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        data = json.loads(response.choices[0].message.content)
    
    task = data['task']
    seconds = data['seconds']
    
    st.write(f"⏱️ Setting alarm for **{task}** ({seconds}s)")
    
    # 3. COUNTDOWN
    bar = st.progress(0)
    for i in range(seconds):
        time.sleep(1)
        bar.progress((i + 1) / seconds)
    
    # 4. ALARM TRIGGER
    st.error(f"🚨 ALERT: {task}")
    play_alarm()
    st.balloons()
    
    if st.button("DISMISS"):
        st.rerun()
