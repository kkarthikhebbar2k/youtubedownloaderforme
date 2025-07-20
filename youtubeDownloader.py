import yt_dlp
import os
from datetime import datetime

def get_download_path():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    today = datetime.now().strftime("%Y-%m-%d")
    target_dir = os.path.join(downloads, today)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir

def get_formats(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get('formats', [])

def display_formats(formats):
    print("Format ID | Res   | Ext | Size   | Type    | Note")
    print("-" * 60)

    for f in formats:
        format_id = f.get('format_id')
        ext = f.get('ext')
        resolution = f.get('resolution') or f.get('height') or '?'
        note = f.get('format_note', '')
        filesize = f.get('filesize') or f.get('filesize_approx') or 0
        size_mb = round(filesize / (1024 * 1024), 2) if filesize else '?'

        has_audio = f.get('acodec') != 'none'
        has_video = f.get('vcodec') != 'none'

        if has_video or has_audio:
            type_tag = ''
            if has_video and has_audio:
                type_tag = 'A+V'
            elif has_video:
                type_tag = 'V-only'
            elif has_audio:
                type_tag = 'A-only'

            print(f"{format_id:9} | {resolution:5} | {ext:<3} | {size_mb:>6}MB | {type_tag:<7} | {note}")

def main():
    url = input("Enter YouTube URL: ").strip()
    print("\n🔍 Fetching available formats...\n")

    formats = get_formats(url)
    if not formats:
        print("❌ No formats found.")
        return

    display_formats(formats)

    choice = input("\n🎯 Enter format code (e.g., 137+140), or press Enter for best 1080p: ").strip()

    download_dir = get_download_path()
    timestamp = datetime.now().strftime("%H%M%S")
    output_template = os.path.join(download_dir, f'%(title)s_{timestamp}.%(ext)s')

    if not choice:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'postprocessors': [
                {       
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',  # Convert to mp4
                },
            ],
        }

    else:
        ydl_opts = {
            'format': choice,
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
        }

    print(f"\n📥 Downloading to: {download_dir}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("\n✅ Download complete.")

if __name__ == "__main__":
    main()
