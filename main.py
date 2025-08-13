import sys
import json
import subprocess
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QListWidget, QListWidgetItem, QMessageBox, QAbstractItemView
)
from PyQt6.QtCore import Qt

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).parent.resolve()

    return Path(base_path) / relative_path

class SubtitleExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Local Video Subtitle Extractor")
        self.resize(600, 400)

        # Get paths to the bundled ffmpeg and ffprobe executables
        self.ffmpeg_path = get_resource_path("ffmpeg.exe")
        self.ffprobe_path = get_resource_path("ffprobe.exe")

        self.video_path = None
        self.tracks = []

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Widgets ---
        self.select_file_btn = QPushButton("Select Video File")
        self.select_file_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_file_btn)

        self.file_label = QLabel("No file selected. FFmpeg/FFprobe required.")
        self.file_label.setWordWrap(True)
        layout.addWidget(self.file_label)

        self.scan_btn = QPushButton("Scan for Subtitle Tracks")
        self.scan_btn.setEnabled(False)
        self.scan_btn.clicked.connect(self.scan_subtitles)
        layout.addWidget(self.scan_btn)

        self.subtitle_list = QListWidget()
        self.subtitle_list.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        layout.addWidget(self.subtitle_list)

        self.extract_btn = QPushButton("Extract Selected Subtitles")
        self.extract_btn.setEnabled(False)
        self.extract_btn.clicked.connect(self.extract_subtitles)
        layout.addWidget(self.extract_btn)

        # Check if ffmpeg/ffprobe exist at startup
        self.check_ffmpeg_presence()

    def check_ffmpeg_presence(self):
        """Checks if ffmpeg and ffprobe are found and updates UI."""
        if not self.ffmpeg_path.exists() or not self.ffprobe_path.exists():
            QMessageBox.critical(
                self, "Missing Dependencies",
                f"ffmpeg.exe or ffprobe.exe not found!\n"
                f"Please make sure they are in the same folder as the application.\n"
                f"Expected ffprobe at: {self.ffprobe_path}"
            )
            self.select_file_btn.setEnabled(False)
            self.scan_btn.setEnabled(False)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mkv *.mp4 *.avi *.mov);;All Files (*)")
        if file_path:
            self.video_path = file_path
            self.file_label.setText(f"Selected: {Path(file_path).name}")
            self.scan_btn.setEnabled(True)
            self.subtitle_list.clear()
            self.extract_btn.setEnabled(False)

    def scan_subtitles(self):
        if not self.video_path:
            return
        
        self.tracks = self.get_subtitle_tracks(self.video_path)
        self.subtitle_list.clear()

        if not self.tracks:
            QMessageBox.warning(self, "No Subtitles", "No subtitle tracks were found in this video file.")
            self.extract_btn.setEnabled(False)
        else:
            for t in self.tracks:
                lang = t.get('language', 'unknown')
                codec = t.get('codec', 'unknown')
                idx = t.get('index', -1)
                title = t.get('title', 'No Title')
                
                item_text = f"Track {idx}: {lang.upper()} ({title}) - Codec: {codec}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, t) # Store the whole track dict in the item
                self.subtitle_list.addItem(item)
            self.extract_btn.setEnabled(True)

    def get_subtitle_tracks(self, video_path):
        cmd = [
            str(self.ffprobe_path),
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            video_path
        ]
        try:
            # Set CREATE_NO_WINDOW flag for Windows to prevent console popup
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', startupinfo=startupinfo)
            if result.returncode != 0:
                QMessageBox.critical(self, "ffprobe Error", f"ffprobe failed to scan the file.\nError: {result.stderr}")
                return []

            info = json.loads(result.stdout)
            subtitle_tracks = []
            for stream in info.get("streams", []):
                if stream.get("codec_type") == "subtitle":
                    track_info = {
                        "index": stream.get("index"),
                        "language": stream.get("tags", {}).get("language", "und"),
                        "title": stream.get("tags", {}).get("title"),
                        "codec": stream.get("codec_name")
                    }
                    subtitle_tracks.append(track_info)
            return subtitle_tracks
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"Could not find ffprobe at {self.ffprobe_path}")
            return []
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Failed to parse video information from ffprobe.")
            return []


    def extract_subtitles(self):
        selected_items = self.subtitle_list.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Select Tracks", "Please select at least one subtitle track to extract.")
            return

        video_file_path = Path(self.video_path)

        for item in selected_items:
            track = item.data(Qt.ItemDataRole.UserRole)
            if track:
                track_index = track['index']
                lang = track['language']
                
                # Determine file extension
                codec = track.get('codec', 'sub')
                ext = "srt" if codec in ["subrip", "srt"] else "ass" if codec in ["ass"] else codec
                
                default_filename = f"{video_file_path.stem}_{track_index}_{lang}.{ext}"
                
                save_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Subtitle File",
                    str(video_file_path.parent / default_filename),
                    filter=f"{ext.upper()} Files (*.{ext});;All Files (*)"
                )
                
                if save_path:
                    self.extract_subtitle(self.video_path, track_index, save_path)
                    QMessageBox.information(self, "Success", f"Subtitle saved successfully to:\n{save_path}")

    def extract_subtitle(self, video_path, track_index, output_path):
        cmd = [
            str(self.ffmpeg_path),
            "-i", video_path,
            "-map", f"0:s:{track_index - 1}", # Subtitle stream indexes might need adjustment
            "-c", "copy",
            output_path,
            "-y" # Overwrite output file if it exists
        ]
        # Adjust map for absolute track index if needed
        cmd_absolute = [
            str(self.ffmpeg_path),
            "-i", video_path,
            "-map", f"0:{track_index}",
            "-c", "copy",
            output_path,
            "-y"
        ]

        try:
            # Set CREATE_NO_WINDOW flag for Windows to prevent console popup
            startupinfo = None
            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Run ffmpeg
            result = subprocess.run(cmd_absolute, check=True, capture_output=True, text=True, encoding='utf-8', startupinfo=startupinfo)
        
        except FileNotFoundError:
             QMessageBox.critical(self, "Error", f"Could not find ffmpeg at {self.ffmpeg_path}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "ffmpeg Error", f"Failed to extract subtitle.\nffmpeg stderr:\n{e.stderr}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SubtitleExtractorApp()
    window.show()
    sys.exit(app.exec())
