#!/bin/bash
clear

# Configuración: Crear las tuberías nombradas (FIFO) si no existen
PIPE_DIR="${OSIRIS000_BIN}/com/datas"

PIPE1_NAME="pipe1"
PIPE2_NAME="pipe2"
PIPE1="${PIPE_DIR}/${PIPE1_NAME}"
PIPE2="${PIPE_DIR}/${PIPE2_NAME}"

LOGFILE1="${PIPE_DIR}/pipe1.log"
LOGFILE2="${PIPE_DIR}/pipe2.log"

P1N="BUCLE 1"
P2N="BUCLE 2"

# Crear el directorio si no existe
mkdir -p "$PIPE_DIR"

# Crear las tuberías si no existen
if [ ! -p "$PIPE1" ]; then
    mkfifo "$PIPE1"
    echo "Creado $PIPE1_NAME"
else
    echo "$PIPE1_NAME ya existe..."
fi

if [ ! -p "$PIPE2" ]; then
    mkfifo "$PIPE2"
    echo "Creado $PIPE2_NAME"
else
    echo "$PIPE2_NAME ya existe..."
fi

# Manejo de señales para limpieza
trap "rm -f $PIPE1 $PIPE2; kill 0" SIGINT SIGTERM EXIT

# Función para procesar datos de una tubería
process_pipe() {
    local pipe=$1
    local name=$2
    local log_file=$3

    echo "$name iniciado, esperando datos..." >> "$log_file"

    while true; do
        if read line < "$pipe"; then
            echo "$name procesando: $line" >> "$log_file"
        fi
    done &
}

# Iniciar bucles en segundo plano
process_pipe "$PIPE1" "$P1N" "$LOGFILE1"
process_pipe "$PIPE2" "$P2N" "$LOGFILE2"

# Función para mostrar el prompt de entrada sin desplazar el texto
display_prompt() {
    local prompt="$1"
    tput cr    # Carriage Return: mueve el cursor al inicio de la línea
    tput el    # Elimina desde la posición del cursor hasta el final de la línea
    echo -n "$prompt"
}

# Bucle principal para seleccionar a qué bucle enviar los datos

    display_prompt_info="Input el comando ('1' para enviar a Bucle 1, '2' para enviar a Bucle 2, 'exit' para salir): "

while true; do
    # Mostrar el prompt de entrada
    display_prompt ">>>"
    read comando

    if [ "$comando" == "exit" ]; then
        echo "Saliendo..."
        break
    elif [ "$comando" == "1" ]; then
        display_prompt ">>>${comando}>> "
        read data
        echo "$data" > "$PIPE1"
       if [ "$data" == "MEM" ]; then
         echo "Executing Freemem..."
         echo "Executing Freemem..." > "$PIPE1"
         # Ejecutar el script en segundo plano con la salida no bufferizada redirigida al pipe
        "$OSIRIS000_BIN/scripts/freemem" > "$PIPE1" 2>&1 &
#        echo "Executed Freemem..."
#        echo "Executed freemem" > "$PIPE1"
#         echo "Executing CLEARDEP..."
#         echo "Executing CLEARDEP..." > "$PIPE1"
         # Ejecutar el script en segundo plano con la salida no bufferizada redirigida al pipe
#        "$OSIRIS000_BIN/scripts/cleardep.sh" > "$PIPE1" 2>&1 &
#        echo "Executed CLEARDEP..."
#        echo "Executed CLEARDEP" > "$PIPE1"
       fi
    elif [ "$comando" == "2" ]; then
        display_prompt ">>>${comando}>> "
        read data
        echo "$data" > "$PIPE2"
    else
        display_prompt "Comando no reconocido."
    fi
done

# Limpiar al salir (esto se ejecutará debido al trap)
rm "$PIPE1" "$PIPE2"
