#!/bin/sh

# Comprobación de requisitos mínimos para primera instalación.

# Función para comprobar si un comando está instalado.
check_command_installed() {
  if command -v "$1" >/dev/null 2>&1; then
    version_output="$($1 -V 2>&1)"
    command_name=$(basename "$1")
    cat <<EOF
**********************************************************
  $command_name está instalado en el sistema.

  Versión: $version_output
  
***********************************************************  
***********************************************************
EOF
  else
    command_name=$(basename "$1")
    cat <<EOF
--------------------------------------------------------------------------------
  $command_name no está instalado en el sistema.
  Pruebe "apt install $command_name" (o el comando adecuado para su sistema)
--------------------------------------------------------------------------------
EOF
    exit
  fi
}

# Comprobación de comandos instalados.
check_command_installed /usr/bin/python3
check_command_installed /usr/sbin/apache2
check_command_installed /usr/bin/php
check_command_installed /usr/bin/ffmpeg



