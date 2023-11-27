@echo off

set PYTHON_ENVIRONMENT=venv-win

if not exist "%PYTHON_ENVIRONMENT%\" (
    echo creating environment: %PYTHON_ENVIRONMENT% using python -m venv %PYTHON_ENVIRONMENT%
    call python -m venv %PYTHON_ENVIRONMENT%
)

if exist %PYTHON_ENVIRONMENT%\ (
    echo found environment: %PYTHON_ENVIRONMENT%
)

if exist %PYTHON_ENVIRONMENT%\Scripts\activate.bat (
    echo activating environment: %PYTHON_ENVIRONMENT%\Scripts\activate.bat
    %PYTHON_ENVIRONMENT%\Scripts\activate.bat
    python -m pip install --upgrade pip

    if exist requirements.txt (
        echo installing packages using requirements.txt
        pip install -r requirements.txt
    )
)
