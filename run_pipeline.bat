@echo off
cd /d C:\Users\PC\Documents\basketball-data-platform
.venv\Scripts\python.exe src\pipeline.py >> logs\pipeline.log 2>&1
