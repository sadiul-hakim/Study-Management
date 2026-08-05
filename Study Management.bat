@echo off
cd /d "D:\Hakim\Hakim_Code\BA_study_management"
call .venv\Scripts\activate.bat
python manage.py runserver
pause