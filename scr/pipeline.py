from scr.video_processing.downloader import download_video, ensure_mp4
from scr.transcription.whisper import transcribe_audio
from scr.video_processing.extractor import extract_video_frames
from scr.nlp.story_generator import generate_story_with_groq
from scr.audio_generation.tts_engine import text_to_speech

def pipeline(input_url_or_file):
    if input_url_or_file.startswith("http"):
        video_path = download_video(input_url_or_file)
    else:
        video_path = ensure_mp4(input_url_or_file)

    audio_text = transcribe_audio(video_path)
    visual_texts = extract_video_frames(video_path)
    story = generate_story_with_groq(audio_text, visual_texts)

    final_text = (
        "Welcome to today's podcast. Sit back and enjoy the story.\n\n"
        + story +
        "\n\n Thank you for listening. Stay tuned for the next episode!"
    )

    podcast_file = "podcast.mp3"
    text_to_speech(final_text, podcast_file)

    return story, podcast_file
