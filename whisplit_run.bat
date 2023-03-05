@echo off

set ENV_NAME=whisplit
set REQ_FILE=requirements.txt
set SCRIPT=main.py

:: Check if environment exists
conda env list | findstr /i /c:"%ENV_NAME%" >nul
if %errorlevel% equ 0 (
    echo Environment %ENV_NAME% already exists
) else (
    echo Creating environment %ENV_NAME%
    conda create --name %ENV_NAME% --file %REQ_FILE%
)

:: Activate environment and run script
call activate %ENV_NAME%
streamlit run %SCRIPT%