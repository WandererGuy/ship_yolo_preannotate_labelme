import os 
import shutil 
import subprocess
from tqdm import tqdm
import time 


main_folder = "2_dest_folder"
for folder_name in tqdm(os.listdir(main_folder), total = len(os.listdir(main_folder))):
        folder_path = os.path.join(main_folder, folder_name)
        image_input_folder = os.path.join(folder_path, 'image')
        txt_input_folder = os.path.join(folder_path, 'txt')
        json_output_folder = os.path.join(folder_path, 'json')
        os.makedirs(json_output_folder, exist_ok=True)
        command = ["python", 
                "5_coco2json.py",
                "--image_input_folder",
                image_input_folder,
                "--txt_input_folder",
                txt_input_folder,
                "--json_output_folder",
                json_output_folder
                ]
        cm = " ".join(command)
        print (cm)
        with subprocess.Popen(command, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True) as process:
                for line in process.stdout:
                        print(line, end='')
