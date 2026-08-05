@REM @echo off
@REM cd /d "D:\Hakim\Hakim_Code\BA_study_management"
@REM call .venv\Scripts\activate.bat
@REM python manage.py runserver
@REM pause

@echo off
REM Runs the Django app from inside WSL using gunicorn

wsl bash -c "cd /mnt/d/Hakim/Hakim_Code/BA_study_management && source .venv-wsl/bin/activate && gunicorn BA_study_management.wsgi:application --bind 0.0.0.0:8000"

pause