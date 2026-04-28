import streamlit as st
from streamlit_mic_recorder import speech_to_text
import time

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp { background-color: #0A0A0A; color: white; }
.hero-text { font-size: 2rem; font-weight: 700; text-align: center; color: #FF4B4B; margin: 20px 0; }
.timer-huge { font-size: 6rem; font-weight: 900; text-align: center; color: #FF4B4B; }
div.stButton > button {
    border-radius: 100px !important;
    height: 3.5em !important;
    font-weight: bold !important;
    background-color: #FF4B4B;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- STATE ----------
if 'step' not in st.session_state:
    st.session_state.step = "idle"

if 'text' not in st.session_state:
    st.session_state.text = ""

if 'timer_end' not in st.session_state:
    st.session_state.timer_end = None


# ---------- ALARM ----------
def play_alarm():
    sound_url = "https://www.soundjay.com/buttons/beep-01a.mp3"
    st.components.v1.html(f"""
        <script>
        const audio = new Audio("{sound_url}");
        audio.loop = true;

        audio.play().catch(() => {{
            document.addEventListener('click', () => {{
                audio.play();
            }}, {{ once: true }});
        }});
        </script>
    """, height=0)


st.title("Vibe Recorder")

# ---------- STATE 1 ----------
if st.session_state.step == "idle":
    st.write("Tap and speak your reminder")

    captured = speech_to_text(
        language='en',
        start_prompt="⏺️ RECORD",
        stop_prompt="⏹️ STOP",
        key='stt'
    )

    if captured:
        st.session_state.text = captured
        st.session_state.step = "confirm"
        st.rerun()

# ---------- STATE 2 ----------
elif st.session_state.step == "confirm":
    st.markdown(f'<div class="hero-text">"{st.session_state.text}"</div>', unsafe_allow_html=True)
    st.write("Set timer:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("10s"):
            st.session_state.timer_end = time.time() + 10
            st.session_state.step = "counting"
            st.rerun()

    with col2:
        if st.button("15s"):
            st.session_state.timer_end = time.time() + 15
            st.session_state.step = "counting"
            st.rerun()

    with col3:
        if st.button("20s"):
            st.session_state.timer_end = time.time() + 20
            st.session_state.step = "counting"
            st.rerun()

# ---------- STATE 3 ----------
elif st.session_state.step == "counting":
    remaining = int(st.session_state.timer_end - time.time())

    if remaining > 0:
        st.markdown(f'<div class="timer-huge">{remaining}</div>', unsafe_allow_html=True)
        st.write(f"Task: **{st.session_state.text}**")

        time.sleep(1)
        st.rerun()

    else:
        st.session_state.step = "ringing"
        st.rerun()

# ---------- STATE 4 ----------
elif st.session_state.step == "ringing":
    st.markdown(
        '<div class="timer-huge" style="background:#FF4B4B; color:white; border-radius:20px;">🚨 DONE</div>',
        unsafe_allow_html=True
    )

    st.write(f"### {st.session_state.text}")

    play_alarm()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ FINISHED"):
            st.session_state.step = "idle"
            st.rerun()

    with col2:
        if st.button("⏳ +15s"):
            st.session_state.timer_end = time.time() + 15
            st.session_state.step = "counting"
            st.rerun()
