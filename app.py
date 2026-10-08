import streamlit as st
import asyncio
import edge_tts
from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip
import os
import uuid

st.set_page_config(page_title="AI Viral Video Generator", page_icon="🚀")
st.title("AI Viral Video Generator 🚀")
st.write("Upload your image or video and convert your script into a viral video.")

uploaded_file = st.file_uploader(
    "Upload your Image or Video", 
    type=["jpg", "jpeg", "png", "mp4", "mov"]
)

script_text = st.text_area(
    "Write your script here",
    value="Hi, I'm a Software Engineer. I built an AI tool that converts any script into a viral video.",
    height=150
)

voice = st.selectbox("Select Voice", ["en-US-JennyNeural", "en-US-GuyNeural"])

async def generate_voice(text, voice_name, output_file):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(output_file)

if st.button("Generate Viral Video"):
    if uploaded_file is None:
        st.warning("Please upload an image or video first!")
    elif not script_text:
        st.warning("Please write your script!")
    else:
        with st.spinner("Generating your video..."):
            audio_file = f"audio_{uuid.uuid4()}.mp3"
            final_video = f"final_{uuid.uuid4()}.mp4"
            temp_path = ""

            try:
                asyncio.run(generate_voice(script_text, voice, audio_file))
                audio_clip = AudioFileClip(audio_file)

                if uploaded_file.type.startswith('video'):
                    temp_path = f"temp_{uuid.uuid4()}.mp4"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    video_clip = VideoFileClip(temp_path)
                    if video_clip.duration > audio_clip.duration:
                        video_clip = video_clip.subclip(0, audio_clip.duration)
                    
                    final_clip = video_clip.set_audio(audio_clip)
                    final_clip.write_videofile(final_video, fps=24, codec='libx264', audio_codec='aac', logger=None)

                else:
                    temp_path = f"temp_{uuid.uuid4()}.jpg"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    image_clip = ImageClip(temp_path, duration=audio_clip.duration)
                    final_clip = image_clip.set_audio(audio_clip)
                    final_clip.write_videofile(final_video, fps=24, codec='libx264', audio_codec='aac', logger=None)
                
                st.success("Your video is ready!")
                st.video(final_video)
                
                with open(final_video, "rb") as file:
                    st.download_button("Download Video", file, file_name="viral_video.mp4")

            except Exception as e:
                st.error(f"Error: {e}")
            
            finally:
                # Cleanup all temp files
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                if os.path.exists(final_video):
                    os.remove(final_video)
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)
