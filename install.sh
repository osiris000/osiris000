#!/bin/sh

type check_command_installed >/dev/null 2>&1 || . osiris.sh

# Comprobación de aplicaciones instaladas.


check_command_installed osiris-env-sys-vars

#activamos directorio virtual
eval . bin/venv.sh


check_command_installed /usr/bin/python-pack
#check_command_installed node-Opack --version
#check_command_installed terminator-Opack 
check_command_installed ffmpeg-pack
#check_command_installed tmux-pack










#check_command_installed  /usr/bin/date && /usr/bin/date -R 


#check_command_installed /usr/bin/pip
#check_command_installed /usr/bin/nodejs
#check_command_installed /usr/bin/certbot

#check_command_installed /usr/bin/Osiris-python3.9-venv

#. bin/venv.sh


#check_command_installed /usr/bin/Osiris-venv-activate
#check_command_installed /usr/bin/Osiris-venv-export

#check_command_installed /usr/bin/depend

#check_command_installed /usr/bin/tor --version

#check_command_installed /usr/sbin/apache2 -v
#check_command_installed /usr/bin/php --version 
#check_command_installed /usr/bin/mariadb 
#check_command_installed /usr/bin/ffmpeg -version
#check_command_installed /usr/bin/transmission-cli --version 
#check_command_installed /usr/bin/port-audio 
#check_command_installed /usr/bin/tcptrack --version 
#check_command_installed /usr/bin/yt-dlp --version
#check_command_installed /usr/bin/rustc "--version -v"
#check_command_installed /usr/bin/docker 



