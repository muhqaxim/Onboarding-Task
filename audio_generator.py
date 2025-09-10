import os
from elevenlabs import ElevenLabs

from video_generator import build_video

OUTPUT_DIR = "outputs/audio/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

client = ElevenLabs(api_key=("sk_eb78a9752bf04c9288f8d3bcc018a4b9967cc19015dabca1"))


VOICE_OPTIONS = {
    "jamaican": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM", 
    },
    "black_american": {
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
    },
    "custom": {
        "voice_id": None
    }
}


def generate_audio(text: str, voice_type: str, filename: str):

    if voice_type not in VOICE_OPTIONS:
        raise ValueError(f"Invalid voice type: {voice_type}")

    voice_id = VOICE_OPTIONS[voice_type]["voice_id"]
    if voice_id is None:
        raise ValueError("Custom voice not uploaded yet!")

    audio_stream = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text=text
    )

    filepath = os.path.join(OUTPUT_DIR, f"{filename}.mp3")
    with open(filepath, "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)
    return filepath


def upload_custom_voice(name: str, sample_file: str):
    with open(sample_file, "rb") as f:
        new_voice = client.voices.add(
            name=name,
            files=[f],
            description="Custom uploaded voice"
        )
    VOICE_OPTIONS["custom"]["voice_id"] = new_voice.voice_id
    return new_voice.voice_id

def get_audio(text):

    audio_path = generate_audio(text, "jamaican", "story_jamaican")
    build_video(story_text=text, audio_path=audio_path, out_path="outputs/video/")
    print("going for generating vide with jamaican voice")

    audio_path = generate_audio(text, "black_american", "story_blackamerican")
    build_video(story_text=text, audio_path=audio_path, out_path="outputs/video/")
    print("going for generating vide with black_american voice")


