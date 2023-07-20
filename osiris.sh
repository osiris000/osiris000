#!/bin/sh

# Comprobación de requisitos mínimos para primera instalación.


check_command_installed() {
  command_path=$1
  version_option=$2

  # Verificar con la ruta del ejecutable
  if [ -x "$command_path" ]; then
    version_output="$($command_path $version_option </dev/null 2>&1)"
    command_name=$(basename "$command_path")
    echo "******************************************************************"
    printf "%-64s%s\n" " $command_name está instalado en la ruta especificada." "*"
    echo "------------------------------------------------------------------"
    echo "$version_output"
    echo "******************************************************************"
  else
    command_name=$(basename "$command_path")
    echo "------------------------------------------------------------------"
    printf "%-69s%s\n" " $command_name no está instalado en la ruta especificada."
    echo " Se está verificando con dpkg para obtener más información."
    echo "------------------------------------------------------------------"
    
    # Verificar con el sistema de gestión de paquetes
    dpkg_output=$(dpkg -l "$command_name" 2>&1)
    if [ $? -eq 0 ]; then
      echo "******************************************************************"
      printf "%-64s%s\n" " $command_name está instalado en el sistema (según dpkg)." "*"
      echo "------------------------------------------------------------------"
      echo "$dpkg_output" | tail -n +6
      echo "******************************************************************"
    else
      echo "------------------------------------------------------------------"
      printf "%-69s%s\n" " $command_name no está instalado en el sistema (según dpkg) tampoco."
      echo " Pruebe \"apt install $command_name\" (o el comando adecuado para su sistema)"
      echo "------------------------------------------------------------------"
      exit 1
    fi
  fi
}


# Comprobación de comandos instalados.
check_command_installed /usr/bin/python3 -V
check_command_installed /usr/sbin/apache2 -v
check_command_installed /usr/bin/php -v
check_command_installed /usr/bin/ffmpeg -v



