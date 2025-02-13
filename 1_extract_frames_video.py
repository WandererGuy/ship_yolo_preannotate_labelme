'''
script collect up to max_frame_count number of frame per video 
'''
import cv2
import os 
import uuid
import shutil 
import os
import time 
import yaml
import time 
from unidecode import unidecode

from tqdm import tqdm



map_video_save = {}
# Read from config.yaml
# Check if the folder exists
for folder_path in ["1_extracted_frames", "2_dest_folder", "3_AI_label"]:
    if os.path.exists(folder_path):
        # Remove the folder and its contents
        shutil.rmtree(folder_path)
        print(f"The folder {folder_path} has been removed.")

OUTPUT_FOLDER = r".\1_extracted_frames"
def find_all_video_paths(folder_path):
    # List of common video file extensions
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
    video_paths = []
    
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_paths.append(os.path.join(root, file))
    
    return video_paths

def find_all_image_paths(folder_path):
    # List of common video file extensions
    video_extensions = ['.jpg', '.png', '.jpeg']
    video_paths = []
    
    # Walk through the folder to find video files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_paths.append(os.path.join(root, file))
    
    return video_paths

def find_keep_folder(map_data):
    keep_folder = []
    for key, value in map_data.items():
            keep_folder.append(value)
    return keep_folder

if __name__ == '__main__':
    """
    given a folder , get all videos in the folder/subfolder/...
    extract frame per video
    """
    import yaml

    # Load the YAML file
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)
    max_frame_count = data["MAX_FRAME_COUNT"]
    # folder_path = r"C:\Users\Admin\Downloads\Dataset 1\Dataset 1"
    folder_path = data["SOURCE_FOLDER_HAVE_VIDEOS"]
    ls_video_path = find_all_video_paths(folder_path)

    for video_path in tqdm(ls_video_path, total=len(ls_video_path)):
            try:
                with open('map.yaml', 'r') as file:
                    map_data = yaml.load(file, Loader=yaml.FullLoader)
                    if map_data is None:
                        map_data = {}
            except:
                map_data = {}
                

            video_capture = cv2.VideoCapture(video_path)
            total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            t = unidecode(os.path.basename(video_path).split(".")[0]).replace('"', '').replace("'", '')
            save_video_folder_name = os.path.basename(os.path.dirname(video_path)) + '____' + str(t)
            # save_video_folder_name = str(uuid.uuid4())

            map_data[video_path] = save_video_folder_name
            map_video_save[video_path] = save_video_folder_name
            save_video_folder = os.path.join(OUTPUT_FOLDER, save_video_folder_name)
            os.makedirs(save_video_folder, exist_ok=True)
            # Check if video is opened correctly
            if not video_capture.isOpened():
                print("Error: Could not open video.")
                exit()
            num_capture_rate = int(total_frames / max_frame_count)
            print (total_frames)
        
            if num_capture_rate == 0:
                num_capture_rate = 1
            print ( "NUM CAPTURE RATE: " + str(num_capture_rate))
            frame_count = 0
            extracted_frame_count = 0

            while True:
                # Read the next frame
                ret, frame = video_capture.read()

                if not ret:
                    break  # Exit loop when video ends

                if frame_count % num_capture_rate == 0:  # Capture every 4th frame
                    # Save the frame as an image
                    cv2.imwrite(os.path.join(save_video_folder, f'{extracted_frame_count}.jpg'), frame)
                    print(f"Image extracted and saved as '{extracted_frame_count}.jpg'.")
                    extracted_frame_count += 1

                frame_count += 1
                if extracted_frame_count >= max_frame_count:
                    break
            # Release the video capture object
            video_capture.release()

            with open('map.yaml', 'w') as file:
                yaml.dump(map_data, file)
                time.sleep(2)




