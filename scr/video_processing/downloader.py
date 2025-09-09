import os
import yt_dlp
import validators
from moviepy import VideoFileClip

def validate_url(url):
    if not validators.url(url):
        raise ValueError("Invalid URL format.")
    if "youtube.com" not in url and "youtu.be" not in url:
        raise ValueError("Only YouTube URLs are supported.")
    return True

def download_video(url, output_path="downloads", max_duration=600):
    validate_url(url)
    os.makedirs(output_path, exist_ok=True)
    out_file = os.path.join(output_path, "%(title)s.%(ext)s")

    ydl_opts = {
        "outtmpl": out_file,
        "format": "mp4/bestvideo+bestaudio/best",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info.get("duration") and info["duration"] > max_duration:
            raise ValueError(f"Video too long (> {max_duration/60:.0f} minutes).")
        file_path = ydl.prepare_filename(info)
        if not file_path.endswith(".mp4"):
            file_path = file_path.rsplit(".", 1)[0] + ".mp4"
        return file_path

def ensure_mp4(filepath):
    if not filepath.endswith(".mp4"):
        clip = VideoFileClip(filepath)
        new_path = filepath.rsplit(".", 1)[0] + ".mp4"
        clip.write_videofile(new_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        return new_path
    return filepath
