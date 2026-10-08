import os
import sys
import subprocess
import urllib.request
import zipfile

def setup_ffmpeg():
    current_dir = os.getcwd()
    ffmpeg_exe = os.path.join(current_dir, "ffmpeg.exe")
    ffprobe_exe = os.path.join(current_dir, "ffprobe.exe")
    
    if os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe):
        os.environ["PATH"] += os.pathsep + current_dir
        return current_dir
        
    print("[*] FFmpeg project folder mein setup ho raha hai...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(current_dir, "ffmpeg.zip")
    try:
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.namelist():
                if file_info.endswith("ffmpeg.exe") or file_info.endswith("ffprobe.exe"):
                    filename = os.path.basename(file_info)
                    source = zip_ref.open(file_info)
                    target = open(os.path.join(current_dir, filename), "wb")
                    with source, target:
                        import shutil
                        shutil.copyfileobj(source, target)
        if os.path.exists(zip_path):
            os.remove(zip_path)
    except Exception as e:
        print(f"[!] FFmpeg error: {e}")
    os.environ["PATH"] += os.pathsep + current_dir
    return current_dir

FFMPEG_DIR = setup_ffmpeg()

try:
    import yt_dlp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    import yt_dlp

AUDIO_DIR = "downloads/audio"
VIDEO_DIR = "downloads/video"

class MediaDownloader:
    def get_opts(self, url):
        opts = {
            'ffmpeg_location': FFMPEG_DIR,
            'socket_timeout': 60,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Domain ke hisaab se sahi cookie file auto-select karne ka jugad
        cookie_file = None
        if "instagram.com" in url and os.path.exists("www.instagram.com_cookies.txt"):
            cookie_file = "www.instagram.com_cookies.txt"
        elif "hotstar.com" in url and os.path.exists("www.hotstar.com_cookies.txt"):
            cookie_file = "www.hotstar.com_cookies.txt"
        elif "youtube.com" in url or "youtu.be" in url:
            if os.path.exists("www.youtube.com_cookies.txt"):
                cookie_file = "www.youtube.com_cookies.txt"
        elif "naver.com" in url and os.path.exists("creator.tv.naver.com_cookies.txt"):
            cookie_file = "creator.tv.naver.com_cookies.txt"
            
        if cookie_file:
            opts['cookiefile'] = cookie_file
            print(f"[*] Cookie applied for this URL: {cookie_file}")
            
        return opts

    def download_audio(self, url):
        if not url: return "Kripya link daalein!", None
        try:
            base_name = f"Vikas_RDX_Audio_{os.getpid()}"
            raw_out = os.path.join(AUDIO_DIR, base_name)
            final_mp3 = raw_out + ".mp3"
            
            opts = self.get_opts(url)
            opts.update({
                'format': 'bestaudio/best',
                'outtmpl': raw_out,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
                'noplaylist': True,
            })
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                
            if os.path.exists(final_mp3):
                return "👑 Audio successfully downloaded by Vikas RDX!", final_mp3
            return "Audio download fail ho gaya!", None
        except Exception as e:
            return f"[!] Audio Error: {str(e)}", None

    def download_video(self, url):
        if not url: return "Kripya link daalein!", None
        try:
            base_name = f"Vikas_RDX_Video_{os.getpid()}"
            vid_path = os.path.join(VIDEO_DIR, base_name + ".mp4")
            
            opts = self.get_opts(url)
            opts.update({
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(VIDEO_DIR, base_name),
                'merge_output_format': 'mp4',
                'noplaylist': True,
            })
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                
            if os.path.exists(vid_path):
                return "👑 Video successfully downloaded by Vikas RDX!", vid_path
            return "Video download fail ho gaya!", None
        except Exception as e:
            return f"[!] Video Error: {str(e)}", None