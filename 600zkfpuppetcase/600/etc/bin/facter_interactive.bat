@echo off
echo Running Facter on demand ...
cd "%~dp0"
call facter.bat --puppet %*
PAUSE
