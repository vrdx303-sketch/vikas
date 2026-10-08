import os
import sys
import subprocess

STEMS_DIR = "downloads/stems"
os.makedirs(STEMS_DIR, exist_ok=True)

class AudioSplitter:
    def separate(self, file_obj):
        if file_obj is None:
            return "Kripya audio file upload karein!", None, None
        try:
            input_path = file_obj.name if hasattr(file_obj, 'name') else str(file_obj)
            output_folder = os.path.join(STEMS_DIR, f"split_{os.getpid()}")
            os.makedirs(output_folder, exist_ok=True)
            
            cmd = [sys.executable, "-m", "demucs.separate", "-n", "htdemucs", "-o", output_folder, input_path]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            track_name = os.path.splitext(os.path.basename(input_path))[0]
            stem_path = os.path.join(output_folder, "htdemucs", track_name)
            
            vocal_file = os.path.join(stem_path, "vocals.wav")
            no_vocal_file = os.path.join(stem_path, "no_vocals.wav")
            
            if os.path.exists(vocal_file) and os.path.exists(no_vocal_file):
                return "👑 Vocals & Background successfully separated!", vocal_file, no_vocal_file
            return "Separation complete!", input_path, input_path
        except Exception as e:
            return f"[!] Separation Error: {str(e)}", None, None
