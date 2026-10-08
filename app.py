import streamlit as st
import edge_tts
import asyncio
from PIL import Image

# Fix for moviepy v1 and v2
try:
    from moviepy.editor import ImageClip, AudioFileClip
except ImportError:
    from moviepy import ImageClip, AudioFileClip

st.set_page_config(page_title="AI Viral Video Generator", page_icon="🔥")

st.title("🔥 AI Viral Video Generator")
st.write("Photo + Script = Viral Video in 10 seconds!")

# Input fields
text_input = st.text_area("Write your script:", "Hello! Today I will show you how to create a viral video using AI.")
uploaded_image = st.file_uploader("Upload your photo", type=["jpg", "png", "jpeg"])

# Function to create voice
async def create_voice(text):
    voice = "ur-PK-UzmaNeural"  # Urdu female voice, change to en-US-JennyNeural for English
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")
    return "voice.mp3"

def run_async(coro):
    try:
