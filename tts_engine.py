import os
import sys

# Pen Drive routing ensure karna
PEN_DRIVE_PATH = "E:\\RDX_AI_Storage"
if os.path.exists("E:\\"):
    os.environ["HF_HOME"] = os.path.join(PEN_DRIVE_PATH, "huggingface")
    os.environ["TORCH_HOME"] = os.path.join(PEN_DRIVE_PATH, "torch")

from transformers import AutoProcessor, BarkModel
import torch
import soundfile as sf

print("[*] Pen drive se Sukuna TTS Model load ho raha hai...")
processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small")

TTS_DIR = "downloads/tts"
os.makedirs(TTS_DIR, exist_ok=True)

class TextToSpeechEngine:
    def synthesize(self, text, voice_choice=None):
        if not text or not text.strip():
            return "Kripya kuch text daalein, laadle!", None
        
        try:
            file_name = f"Vikas_RDX_Sukuna_{os.getpid()}.wav"
            output_path = os.path.join(TTS_DIR, file_name)
            
            print(f"[*] Generating Sukuna villain voice safely...")
            
            # Text processing with voice preset handled properly
            inputs = processor(
                text=[text],
                voice_preset="v2/en_speaker_9",
                return_tensors="pt"
            )
            
            speech_values = model.generate(**inputs)
            audio_array = speech_values.cpu().numpy().squeeze()
            
            sf.write(output_path, audio_array, 24000)
            
            if os.path.exists(output_path):
                return "👑 RDX AI Voice (Sukuna Style) successfully generated!", output_path
            return "TTS generation fail ho gaya!", None
        except Exception as e:
            return f"[!] TTS Error: {str(e)}", None