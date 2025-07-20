import yt_dlp
import os
from datetime import datetime
from yt_dlp.utils import sanitize_filename

def get_download_path():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    today = datetime.now().strftime("%Y-%m-%d")
    target_dir = os.path.join(downloads, today)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def get_output_file(base_dir, base_name):
    for f in os.listdir(base_dir):
        if f.startswith(base_name) and f.endswith(".mp4"):
            return os.path.join(base_dir, f)
    return None

def main():
    url = input("🔗 Enter YouTube URL: ").strip()
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
        'postprocessors': [
            {'key': 'FFmpegMerger'}
        ],
        'quiet': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    final_path = get_output_file(download_dir, output_base)
    if final_path:
        print(f"\n✅ Download complete:\n{final_path}")
    else:
        print("\n❌ Merge or download failed.")

if __name__ == "__main__":
    main()
