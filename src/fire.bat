@echo off

set init_dir=%cd%
cd %~dp0

pipenv run python cli\fire\fire_cli.py %*

cd %init_dir%