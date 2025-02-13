@echo off
setlocal
set current_dir=%~dp0
call conda activate "%current_dir%env"
cd assist_label
cd Labelme2YOLO
python labelme2yolo.py --json_dir /home/username/labelme_json_dir/
python main.py
cd ..
