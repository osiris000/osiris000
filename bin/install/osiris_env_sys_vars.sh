#!/usr/bin/bash
echo "Este script establece las variables del entorno global"
echo "  Virtual environment G-Osiris"
VENV_NAME="osiris_env"

# Variables de entorno (usa comillas dobles en todos los valores)
export OSIRIS000_VENV_PYTHONPATH="/var/www/osiris000/bin/com/osiris_env/lib/python3.9/site-packages"
export OSIRIS000_BIN="/var/www/osiris000/bin"
export OSIRIS000_BASEPATH="/var/www/osiris000"
export OSIRIS000_VENV_NAME="${VENV_NAME}"
export OSIRIS000_VENV_PATH="/var/www/osiris000/bin/com/osiris_env"
export VENV_ACTIVATE_PATH="/var/www/osiris000/bin/com/osiris_env/bin/activate"
export AME_VENV="${VENV_NAME}"
export OSIRIS_PUBLIC_WWW_DIR="/var/www/osiris000/html/app/freedirectory/osiris"


# Comando sed para actualizar el archivo /etc/environment de forma atómica
sudo sed -i -e "s|^OSIRIS000_VENV_PYTHONPATH=.*|OSIRIS000_VENV_PYTHONPATH=\"${OSIRIS000_VENV_PYTHONPATH}\"|g" \
           -e "s|^OSIRIS000_BIN=.*|OSIRIS000_BIN=\"${OSIRIS000_BIN}\"|g" \
           -e "s|^OSIRIS000_BASEPATH=.*|OSIRIS000_BASEPATH=\"${OSIRIS000_BASEPATH}\"|g" \
           -e "s|^OSIRIS000_VENV_NAME=.*|OSIRIS000_VENV_NAME=\"${OSIRIS000_VENV_NAME}\"|g" \
           -e "s|^OSIRIS000_VENV_PATH=.*|OSIRIS000_VENV_PATH=\"${OSIRIS000_VENV_PATH}\"|g" \
           -e "s|^VENV_ACTIVATE_PATH=.*|VENV_ACTIVATE_PATH=\"${VENV_ACTIVATE_PATH}\"|g" \
           -e "s|^AME_VENV=.*|AME_VENV=\"${AME_VENV}\"|g" \
           -e "s|^OSIRIS_PUBLIC_WWW_DIR=.*|OSIRIS_PUBLIC_WWW_DIR=\"${OSIRIS_PUBLIC_WWW_DIR}\"|g" \
           -e "/^$/d" /etc/environment  #Elimina lineas vacías

# Comprobar si sed se ejecutó correctamente.
if [ $? -ne 0 ]; then
    echo "Error al actualizar /etc/environment"
    exit 1
fi

# Recargar variables de entorno (opcional, ya que se exportan arriba)
source /etc/environment

echo "Variables de entorno configuradas correctamente."
