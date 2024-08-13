#!/bin/bash


if [ "$(id -u)" -eq 0 ]; then
    echo "El usuario es root. Continuando con el script."
else
    echo "Este script debe ejecutarse como root para continuar."

    # Obtener la ruta del directorio actual
    current_directory=$(pwd)

    # Intentar cambiar al usuario root con el comando "su"
    su -c "cd $current_directory; exec bash ./osiris.sh"

    # Comprobar si se pudo cambiar a root exitosamente
    if [ "$(id -u)" -eq 0 ]; then
        echo "Ahora eres root. Continuando con el script."
    else
        ./osiris.sh
        exit 1
    fi
fi


# Continuar con el resto del script aquí...

. share.sh
. install.sh

#continue


python_osiris_path="osiris.py"

cd bin && /usr/bin/python3 "$python_osiris_path"