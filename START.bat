@echo off
setlocal
set current_dir=%~dp0
call conda activate "%current_dir%env"
@REM CHANGE SOURCE_FOLDER IN 1_extract_frames_video.py
echo running 1_extract_frames_video.py
python 1_extract_frames_video.py
@REM python 4_bonus.py
@REM python 6_bonus.py
@REM python 7_finalize.py
