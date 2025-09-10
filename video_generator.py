import os
import re
import math
import uuid
import numpy as np
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, VideoClip
import moviepy.video.fx as vfx


W, H = 1920, 1080 
FPS = 30
MARGIN = 80
CAPTION_MAX_CHARS = 90
CAPTION_MAX_LINES = 3
CAPTION_MIN_SEC = 1.8
CAPTION_MAX_SEC = 6.0
FONT_SIZE = 58
LINE_SPACING = 1.15
TEXT_COLOR = (255, 255, 255, 255)
STROKE_COLOR = (0, 0, 0, 220)
STROKE_WIDTH = 4
BOX_PAD_X = 24
BOX_PAD_Y = 14
BOX_COLOR = (0, 0, 0, 120)
FADE_DUR = 0.25

OUTPUT_DIR = "outputs/video/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]

def pick_font_path() -> str:
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    return None

def sentence_split(text: str):
    pieces = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in pieces if s.strip()]

def group_into_captions(sentences):
    captions, buf = [], ""
    for s in sentences:
        candidate = (buf + " " + s).strip() if buf else s
        if len(candidate) <= CAPTION_MAX_CHARS:
            buf = candidate
        else:
            if buf:
                captions.append(buf)
            buf = s
    if buf:
        captions.append(buf)
    return captions

def text_width(s, font):
    bbox = font.getbbox(s)
    return bbox[2] - bbox[0]

def wrap_text_lines(text, font, max_width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_width(test, font) <= max_width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = w
        if len(lines) == CAPTION_MAX_LINES:
            remainder = " ".join(words[words.index(w):])
            if remainder:
                lines[-1] += " " + remainder
            return lines
    if cur:
        lines.append(cur)
    return lines

def render_caption_image(text, vw, vh):
    font_path = pick_font_path()
    font = ImageFont.truetype(font_path, FONT_SIZE) if font_path else ImageFont.load_default()
    max_text_width = vw - 2 * MARGIN
    lines = wrap_text_lines(text, font, max_text_width)

    line_heights, line_widths = [], []
    for line in lines:
        bbox = font.getbbox(line)
        line_widths.append(bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])

    line_height = int(sum(line_heights) / len(line_heights)) if line_heights else FONT_SIZE
    total_text_h = int(sum(line_heights) + (len(lines) - 1) * line_height * (LINE_SPACING - 1))
    text_w = max(line_widths) if line_widths else 0

    box_w = text_w + 2 * BOX_PAD_X
    box_h = total_text_h + 2 * BOX_PAD_Y
    x, y = (vw - box_w) // 2, vh - box_h - MARGIN

    img = Image.new("RGBA", (vw, vh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=18, fill=BOX_COLOR)

    cur_y = y + BOX_PAD_Y
    for line in lines:
        w = text_width(line, font)
        lx = x + (box_w - w) // 2
        draw.text((lx, cur_y), line, font=font, fill=TEXT_COLOR,
                  stroke_width=STROKE_WIDTH, stroke_fill=STROKE_COLOR)
        cur_y += int(line_height * LINE_SPACING)
    return img

def allocate_caption_times(captions, total_audio_sec):
    word_counts = [max(1, len(c.split())) for c in captions]
    total_words = sum(word_counts)
    raw_durations = [total_audio_sec * wc / total_words for wc in word_counts]
    clamped = [min(CAPTION_MAX_SEC, max(CAPTION_MIN_SEC, d)) for d in raw_durations]
    scale = total_audio_sec / sum(clamped)
    durations = [d * scale for d in clamped]
    times, t = [], 0.0
    for d in durations:
        start, end = t, min(total_audio_sec, t + d)
        times.append((start, end))
        t = end
    if times:
        s, _ = times[-1]
        times[-1] = (s, total_audio_sec)
    return times

def gradient_bg(t, w=W, h=H):
    cx = w * (0.5 + 0.1 * math.sin(0.2 * t))
    cy = h * (0.55 + 0.08 * math.cos(0.17 * t))
    y, x = np.ogrid[:h, :w]
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    dist_norm = np.clip(dist / (0.9 * max(w, h)), 0, 1)
    c1, c2 = np.array([18, 18, 40]), np.array([75, 35, 120])
    blend = 0.5 + 0.5 * math.sin(0.1 * t)
    base = (1 - dist_norm[..., None]) * c2 + dist_norm[..., None] * c1
    base = (1 - blend) * base + blend * np.roll(base, 1, axis=2)
    return base.clip(0, 255).astype("uint8")

def make_background_clip(duration):
    return VideoClip(lambda t: gradient_bg(t), duration=duration).with_fps(FPS).with_audio(None)

def build_video(story_text, audio_path, out_path):
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    audio = AudioFileClip(audio_path)
    duration = float(audio.duration)

    sentences = sentence_split(story_text)
    captions = group_into_captions(sentences)
    times = allocate_caption_times(captions, duration)

    bg = make_background_clip(duration).resized((W, H)).with_audio(audio)

    caption_clips = []
    for text, (start, end) in zip(captions, times):
        img = render_caption_image(text, W, H)
        clip = (
            ImageClip(np.array(img))
            .with_start(start)
            .with_duration(end - start)
        )
        clip = clip.with_effects([vfx.FadeIn(duration=FADE_DUR)])
        clip = clip.with_effects([vfx.FadeOut(duration=FADE_DUR)])
        caption_clips.append(clip)


    video_filename = f"{uuid.uuid4().hex}.mp4"
    out_path = os.path.join(OUTPUT_DIR, video_filename)



    final = CompositeVideoClip([bg, *caption_clips], size=(W, H)).with_duration(duration)
    final.write_videofile(
        out_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="5000k",
        threads=os.cpu_count() or 4,
        preset="medium"
    )
