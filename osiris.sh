#!/bin/sh


#comprobación de requisitos mínimos para primera instalación, 

#python3

check_command_installed() {
  if command -v "$1" >/dev/null 2>&1; then
    version_output="$($1 -V 2>&1)"
    echo "$1 está instalado en el sistema. Versión: $version_output"
  else
    cat <<EOF
$1 no está instalado en el sistema
Pruebe "apt install $1" (o el comando adecuado para su sistema)
EOF
  fi
}


check_command_installed python3

check_command_installed ffmpeg
