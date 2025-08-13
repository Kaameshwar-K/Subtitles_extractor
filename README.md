# Subtitle Extractor
A simple desktop application for Windows to easily extract subtitle tracks from video files.

## Features

* Select a local video file.
* Scans the file to find all available subtitle tracks.
* Displays track information (language, title, codec).
* Extract one or more subtitles and save them as `.srt` or other formats.

## How to Use

### For Users

1. Go to the Releases page.
2. Download the latest Subtitle Extractor `.exe` file.
3. Run the executable. No installation is needed!

### For Developers

This project requires Python and FFmpeg.

1. Clone the repository:
git clone https://github.com/Kaameshwar-K/Subtitles_extractor.git

2. Change into the repository directory:
cd Subtitles_extractor

3. Install Python dependencies:
pip install PyQt6

4. Install FFmpeg: You must have `ffmpeg.exe` and `ffprobe.exe` available. You can download them from the official FFmpeg website. For this script to work easily, place them in the same directory as the Python script.
5. Run the application:
