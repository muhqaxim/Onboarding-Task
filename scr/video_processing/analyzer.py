import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from scr.utils.config_loader import get_device

device = get_device()

# Load BLIP model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
).to(device)

def generate_caption(frame):
    inputs = processor(frame, return_tensors="pt").to(device)
    out = blip_model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)
