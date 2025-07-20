import yt_dlp
import os
from datetime import datetime
from yt_dlp.utils import sanitize_filename
import shutil
import sys

def check_ffmpeg():
    """Warn the user if FFmpeg is missing."""
    if not shutil.which('ffmpeg'):
        print("⚠️  Warning: FFmpeg is not installed or not in PATH.")
        print("    Video merging/conversion may fail or only partial files will be downloaded.")
        print("    Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/")
        print("")

def get_download_path():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    today = datetime.now().strftime("%Y-%m-%d")
    target_dir = os.path.join(downloads, today)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def get_output_file(base_dir, base_name):
    """Look for common video extensions."""
    for ext in ('.mp4', '.webm', '.mkv'):
        fname = base_name + ext
        full_path = os.path.join(base_dir, fname)
        if os.path.isfile(full_path):
            return full_path
    # Fallback: Try any file starting with base_name and known extensions
    for f in os.listdir(base_dir):
        if f.startswith(base_name) and f.lower().endswith(('.mp4', '.webm', '.mkv')):
            return os.path.join(base_dir, f)
    return None

def main():
    check_ffmpeg()
    try:
        url = input("🔗 Enter YouTube URL: ").strip()
        if not url:
            print("No URL provided.")
            sys.exit(1)
        download_dir = get_download_path()
        timestamp = datetime.now().strftime("%H%M%S")

        # Get video metadata
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = sanitize_filename(info.get("title", "video"), restricted=True)

        output_base = f"{title}_{timestamp}"
        output_template = os.path.join(download_dir, output_base + ".%(ext)s")

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': {'default': output_template},
            'merge_output_format': 'mp4',
            'quiet': False,  # Show progress and info
        }

        # Download the video
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"❌ Error during download: {e}")
            sys.exit(1)

        final_path = get_output_file(download_dir, output_base)
        if final_path:
            print(f"\n✅ Download complete:\n{final_path}")
        else:
            print("\n❌ Merge or download failed. Check above messages and your output folder.")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
