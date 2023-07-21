#!/bin/sh

#!/bin/bash

# Array con los nombres de las aplicaciones y sus comandos de instalación
declare -A INSTALL_COMMANDS=(
  ["python3"]="apt install python3"
  ["apache2"]="apt install apache2"
  ["php"]="apt install php"
  ["mariadb"]="apt install mariadb"
  ["ffmpeg"]="apt install ffmpeg"
  ["pip3"]="apt install pip3"
  # Agrega aquí otras aplicaciones que desees verificar e instalar
)

# Función para instalar una aplicación usando apt
apt_install_command() {
  app_name=$1
  command_to_install=${INSTALL_COMMANDS[$app_name]}

  if [ -n "$command_to_install" ]; then
    echo "Pruebe \"$command_to_install\" para instalar $app_name."
    read -p "¿Desea continuar? (y/s/n): " choice
    case "$choice" in 
      y|Y ) 
        $command_to_install
        ;;
      s|S ) 
        echo "Instalación saltada."
        ;;
      * )
        echo "Instalación cancelada."
        ;;
    esac
  else
    echo "No se encontró el comando de instalación para $app_name."
  fi
}



# Función para comprobar si un comando está instalado
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
      apt_install_command "$command_name"
      echo "------------------------------------------------------------------"
      exit 1
    fi
  fi
}








