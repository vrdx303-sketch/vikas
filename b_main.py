import gradio as gr
from downloader import MediaDownloader
from splitter import AudioSplitter

downloader = MediaDownloader()
splitter = AudioSplitter()

with gr.Blocks() as demo:
    gr.Markdown("# 🚀 RDX AI Studio - Master Modular Edition")
    gr.Markdown("Vikas RDX ka Official Studio | Clean Architecture & 100% Working Tools")
    
    with gr.Row():
        with gr.Column(scale=1, min_width=280):
            gr.Markdown("### 🛠️ Control Center")
            choice = gr.Radio(
                ["🎬 Link to Video Download", "🎵 Link to Audio Download", "✂️ Vocal & Background Separator"], 
                label="Feature Select Karein", 
                value="🎬 Link to Video Download"
            )
            gr.Markdown("---")
            gr.Markdown("**Status:** System Ready 🟢\n**Watermark:** Vikas RDX 👑")
            
        with gr.Column(scale=3):
            with gr.Group(visible=True) as tab_video:
                gr.Markdown("### 🎬 Link to Video Download")
                v_url = gr.Textbox(label="Video Link Dalein", placeholder="https://...")
                v_btn = gr.Button("Download Video", variant="primary")
                v_status = gr.Textbox(label="Status", lines=2)
                v_file = gr.File(label="Downloaded Video File (.mp4)")
                v_btn.click(fn=downloader.download_video, inputs=v_url, outputs=[v_status, v_file])

            with gr.Group(visible=False) as tab_audio:
                gr.Markdown("### 🎵 Link to Audio Download")
                a_url = gr.Textbox(label="Audio/Video Link Dalein", placeholder="https://...")
                a_btn = gr.Button("Download Audio (MP3)", variant="primary")
                a_status = gr.Textbox(label="Status", lines=2)
                a_audio = gr.Audio(label="Downloaded MP3 File (.mp3)")
                a_btn.click(fn=downloader.download_audio, inputs=a_url, outputs=[a_status, a_audio])

            with gr.Group(visible=False) as tab_stems:
                gr.Markdown("### ✂️ Vocal & Background Separator")
                s_file = gr.File(label="Audio File Upload Karein")
                s_btn = gr.Button("Separate Vocals", variant="primary")
                s_status = gr.Textbox(label="Status", lines=2)
                s_vocals = gr.Audio(label="Human Vocals")
                s_bg = gr.Audio(label="Background Instrumental")
                s_btn.click(fn=splitter.separate, inputs=s_file, outputs=[s_status, s_vocals, s_bg])

    def switch_workspace(selection):
        return (
            gr.update(visible=selection == "🎬 Link to Video Download"),
            gr.update(visible=selection == "🎵 Link to Audio Download"),
            gr.update(visible=selection == "✂️ Vocal & Background Separator"),
        )
        
    choice.change(fn=switch_workspace, inputs=choice, outputs=[tab_video, tab_audio, tab_stems])

if __name__ == "__main__":
    print("[🚀] RDX Master Studio launch ho raha hai...")
    demo.launch(inbrowser=True, theme=gr.themes.Soft())