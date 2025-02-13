import os 
import shutil
# from 1_extract_frames_video import find_all_image_paths, find_keep_folder, OUTPUT_FOLDER
import yaml


# with open('map.yaml', 'r') as file:
#     map_data = yaml.load(file, Loader=yaml.FullLoader)
#     if map_data is None:
#         map_data = {}

# ###### keep unique folder only , 1 video have 1 folder ##########
# for folder in os.listdir(OUTPUT_FOLDER):
#     if folder not in find_keep_folder(map_data):
#         shutil.rmtree(os.path.join(OUTPUT_FOLDER, folder))


########################################################################

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

folder_path = r"C:\Users\Admin\Downloads\Dataset\Dataset\Image"
ls = find_all_image_paths(folder_path)
save_image_path = r"2_Nam_images"
os.makedirs(save_image_path, exist_ok=True)
for index, image_path in enumerate(ls):
    extension = "." + image_path.split(".")[-1]
    shutil.copy(image_path, os.path.join(save_image_path, str(index) + extension))

#########################################################################
# save_image_path = r"C:\Users\Admin\CODE\work\ship_detect\3_all_images"
# os.makedirs(save_image_path, exist_ok=True)
# image_ls = set()
# folder_path = r"C:\Users\Admin\CODE\work\ship_detect\2_images"
# folder_path_2 = r"C:\Users\Admin\CODE\work\ship_detect\1_extracted_frames"
# image_ls.update(find_all_image_paths(folder_path))
# image_ls.update(find_all_image_paths(folder_path_2))
# for index, image_path in enumerate(image_ls):
#     extension = "." + image_path.split(".")[-1]
#     shutil.copy(image_path, os.path.join(save_image_path, str(index) + extension))
