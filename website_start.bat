@echo off
echo Starting fronted app...

REM Replace "app.exe" with the actual name of your backend app executable
cd frontend/sign-recognition-project
call npm run dev

echo Backend app started.