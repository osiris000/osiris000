#!/bin/bash
echo "Este script activa el directorio vrtual"


# Asegurarse de que las variables de entorno están definidas
if [ -z "$OSIRIS000_VENV_PATH" ] || [ -z "$OSIRIS000_VENV_NAME" ]; then
    echo "Las variables de entorno OSIRIS000_VENV_PATH y OSIRIS000_VENV_NAME deben estar definidas."
    echo "Se va a Ejecutar osiris_env_sys_vars.sh para establecer las variables de entorno "
    ./bin/install/osiris_env_sys_vars.sh
    return 0
fi


echo "Activando directorio virtual en: ${OSIRIS000_VENV_PATH} "
python3 -m venv $OSIRIS000_VENV_PATH
echo  $VENV_ACTIVATE_PATH
eval source $VENV_ACTIVATE_PATH
export PYTHONPATH=".:$OSIRIS000_VENV_PYTHONPATH"


