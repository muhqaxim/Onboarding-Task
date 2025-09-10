import whisper
from moviepy import VideoFileClip
from scr.utils.config_loader import get_device

device = get_device()
whisper_model = whisper.load_model("base", device=device)

def transcribe_audio(video_path):
    print("Transcribing audio from:", video_path)
    clip = VideoFileClip(video_path)
    print("here is clip:", clip)

    audio_path = video_path.replace(".mp4", ".wav")
    clip.audio.write_audiofile(audio_path)

    result = whisper_model.transcribe(audio_path)
    print("here resukt of transcribe_audio:", result["text"])
    return result["text"]
