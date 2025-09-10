import os
from elevenlabs import generate, save, set_api_key

# Set your API key (use env var if available, otherwise fallback to hardcoded key)
set_api_key(os.getenv("ELEVEN_API_KEY", "sk_eb78a9752bf04c9288f8d3bcc018a4b9967cc19015dabca1"))

def text_to_speech(text: str, output_file: str, voice: str = "Rachel"):
    # Generate audio
    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )

    # Save audio to file
    save(audio, output_file)
    print(f"✅ Audio saved to {output_file}")
    return output_file
