import streamlit as st
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

st.set_page_config(page_title="AI Viral Video Generator", page_icon="🔥")
st.title("🔥 AI Viral Video Generator")

text_input = st.text_area("Script likho:", "Assalamualaikum! Aaj mai AI se viral video banana sikhaungi.")
uploaded_image = st.file_uploader("Photo upload karo", type=["jpg", "png", "jpeg"])

async def create_voice(text):
    voice = "ur-PK-Uzma-Apollo"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")
    return "voice.mp3"

def create_video(image_path, audio_path, script_text):
    audio = AudioFileClip(audio_path)
    clip = ImageClip(image_path).set_duration(audio.duration).set_audio(audio)
    clip = clip.resize(height=1920).set_position("center")
    txt = TextClip(script_text[:60], fontsize=60, color='white', stroke_color='black', stroke_width=2, method='caption', size=(900, None))
    txt = txt.set_duration(audio.duration).set_position(('center', 0.8), relative=True)
    final = CompositeVideoClip([clip, txt], size=(1080, 1920))
    final.write_videofile("viral_video.mp4", fps=24, codec='libx264', audio_codec='aac')
    return "viral_video.mp4"

if st.button("Video Banao 🚀"):
    if not text_input or not uploaded_image:
        st.error("Text aur photo dono do!")
    else:
        with open("photo.jpg", "wb") as f:
            f.write(uploaded_image.getbuffer())
        with st.spinner("Voice ban rahi hai..."):
            asyncio.run(create_voice(text_input))
        with st.spinner("Video ban raha hai..."):
            create_video("photo.jpg", "voice.mp3", text_input)
        st.success("Done!")
        st.video("viral_video.mp4")
