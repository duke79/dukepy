@echo off

set init_dir=%cd%
cd %~dp0

python cli\fire\fire_cli.py %*

:loop

set /p INPUT=

REM https://stackoverflow.com/a/1420981/973425
python cli\fire\fire_cli.py %INPUT% 2>&1

goto loop

cd %init_dir%