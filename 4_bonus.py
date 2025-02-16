import os 
import shutil 
import subprocess
from tqdm import tqdm
import time 
import yaml
for folder_path in ["1_extracted_frames", "2_dest_folder", "3_AI_label"]:
    if os.path.exists(folder_path):
        # Remove the folder and its contents
        shutil.rmtree(folder_path)
        print(f"The folder {folder_path} has been removed.")

# Load the YAML file
with open("config.yaml", "r") as file:
    data = yaml.safe_load(file)

FOLDER_FOR_INFER =  data["FOLDER_FOR_INFER"]
source_folder = FOLDER_FOR_INFER
dest_folder = "2_dest_folder"
os.makedirs(dest_folder, exist_ok=True)
for folder_name in tqdm(os.listdir(source_folder), total = len(os.listdir(source_folder))):
    os.rename(os.path.join(source_folder, folder_name), (os.path.join(source_folder, folder_name)).replace(' ', '_'))


for folder_name in tqdm(os.listdir(source_folder), total = len(os.listdir(source_folder))):
    folder_path = os.path.join(source_folder, folder_name)
    image_input_folder = folder_path
    txt_output_folder = os.path.join(dest_folder, folder_name, 'txt')
    image_output_folder = os.path.join(dest_folder, folder_name, 'image')
    os.makedirs(txt_output_folder, exist_ok=True)
    os.makedirs(image_output_folder, exist_ok=True)
    command = ["python", 
            "3_run_yolo.py",
            "--image_input_folder",
            image_input_folder,
            "--txt_output_folder",
            txt_output_folder,
            "--image_output_folder",
            image_output_folder
            ]
    cm = " ".join(command)
    print (cm)
    with subprocess.Popen(command, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            text=True) as process:
        for line in process.stdout:
            print(line, end='')

