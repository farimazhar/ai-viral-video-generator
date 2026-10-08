import streamlit as st
import edge_tts
import asyncio
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="AI Viral Video Generator", page_icon="🔥")
st.title("🔥 AI Viral Video Generator")
st.write("Photo + Script = Viral Video!")

text_input = st.text_area("Write your script:", "Hello! Today I will show you how to create a viral video using AI.")
uploaded_image = st.file_uploader("Upload your photo", type=["jpg", "png", "jpeg"])

async def create_voice(text):
    voice = "ur-PK-UzmaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")
    return "voice.mp3"

def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

if st.button("Generate Video 🚀"):
    if not text_input or not uploaded_image:
        st.error("Please provide both script and photo!")
    else:
        with open("photo.jpg", "wb") as f:
            f.write(uploaded_image.getbuffer())
        with st.spinner("Creating voice..."):
            run_async(create_voice(text_input))
        with st.spinner("Creating video..."):
            img = Image.open("photo.jpg")
            img = img.resize((1080, 1920))
            img.save("resized.jpg")
            audio = AudioFileClip("voice.mp3")
            clip = ImageClip("resized.jpg").set_duration(audio.duration).set_audio(audio)
            clip.write_videofile("viral_video.mp4", fps=24, codec='libx264', audio_codec='aac')
        st.success("Done! 🔥 Video ready")
        st.video("viral_video.mp4")
        with open("viral_video.mp4", "rb") as f:
            st.download_button("Download Video", f, file_name="viral_video.mp4")
