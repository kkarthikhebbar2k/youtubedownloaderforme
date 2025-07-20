# youtubedownloaderforme

**Helps download YouTube videos to your system**

## Features

- Download videos from YouTube to your local machine.
- Supports both a standalone executable and the original Python script.
- Saves videos to the `Downloads/<today's date>/` directory automatically.

## Prerequisites

- **FFmpeg** must be installed and added to your system's environment path.
  - Download the latest Windows builds from: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)[1]
  - Follow instructions to extract and add the `bin` directory to your system's `PATH` variable.
  - This is necessary for video conversion features to work correctly.

## Usage

### 1. Executable

- Run the executable located at `dist/youtubeDownloader.exe`.
- Paste the YouTube link when prompted.
- The video will be saved to `Downloads/<today's date>/` (replacing with the current date).

### 2. Python Script

- Run the script:
python youtubeDownloader.py
- Paste the YouTube link when prompted.
- Choose the video format, or press Enter to download in the highest resolution.
- The video will be saved to `Downloads/<today's date>/` (replacing with the current date).

## Known Issues

- The binary may **crash when downloading videos** due to a converter issue in the `yt_dlp` library.

## Notes

- For best results, use the Python script if you encounter errors with the executable.
- Ensure all dependencies (such as `yt_dlp`) are installed and up to date when running the script directly.
