#!/bin/sh

type check_command_installed >/dev/null 2>&1 || . osiris.sh

# Comprobación de aplicaciones instaladas.

check_command_installed /usr/bin/python3 --version
check_command_installed /usr/sbin/apache2 -v
check_command_installed /usr/bin/php --version 
check_command_installed /usr/bin/mariadb 
check_command_installed /usr/bin/ffmpeg -version
check_command_installed /usr/bin/transmission-cli 
check_command_installed /usr/bin/youtube-dl 
check_command_installed /usr/bin/rustc "--version -v"
check_command_installed /usr/bin/pip3
check_command_installed /usr/bin/docker 
check_command_installed /usr/bin/sublime-text

