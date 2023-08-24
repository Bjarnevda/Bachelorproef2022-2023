@echo off
setlocal

for %%i in ("%~dp0.") do set "SCRIPTPATH=%%~fi"


set "ROLESPATH=%SCRIPTPATH%\ansible\roles"

rd /s /q %ROLESPATH%
"C:\Program Files\Git\bin\bash.exe" --login -i -c "git clone https://github.com/geerlingguy/ansible-role-docker.git \"%ROLESPATH%\geerlingguy.docker""
"C:\Program Files\Git\bin\bash.exe" --login -i -c "git clone https://github.com/geerlingguy/ansible-role-pip.git \"%ROLESPATH%\geerlingguy.pip""

vagrant destroy --force
vagrant up
vagrant reload
vagrant ssh -c "docker restart $(docker ps -a -q)"
vagrant provision
pause

endlocal