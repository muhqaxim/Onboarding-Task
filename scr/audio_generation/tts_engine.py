# import requests
# from scr.utils.config_loader import ELEVEN_API_KEY, VOICE_ID

# def text_to_speech(text, filename):
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
#     headers = {"xi-api-key": ELEVEN_API_KEY, "Content-Type": "application/json"}
#     data = {"text": text, "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}

#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         with open(filename, "wb") as f:
#             f.write(response.content)
#     else:
#         raise Exception("ElevenLabs Error: " + response.text)
from elevenlabs import ElevenLabs

# Initialize client once (reuse instead of re-creating in each call)
client = ElevenLabs(api_key="YOUR_API_KEY")  # replace with your real key

def text_to_speech(text: str, output_file: str):
    # Generate audio from text
    audio = client.generate(
        text=text,
        voice="Rachel",  # you can change to another available voice
        model="eleven_multilingual_v2"
    )

    # Save audio to file
    with open(output_file, "wb") as f:
        f.write(audio)

    print(f"✅ Audio saved to {output_file}")


