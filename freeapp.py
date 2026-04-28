import streamlit as st
import time

# --- UI STYLING ---
st.set_page_config(page_title="Free Vibe Recorder")

st.markdown("""
    <style>
    .stApp { background-color: #0F0F0F; color: white; }
    .alarm-box {
        padding: 20px;
        background-color: #FF4B4B;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Vibe Recorder (Free Version)")

# --- FREE BROWSER TRANSCRIPTION ---
# This uses a simple text input as a fallback or browser speech
text_input = st.text_input("What is the task? (e.g., Check zine in 10 seconds)", placeholder="Type or use your phone's voice-to-text on keyboard")

if text_input:
    # Basic logic to find numbers in your text
    words = text_input.split()
    seconds = 30 # Default
    for word in words:
        if word.isdigit():
            seconds = int(word)
            break
    
    st.write(f"⏱️ Timer set for {seconds} seconds...")
    
    # Progress bar
    bar = st.progress(0)
    for i in range(seconds):
        time.sleep(1)
        bar.progress((i + 1) / seconds)
    
    # Alarm Trigger
    st.markdown(f'<div class="alarm-box">🚨 TIME IS UP: {text_input}</div>', unsafe_allow_html=True)
    
    # Play free beep sound
    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mp3"></audio>', height=0)
    
    if st.button("DONE"):
        st.rerun()
