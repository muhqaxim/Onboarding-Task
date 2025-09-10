import requests
from scr.utils.config_loader import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def generate_story_with_groq(audio_text, visual_texts, genre="adventure"):
    combined = (
    f"You are a creative storyteller. Write a {genre} story between 300 and 800 words. "
    "I will give you two sources: (1) an audio transcript containing dialogue or narration, "
    "and (2) visual captions describing scenes from the video. "
    "Your job is to combine these into a single smooth, engaging narrative with characters, plot, and resolution. "

    "Important: Do NOT mention phrases like 'audio transcript' or 'visual captions'. "
    "Instead, weave their content naturally into the story as if it were happening. "
    "Use paragraphs, not bullet points.\n\n"

    f"Transcript:\n{audio_text}\n\n"
    "Scenes:\n" + "\n".join(f"- {cap}" for cap in visual_texts) + "\n\n"
    "Now write the final story."
  )

    payload = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{"role": "user", "content": combined}],
        "temperature": 0.8,
        "max_tokens": 1200
    }

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    print("Groq API response status:", response.status_code)
    print("Groq API response from groq:")

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Groq API Error {response.status_code}: {response.text}")
