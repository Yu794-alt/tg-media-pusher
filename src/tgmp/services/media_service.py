
from entities.media_entity import Media


def get_video():
    folder = Media("D:\\tv", extensions=[".mp4", ".webm", ".avi"])
    videos = folder.get_media_files()
    print(videos)
    return {"message": "Video folder retrieved successfully", "folder_path": str(folder.folder_path)}
