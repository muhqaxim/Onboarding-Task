# from scr.pipeline import pipeline

# if __name__ == "__main__":
#     url_or_file = "https://www.youtube.com/watch?v=uwzViw-T0-A&t=15s"  # or YouTube link
#     story, podcast_file = pipeline(url_or_file)
#     print("Generated Story:\n", story)

from scr.pipeline import pipeline
from scr.audio_generation.tts_engine import text_to_speech

if __name__ == "__main__":
    url_or_file = "https://www.youtube.com/watch?v=uwzViw-T0-A&t=15s"

    # Step 1: Run pipeline (video -> story)
    story, _ = pipeline(url_or_file)
    print("Generated Story")
    print(story)

    # Step 2: Generate podcast audio
    podcast_file = text_to_speech(story, "podcast_story.mp3")
    print(f"\n Podcast saved as {podcast_file}")
