import torch

# Device selection
def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

# API keys (later load from config.yaml or env variables)
GROQ_API_KEY = "your api key"
ELEVEN_API_KEY = "your api key"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
