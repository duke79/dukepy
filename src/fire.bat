@echo off

set init_dir=%cd%
cd %~dp0

python cli\fire\fire_cli.py %*

REM https://stackoverflow.com/a/1420981/973425
python cli\fire\fire_cli.py %INPUT% 2>&1

cd %init_dir%