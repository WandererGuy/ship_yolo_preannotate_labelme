import os 
import shutil 
import subprocess
from tqdm import tqdm
import time 
output_folder = f"3_AI_label"
os.makedirs(output_folder, exist_ok=True)

main_folder = "2_dest_folder"
for folder_name in tqdm(os.listdir(main_folder), total = len(os.listdir(main_folder))):
        folder_path = os.path.join(main_folder, folder_name)
        image_input_folder = os.path.join(folder_path, 'image')
        json_output_folder = os.path.join(folder_path, 'json')
        os.makedirs(os.path.join(output_folder, folder_name), exist_ok=True) 
        for filename in os.listdir(image_input_folder):
            shutil.copy(os.path.join(image_input_folder, filename), os.path.join(output_folder, folder_name))
        for filename in os.listdir(json_output_folder):
            shutil.copy(os.path.join(json_output_folder, filename), os.path.join(output_folder, folder_name))
