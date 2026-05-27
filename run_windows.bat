@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

if "%TTN_CONDA_ENV%"=="" (
    set "TTN_CONDA_ENV=ttn-env"
)

where conda >nul 2>nul
if errorlevel 1 (
    echo conda was not found in PATH. Open an Anaconda/Miniconda Prompt or add conda to PATH.
    exit /b 1
)

set "PYTHONPATH=%PROJECT_ROOT%\src"
cd /d "%PROJECT_ROOT%"

for /f "usebackq delims=" %%I in (`conda run -n "%TTN_CONDA_ENV%" python -c "import os; print(os.environ['CONDA_PREFIX'])"`) do (
    set "CONDA_ENV_PREFIX=%%I"
)
set "PROJ_LIB=%CONDA_ENV_PREFIX%\Library\share\proj"
set "PROJ_DATA=%PROJ_LIB%"

conda run -n "%TTN_CONDA_ENV%" python -m thucthengay %*
exit /b %ERRORLEVEL%
