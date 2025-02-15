import os 
import shutil
import yaml

########################################################################
def find_all_image_paths(folder_path: str) -> list[str]:
    # List of common video file extensions
    video_extensions = ['.jpg', '.png', '.jpeg']
    video_paths = []
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_paths.append(os.path.join(root, file))
    return video_paths

if __name__ == "__main__":
    folder_path = r"C:\Users\Admin\Downloads\Dataset\Dataset\Image"
    ls = find_all_image_paths(folder_path)
    save_image_path = r"2_Nam_images"
    os.makedirs(save_image_path, exist_ok=True)
    for index, image_path in enumerate(ls):
        extension = "." + image_path.split(".")[-1]
        shutil.copy(image_path, os.path.join(save_image_path, str(index) + extension))

