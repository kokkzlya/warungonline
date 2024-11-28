# Simple Hack Tutorial

## Prerequisites
1. pyenv
2. poetry
3. Python 3.12

## How to install pyenv
1. Buka powershell
1. Jalankan:
    ```
    Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
    ```
1. Lihat list Python yang tersedia:
    ```
    pyenv install -l
    ```
1. Install Python 3.12:
    ```
    pyenv install 3.12.7
    ```
1. Set Python 3.12.7 sebagai python global:
    ```
    pyenv global 3.12.7
    ```

## How to install poetry
1. Open powershell
1. Run
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    ```
1. Set environment variable, add to PATH:
    ```
    %USERPROFILE%\AppData\Roaming\pypoetry\venv\Scripts
    ```
1. Reopen the powershell, then check `poetry` with:
    ```
    poetry --version
    ```

## How to run project
1. Install dependency first
    ```
    poetry install
    ```
1. Run this command:
    ```
    poetry run python -m app
    ```
1. Open in browser:
    ```
    http://localhost:5000
    ```
