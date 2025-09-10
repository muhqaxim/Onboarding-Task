import torch

# Device selection
def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

# API keys (later load from config.yaml or env variables)
GROQ_API_KEY = "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"
ELEVEN_API_KEY = "sk_eb78a9752bf04c9288f8d3bcc018a4b9967cc19015dabca1"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
