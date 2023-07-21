#!/bin/sh


# Leer el archivo de texto y crear el array
declare -A INSTALL_COMMANDS

while IFS= read -r line; do
  # Ignorar líneas vacías o que contengan solo espacios
  if [[ -n "${line// }" && "$line" != "#"* ]]; then
    app_name=$(echo "$line" | awk '{print $1}')
    command_to_install=$(echo "$line" | awk '{$1=""; print substr($0,2)}')
    INSTALL_COMMANDS["$app_name"]=$command_to_install
  fi
done < osiris.ini

# Función apt_install_command con opción para saltar la instalación
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
      read -p "¿Continuar o Salir? (c/s): " choice
    case "$choice" in
      s|S )
        echo "Instalación cancelada."
        exit 0
        ;;
    esac
    fi
  fi
}








