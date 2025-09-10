
##  Getting Started

### Prerequisites

- Python 3.10 or above
- A command-line interface (e.g., Terminal, PowerShell)

### Installation

Install all required dependencies using the following command:

```bash
pip install -r requirements.txt
Configuration
You need to configure API keys for both ElevenLabs and Grok.

Note: Make sure to keep your API keys private and do not commit them to version control.

ElevenLabs API
Open audio_generator.py and go to line 9. Replace the placeholder with your ElevenLabs API key:

python
Copy code
client = ElevenLabs(api_key=("your_api"))
Grok API
Open config_loader.py and go to line 8. Insert your Grok API key:

python
Copy code
GROQ_API_KEY = "your_api"
Usage
Run the main script to start the project:

bash
Copy code
python main.py
Voice Customization (ElevenLabs)
If you'd like to change the voice model, edit audio_generator.py at line 12 within the VOICE_OPTIONS dictionary:

python
Copy code
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
How to Add a Custom Voice
Create a custom voice model in ElevenLabs.

Copy its voice_id.

Insert it under the "custom" key:

python
Copy code
"custom": {
    "voice_id": "your_custom_voice_id"
}
[!TIP]
To switch between voices, use the following options within VOICE_OPTIONS: "jamaican", "black_american", or "custom" for your own model.

Summary
Install dependencies: pip install -r requirements.txt

Configure ElevenLabs API in audio_generator.py (line 9)

Configure Grok API in config_loader.py (line 8)

Customize voice model in audio_generator.py (line 12)

Run the project: python main.py

