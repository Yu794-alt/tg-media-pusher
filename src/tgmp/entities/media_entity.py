
from pathlib import Path

class Media:
    def __init__(self, folder_path: str, extensions: list = None):
        self.folder_path = Path(folder_path)        
        self.extensions = extensions or [".mp4", ".avi", ".mov", ".mkv", ".webm", ".mp3", ".wav"]

        if not self.folder_path.exists():
            raise FileNotFoundError(f"Папка '{self.folder_path}' не существует")
        if not self.folder_path.is_dir():
            raise NotADirectoryError(f"'{self.folder_path}' не является папкой")
        
    def get_media_files(self):
        videos = []
        for ext in self.extensions:
            videos.extend(self.folder_path.glob(f"*{ext}"))
        return videos