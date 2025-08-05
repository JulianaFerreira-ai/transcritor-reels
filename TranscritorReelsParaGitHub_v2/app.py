import os
import streamlit as st
import yt_dlp
import whisper
from moviepy.editor import VideoFileClip

def download_instagram_reel(reel_url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'outtmpl': f'{output_dir}/video.%(ext)s',
        'format': 'mp4/bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([reel_url])
    for file in os.listdir(output_dir):
        if file.endswith(".mp4"):
            return os.path.join(output_dir, file)
    return None

def extract_audio(video_path, output_audio="audio.mp3"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio, verbose=False, logger=None)
    return output_audio

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language='pt')
    return result["text"]

def main():
    st.set_page_config(page_title="Transcritor de Reels", layout="centered")
    st.title("🎧 Transcritor de Reels do Instagram")
    st.write("Cole abaixo o link de um Reels PÚBLICO do Instagram para transcrever o áudio.")
    reel_url = st.text_input("Link do Reels:")

    if st.button("Transcrever") and reel_url:
        with st.spinner("Baixando o vídeo do Reels..."):
            video_path = download_instagram_reel(reel_url)

        if video_path:
            st.success("Vídeo baixado com sucesso!")
            with st.spinner("Extraindo áudio..."):
                audio_path = extract_audio(video_path)
            with st.spinner("Transcrevendo com IA (Whisper)..."):
                transcription = transcribe_audio(audio_path)
            st.subheader("📝 Transcrição:")
            st.text_area("Resultado:", transcription, height=300)
        else:
            st.error("Erro ao baixar o vídeo. Verifique o link.")

if __name__ == "__main__":
    main()