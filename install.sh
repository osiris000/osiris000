#!/bin/sh

type check_command_installed >/dev/null 2>&1 || . osiris.sh

# Comprobación de aplicaciones instaladas.

check_command_installed /usr/bin/python3.9 --version
check_command_installed /usr/bin/pip3
check_command_installed /usr/bin/Osiris-python3-venv
check_command_installed /usr/bin/Osiris-venv-activate
check_command_installed /usr/bin/Osiris-venv-export

check_command_installed /usr/sbin/apache2 -v
check_command_installed /usr/bin/php --version 
#check_command_installed /usr/bin/mariadb 
check_command_installed /usr/bin/ffmpeg -version
check_command_installed /usr/bin/transmission-cli 
check_command_installed /usr/bin/yt-dlp --version
check_command_installed /usr/bin/rustc "--version -v"
#check_command_installed /usr/bin/docker 


check_command_installed /usr/bin/Osiris-install-bardapi 		
check_command_installed /usr/bin/Osiris-force-reinstall-bardapi
check_command_installed /usr/bin/Osiris-upgrade-bardapi


