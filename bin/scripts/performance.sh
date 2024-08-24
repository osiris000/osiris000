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
PROGRAM_LOG="${PIPE_DIR}/program.log"

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

# Función genérica para ejecutar un programa en segundo plano
run_program() {
    local program=$1      # Nombre del programa a ejecutar
    local pipe=$2         # Pipe donde redirigir la salida del programa
    local log_file=$3     # Log para registrar la actividad del programa

    # Redirigir la salida estándar y los errores del programa al pipe
    stdbuf -oL "$program" > "$pipe" 2>&1 &
    PROGRAM_PID=$!
    echo "$program iniciado con PID: $PROGRAM_PID" >> "$log_file"

    # Monitorización del proceso
    while true; do
        if ! ps -p $PROGRAM_PID >/dev/null; then
            echo "$program con PID $PROGRAM_PID ha terminado." >> "$log_file"
            break
        fi
        sleep 5
    done
}

# Bucle principal para seleccionar a qué bucle enviar los datos
display_prompt_info="Input el comando ('1' para enviar a Bucle 1, '2' para enviar a Bucle 2, 'exit' para salir): "

while true; do
    # Mostrar el prompt de entrada
    display_prompt "→ "
    read comando

    if [ "$comando" == "exit" ]; then
        echo "Saliendo..."
        break
    elif [ "$comando" == "1" ]; then
        display_prompt ">>>${comando}>> "
        read data
        echo "$data" > "$PIPE1"
        if [ "$data" == "MEM" ]; then
            echo "Starting freemem:$data"
            echo "Starting freemem..." >> "$PIPE1"
            # Ejecutar el programa 'freemem' en segundo plano y redirigir la salida a PIPE1
            run_program "$OSIRIS000_BIN/scripts/freemem" "$PIPE1" "$PROGRAM_LOG" & 
        elif [ "$data" == "OTRO" ]; then
            echo "Starting $data" >> "$PIPE1"
            # Ejemplo de ejecución de otro programa
#            run_program "/path/to/otro_programa" "$PIPE1" "$PROGRAM_LOG"
        fi
    elif [ "$comando" == "2" ]; then
        display_prompt ">>>${comando}>> "
        read data
        echo "$data" > "$PIPE2"
        if [ "$data" == "XXXX" ]; then
            echo "Starting XXXX..." >> "$PIPE2"
        elif [ "$data" == "MENU" ]; then
            echo "Starting $data" >> "$PIPE2"
            # Ejemplo de ejecución de otro programa
  #          run_program "/path/to/otro_programa" "$PIPE2" "$PROGRAM_LOG"
        fi
    else
        display_prompt "Comando no reconocido."
    fi
done

# Limpiar al salir (esto se ejecutará debido al trap)
rm "$PIPE1" "$PIPE2"
