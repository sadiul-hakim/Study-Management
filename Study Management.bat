@REM Windows Command
@REM @echo off
@REM cd /d "D:\Hakim\Hakim_Code\BA_study_management"
@REM call .venv\Scripts\activate.bat
@REM python manage.py runserver
@REM pause

@REM WSL Command
@echo off
REM Kill anything already using port 8000 inside WSL, then start gunicorn

wsl bash -c "fuser -k 8000/tcp 2>/dev/null; cd /mnt/d/Hakim/Hakim_Code/BA_study_management && source .venv-wsl/bin/activate && exec gunicorn BA_study_management.wsgi:application --bind 0.0.0.0:8000 --workers 1 --reload --timeout 120"

pause