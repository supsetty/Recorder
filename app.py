import streamlit as st
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder
import time

# UI Settings
st.set_page_config(page_title="Vibe Recorder", layout="centered")

# Visual Styling
st.markdown("""
    <style>
    .stApp { background-color: #0F0F0F; color: #FFFFFF; font-family: sans-serif; }
    div.stButton > button { background-color: #333; color: white; border-radius: 20px; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

st.title("Vibe Recorder")

# Audio Input
audio = mic_recorder(start_prompt="Record Task", stop_prompt="Stop", key='recorder')

if audio:
    # This shows the user what they recorded
    st.audio(audio['bytes'])
    
    # Placeholder for the "Brain"
    st.write("---")
    st.info("Intent detected: Reminder")
    
    # Timer Simulation
    if st.button("Set 10s Timer"):
        with st.empty():
            for seconds in range(10, 0, -1):
                st.write(f"⏳ Alarm in {seconds}s")
                time.sleep(1)
            st.write("🚨 **TIME IS UP! CHECK YOUR ZINE.**")
            if st.button("DONE"):
                st.success("Task cleared.")
