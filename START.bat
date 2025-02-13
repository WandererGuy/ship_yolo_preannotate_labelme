@echo off
setlocal
set current_dir=%~dp0
call conda activate "%current_dir%env"
@REM CHANGE SOURCE_FOLDER IN 1_extract_frames_video.py
@REM echo running 1_extract_frames_video.py
@REM python 1_extract_frames_video.py
echo running 4_bonus.py
python 4_bonus.py
echo runnning 6_bonus.py
python 6_bonus.py
echo running 7_finalize.py
python 7_finalize.py
