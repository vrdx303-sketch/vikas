import os
import sys

# --- SELF-CONTAINED PROJECT ROUTING (No heavy external load) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["HF_HOME"] = os.path.join(BASE_DIR, "model", "huggingface")
os.environ["TORCH_HOME"] = os.path.join(BASE_DIR, "model", "torch")

import gradio as gr
import cv2
import numpy as np
from PIL import Image

# Required folders inside the project itself
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
WATERMARK_DIR = os.path.join(DOWNLOADS_DIR, "watermark_cleaned")
os.makedirs(WATERMARK_DIR, exist_ok=True)

# Simple & Effective Watermark / Object Remover Logic for Photos and Videos
class WatermarkRemoverEngine:
    def remove_image_watermark(self, input_image):
        if input_image is None:
            return "Kripya pehle photo upload karein, laadle!", None
        try:
            # Convert to OpenCV format
            img = np.array(input_image)
            img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            # Basic inpainting technique to remove overlay/watermark areas
            # Creating a simple mask (Thresholding to find bright/text overlays if applicable, or general smoothing)
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)
            
            # Inpaint to remove watermark
            result_cv = cv2.inpaint(img_cv, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
            result_rgb = cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB)
            
            output_img = Image.fromarray(result_rgb)
            out_path = os.path.join(WATERMARK_DIR, f"cleaned_image_{os.getpid()}.png")
            output_img.save(out_path)
            
            return "👑 Watermark successfully removed from photo!", out_path
        except Exception as e:
            return f"[!] Image Watermark Error: {str(e)}", None

    def remove_video_watermark(self, input_video_path):
        if not input_video_path:
            return "Kripya pehle video upload karein, laadle!", None
        try:
            cap = cv2.VideoCapture(input_video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            
            out_path = os.path.join(WATERMARK_DIR, f"cleaned_video_{os.getpid()}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                # Frame-by-frame processing for clean output
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
                cleaned_frame = cv2.inpaint(frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
                out.write(cleaned_frame)
                
            cap.release()
            out.release()
            
            if os.path.exists(out_path):
                return "👑 Watermark successfully removed from video!", out_path
            return "Video processing fail ho gayi!", None
        except Exception as e:
            return f"[!] Video Watermark Error: {str(e)}", None

watermark_engine = WatermarkRemoverEngine()

# Gradio Interface with RDX AI Studio Branding
with gr.Blocks(title="RDX AI Studio") as demo:
    gr.Markdown("# 🚀 RDX AI Studio - Portable Master Edition")
    gr.Markdown("Vikas RDX ka Official Studio | Self-Contained Watermark Remover & AI Suite")
    
    with gr.Row():
        with gr.Column(scale=1, min_width=280):
            gr.Markdown("### 🛠️ Control Center")
            choice = gr.Radio(
                [
                    "✨ Remove Image Watermark", 
                    "🎬 Remove Video Watermark"
                ], 
                label="Feature Select Karein", 
                value="✨ Remove Image Watermark"
            )
            gr.Markdown("---")
            gr.Markdown("**Status:** Portable Mode Active 🟢\n**Watermark:** Vikas RDX 👑")
            
        with gr.Column(scale=3):
            # 1. Image Watermark Removal Tab
            with gr.Group(visible=True) as tab_img_wm:
                gr.Markdown("### ✨ Photo se Watermark Hatayein")
                img_input = gr.Image(type="pil", label="Apni Photo Yahan Dalein")
                img_btn = gr.Button("Remove Watermark from Photo", variant="primary")
                img_status = gr.Textbox(label="Status", lines=2)
                img_output = gr.Image(label="Cleaned Image Output")
                img_btn.click(fn=watermark_engine.remove_image_watermark, inputs=img_input, outputs=[img_status, img_output])

            # 2. Video Watermark Removal Tab
            with gr.Group(visible=False) as tab_vid_wm:
                gr.Markdown("### 🎬 Video se Watermark Hatayein")
                vid_input = gr.Video(label="Apna Video Yahan Dalein")
                vid_btn = gr.Button("Remove Watermark from Video", variant="primary")
                vid_status = gr.Textbox(label="Status", lines=2)
                vid_output = gr.Video(label="Cleaned Video Output")
                vid_btn.click(fn=watermark_engine.remove_video_watermark, inputs=vid_input, outputs=[vid_status, vid_output])

    def switch_workspace(selection):
        return (
            gr.update(visible=selection == "✨ Remove Image Watermark"),
            gr.update(visible=selection == "🎬 Remove Video Watermark"),
        )
        
    choice.change(
        fn=switch_workspace, 
        inputs=choice, 
        outputs=[tab_img_wm, tab_vid_wm]
    )

if __name__ == "__main__":
    print("[🚀] RDX Portable Studio launch ho raha hai...")
    demo.queue().launch(inbrowser=True, theme=gr.themes.Soft())