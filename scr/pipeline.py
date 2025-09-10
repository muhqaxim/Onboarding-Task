from scr.video_processing.downloader import download_video, ensure_mp4
from scr.transcription.whisper import transcribe_audio
from scr.video_processing.extractor import extract_video_frames
from scr.nlp.story_generator import generate_story_with_groq

def pipeline(input_url_or_file):
    if input_url_or_file.startswith("http"):
        print("here to check https")
        video_path = download_video(input_url_or_file)
    else:
        print("in else part")

        video_path = ensure_mp4(input_url_or_file)
    if not video_path:
        print("No video path found!")
        video_path = """c:/Users/MOON/Downloads/Onboarding-Task-main/Onboarding-Task-main/downloads/Thirsty Crow Story in English | Moral stories for Kids | Bedtime Stories for Children.mp4"""
    print("going for audio transcription")

    audio_text = transcribe_audio(video_path)
    print("going for visual_texts")

    visual_texts = extract_video_frames(video_path)
    print("going for generate_story_with_groq")

    story = generate_story_with_groq(audio_text, visual_texts)

    final_text = (
        "Welcome to today's podcast. Sit back and enjoy the story.\n\n"
        + story +
        "\n\n Thank you for listening. Stay tuned for the next episode!"
    )
    print("final_text", final_text)

   # podcast_file = "podcast.mp3"
    #text_to_speech(final_text, podcast_file)

    return story
