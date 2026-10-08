import streamlit as st
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip
import os
import uuid

st.set_page_config(page_title="AI Viral Video Generator", page_icon="🚀")
st.title("AI Viral Video Generator 🚀")
st.write("Upload your image or video and convert your script into a viral video.")

# 1. UPLOAD SECTION - Supports Image and Video
uploaded_file = st.file_uploader(
    "Upload your Image or Video", 
    type=["jpg", "jpeg", "png", "mp4", "mov"]
)

# 2. SCRIPT SECTION
script_text = st.text_area(
    "Write your script here",
    value="Hi, I'm a Software Engineer. I built an AI tool that converts any script into a viral video.",
    height=150
)

voice = st.selectbox("Select Voice", ["en-US-JennyNeural", "en-US-GuyNeural"])

# 3. FUNCTION TO GENERATE VOICE
async def generate_voice(text, voice_name, output_file):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_file)

# 4. GENERATE BUTTON
if st.button("Generate Viral Video"):
    if uploaded_file is None:
        st.warning("Please upload an image or video first!")
    elif not script_text:
        st.warning("Please write your script!")
    else:
        with st.spinner("Generating your video..."):
            try:
                audio_file = f"audio_{uuid.uuid4()}.mp3"
                final_video = f"final_{uuid.uuid4()}.mp4"
                
                # Generate Audio
                asyncio.run(generate_voice(script_text, voice, audio_file))
                audio_clip = AudioFileClip(audio_file)
