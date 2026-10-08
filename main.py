import os
import sys
import socket
import time
import threading

# --- SELF-CONTAINED PROJECT ROUTING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

import gradio as gr
import cv2
import numpy as np
from PIL import Image

# Import downloader module safely
try:
    from downloader import MediaDownloader
    downloader = MediaDownloader()
except Exception:
    downloader = None

# Folders setup inside the project
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
WATERMARK_DIR = os.path.join(DOWNLOADS_DIR, "watermark_cleaned")
os.makedirs(WATERMARK_DIR, exist_ok=True)

# --- MACHINE-LEVEL SOURCE CODE PROTECTION (Only runs on Vikas's Laptop) ---
def verify_source_code_protection():
    allowed_user = "vrdx3"  # Tumhare PC ka username
    current_user = os.getlogin()
    if current_user.lower() != allowed_user.lower():
        print(f"[!] SECURITY ERROR: Yeh source code unauthorized machine ({current_user}) par run nahi ho sakta!")
        sys.exit(1)

verify_source_code_protection()

class RDXStudioEngine:
    def remove_image_precise(self, input_image):
        if input_image is None:
            return "कृपया पहले फोटो अपलोड करें!", None
        try:
            img = np.array(input_image)
            img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            h, w, _ = img_cv.shape
            mask = np.zeros((h, w), dtype=np.uint8)
            box_h, box_w = int(h * 0.15), int(w * 0.30)
            mask[h - box_h:h, w - box_w:w] = 255
            cleaned_cv = cv2.inpaint(img_cv, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            output_img = Image.fromarray(cv2.cvtColor(cleaned_cv, cv2.COLOR_BGR2RGB))
            return "वाटरमार्क सफलतापूर्वक साफ कर दिया गया है!", output_img
        except Exception as e:
            return f"त्रुटि: {str(e)}", None

    def remove_video_precise(self, input_video_path):
        if not input_video_path:
            return "कृपया पहले वीडियो अपलोड करें!", None
        try:
            cap = cv2.VideoCapture(input_video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            out_path = os.path.join(WATERMARK_DIR, f"precise_cleaned_video_{os.getpid()}.mp4")
            out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
            box_h, box_w = int(height * 0.12), int(width * 0.18)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                mask = np.zeros((height, width), dtype=np.uint8)
                mask[height - box_h:height, width - box_w:width] = 255
                out.write(cv2.inpaint(frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA))
            cap.release()
            out.release()
            return "वीडियो वाटरमार्क सफलतापूर्वक हटा दिया गया है!", out_path
        except Exception as e:
            return f"वीडियो त्रुटि: {str(e)}", None

    def download_video_secure(self, url):
        if downloader:
            return downloader.download_video(url)
        return "डाउनलोडर मॉड्यूल अनुपलब्ध है", None

    def download_audio_secure(self, url):
        if downloader:
            return downloader.download_audio(url)
        return "डाउनलोडर मॉड्यूल अनुपलब्ध है", None

studio_engine = RDXStudioEngine()

with gr.Blocks(title="rdx_ai_studio", analytics_enabled=False) as demo:
    gr.Markdown("# 🚀 RDX AI Studio - Light & Fast Edition")
    gr.Markdown("विकास नायक का प्रोफेशनल स्टूडियो | rdx_ai_studio 👑")
    
    with gr.Row():
        with gr.Column(scale=1, min_width=280):
            gr.Markdown("### 🛠️ कंट्रोल सेंटर")
            choice = gr.Radio(
                [
                    "🎬 Link to Video Download", 
                    "🎵 Link to Audio Download", 
                    "✨ Remove Image Watermark",
                    "🎬 Remove Video Watermark"
                ], 
                label="फीचर चुनें", 
                value="🎬 Link to Video Download"
            )
            gr.Markdown("---")
            gr.Markdown("**स्थिति:** एक्टिव 🟢\n**मोड:** सुपर-फास्ट & लाइटवेट ⚡")
            
        with gr.Column(scale=3):
            with gr.Group(visible=True) as tab_video:
                gr.Markdown("### 🎬 वीडियो डाउनलोडर")
                v_url = gr.Textbox(label="वीडियो लिंक दर्ज करें", placeholder="https://...")
                v_btn = gr.Button("वीडियो डाउनलोड करें", variant="primary")
                v_status = gr.Textbox(label="स्थिति", lines=2)
                v_file = gr.File(label="डाउनलोड की गई वीडियो फाइल (.mp4)")
                v_btn.click(fn=studio_engine.download_video_secure, inputs=v_url, outputs=[v_status, v_file])

            with gr.Group(visible=False) as tab_audio:
                gr.Markdown("### 🎵 ऑडियो डाउनलोडर")
                a_url = gr.Textbox(label="ऑडियो लिंक दर्ज करें", placeholder="https://...")
                a_btn = gr.Button("ऑडियो डाउनलोड करें (MP3)", variant="primary")
                a_status = gr.Textbox(label="स्थिति", lines=2)
                a_audio = gr.Audio(label="डाउनलोड की गई MP3 फाइल")
                a_btn.click(fn=studio_engine.download_audio_secure, inputs=a_url, outputs=[a_status, a_audio])

            with gr.Group(visible=False) as tab_img_wm:
                gr.Markdown("### ✨ इमेज वाटरमार्क रिमूवर")
                img_input = gr.Image(type="pil", label="वाटरमार्क वाली फोटो अपलोड करें")
                img_btn = gr.Button("वाटरमार्क हटाएं", variant="primary")
                img_status = gr.Textbox(label="स्थिति", lines=2)
                img_output = gr.Image(label="साफ की गई इमेज")
                img_btn.click(fn=studio_engine.remove_image_precise, inputs=img_input, outputs=[img_status, img_output])

            with gr.Group(visible=False) as tab_vid_wm:
                gr.Markdown("### 🎬 वीडियो वाटरमार्क रिमूवर")
                vid_input = gr.Video(label="वीडियो अपलोड करें")
                vid_btn = gr.Button("वीडियो वाटरमार्क हटाएं", variant="primary")
                vid_status = gr.Textbox(label="स्थिति", lines=2)
                vid_output = gr.Video(label="साफ किया गया वीडियो")
                vid_btn.click(fn=studio_engine.remove_video_precise, inputs=vid_input, outputs=[vid_status, vid_output])

    def switch_workspace(selection):
        return (
            gr.update(visible=selection == "🎬 Link to Video Download"),
            gr.update(visible=selection == "🎵 Link to Audio Download"),
            gr.update(visible=selection == "✨ Remove Image Watermark"),
            gr.update(visible=selection == "🎬 Remove Video Watermark"),
        )
        
    choice.change(
        fn=switch_workspace, 
        inputs=choice, 
        outputs=[tab_video, tab_audio, tab_img_wm, tab_vid_wm]
    )

if __name__ == "__main__":
    print("[🚀] RDX AI Studio लाइट सर्वर लॉन्च हो रहा है...")
    demo.queue().launch(inbrowser=True, share=False, server_name="127.0.0.1", server_port=7860, theme=gr.themes.Soft())