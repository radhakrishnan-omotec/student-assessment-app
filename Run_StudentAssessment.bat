@echo off
title Run Omotec Student Assessment UI Demo

:: Set the path to your Python script
set SCRIPT_PATH=DemoEnhancements.py

:run_streamlit
:: Check if the script exists
if not exist "%SCRIPT_PATH%" (
    echo Python script not found at %SCRIPT_PATH%. Please check the path.
    pause
    exit /b 1
)

:: Run the Streamlit app
echo Starting Streamlit app...
streamlit run "%SCRIPT_PATH%"

:: Keep the terminal open to view any errors
if errorlevel 1 (
    echo An error occurred while running the Streamlit app.
    pause
    exit /b 1
)

pause