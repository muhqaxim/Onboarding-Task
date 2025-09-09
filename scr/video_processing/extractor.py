import cv2
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from scr.utils.config_loader import get_device

device = get_device()

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

def extract_video_frames(video_path, threshold=30.0):
    cap = cv2.VideoCapture(video_path)
    prev_hist = None
    texts = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist = cv2.normalize(hist,hist).flatten()

        if prev_hist is not None:
            diff = cv2.compareHist(prev_hist, hist, cv2.HISTCMP_BHATTACHARYYA)
            if diff > 0.3:
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                inputs = processor(rgb, return_tensors="pt").to(device)
                out = blip_model.generate(**inputs)
                caption = processor.decode(out[0], skip_special_tokens=True)
                texts.append(caption)

        prev_hist = hist

    cap.release()
    return texts
