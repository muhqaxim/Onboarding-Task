import whisper
from moviepy import VideoFileClip
from scr.utils.config_loader import get_device

device = get_device()
whisper_model = whisper.load_model("base", device=device)

def transcribe_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path)

    result = whisper_model.transcribe(audio_path)
    return result["text"]
