#!/bin/sh

# Comprobación de requisitos del sistema.

check_command_installed() {
  command_path=$1
  version_option=$2

  # Si no se proporciona una opción de versión, utilizar --version
  if [ -z "$version_option" ]; then
    version_option="--version"
  fi

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



# Comprobación de aplicaciones instaladas.
check_command_installed /usr/bin/python3 
check_command_installed /usr/sbin/apache2 -v
check_command_installed /usr/bin/php 
check_command_installed /usr/bin/mariadb 
check_command_installed /usr/bin/ffmpeg 
check_command_installed /usr/bin/transmission-cli 
check_command_installed /usr/local/bin/youtube-dl 
check_command_installed /usr/bin/rustc 




#continue





