# 🎬 Subtitle Extractor GUI

A simple desktop application for Windows to easily extract subtitle tracks from video files (MKV, MP4, etc.).


## ✨ Features

* Select a local video file.
* Scans the file to find all available subtitle tracks.
* Displays track information (language, title, codec).
* Extract one or more subtitles and save them as `.srt`, `.ass`, or other formats.

## 🚀 How to Use (for Users)

1.  Go to the [**Releases**](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/releases) page.
2.  Download the latest `Subtitle.Extractor.exe` file.
3.  Run the executable. No installation is needed!

## 💻 How to Run from Source (for Developers)

This project requires Python and FFmpeg.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
    cd YOUR_REPOSITORY
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install PyQt6
    ```

3.  **Install FFmpeg:**
    You must have `ffmpeg.exe` and `ffprobe.exe` available. You can download them from the [official FFmpeg website](https://ffmpeg.org/download.html). For this script to work easily, place them in the same directory as the Python script.

4.  **Run the application:**
    ```bash
    python your_script_name.py
    ````

**Important:** Remember to replace `YOUR_USERNAME`, `YOUR_REPOSITORY`, and `your_script_name.py` with your actual details.

---

### **Step 5: Upload Your Project Files to GitHub**

Now, let's upload your prepared files (`.gitignore`, `README.md`, and your Python script).

1.  Install Git if you haven't already.
2.  Open a terminal or command prompt in your project folder.
3.  Run these commands one by one:

    ```bash
    # Initialize a new Git repository
    git init

    # Add all files (respecting the .gitignore)
    git add .

    # Make your first commit (a snapshot of your code)
    git commit -m "Initial commit: Add application source code and README"

    # Link your local repository to the one on GitHub
    git remote add origin [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)

    # Push your code to GitHub
    git push -u origin master
    ```

---

### **Step 6: Create a Release for Your `.exe` File**

This is the final and most important step for distributing your app.

1.  On your GitHub repository page, click on the **"Releases"** link on the right-hand side.
2.  Click **"Create a new release"** or "Draft a new release".
3.  Give it a version number for the tag, like `v1.0`.
4.  Give the release a title, like `Version 1.0`.
5.  In the description box, you can write some notes about the release.
6.  In the **"Attach binaries"** box, drag and drop your `Subtitle Extractor.exe` file (the one from your `dist` folder).
7.  Click **"Publish release"**.

Now, users can go to your repository, click on "Releases," and download the ready-to-use `.exe` file, while developers can see the clean source code in the main view.
