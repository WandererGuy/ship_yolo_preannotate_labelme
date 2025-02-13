@echo off
setlocal
set current_dir=%~dp0
call conda activate "C:\Users\Admin\CODE\work\ship_detect\env_2"
cd Labelme2YOLO
python labelme2yolo.py --json_dir /home/username/labelme_json_dir/
python main.py
