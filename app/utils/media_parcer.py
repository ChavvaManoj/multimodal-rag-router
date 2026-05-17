import whisper
import os
from moviepy import VideoFileClip

# Load Whisper model once
model = whisper.load_model("base")


def extract_audio_from_video(video_path: str):
    """
    Extract audio from video and save as temporary mp3
    """
    audio_path = video_path.rsplit(".", 1)[0] + "_audio.mp3"

    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    return audio_path


def transcribe_media(file_path: str):
    """
    Supports:
    - mp3
    - wav
    - m4a
    - mp4
    """

    extension = file_path.lower().split(".")[-1]

    # Video file
    if extension == "mp4":
        file_path = extract_audio_from_video(file_path)

    # Transcribe
    result = model.transcribe(file_path)

    return result["text"]