import streamlit as st
import edge_tts
import asyncio
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip

st.set_page_config(page_title="AI Viral Video Generator", page_icon="🔥")
st.title("🔥 AI Viral Video Generator")
st.write("Photo + Script = Viral Video!")

text_input = st.text_area("Script likho:", "Assalamualaikum! Aaj mai AI se viral video banana sikhaungi.")
uploaded_image = st.file_uploader("Photo upload karo", type=["jpg", "png", "jpeg"])

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

if st.button("Video Banao 🚀"):
    if not text_input or not uploaded_image:
        st.error("Text aur photo dono do!")
    else:
        with open("photo.jpg", "wb") as f:
            f.write(uploaded_image.getbuffer())
        
        with st.spinner("Voice ban rahi hai..."):
            run_async(create_voice(text_input))
        
        with st.spinner("Video ban raha hai..."):
            # Photo ko resize karo
            img = Image.open("photo.jpg")
            img = img.resize((1080, 1920))
            img.save("resized.jpg")

            audio = AudioFileClip("voice.mp3")
            clip = ImageClip("resized.jpg").set_duration(audio.duration).set_audio(audio)
            clip.write_videofile("viral_video.mp4", fps=24, codec='libx264', audio_codec='aac')
        
        st.success("Done! 🔥 Video ready hai")
        st.video("viral_video.mp4")
        with open("viral_video.mp4", "rb") as f:
            st.download_button("Download Video", f, file_name="viral_video.mp4")
