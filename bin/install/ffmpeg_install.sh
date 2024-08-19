#!/bin/bash

echo "FFmpeg Installer"

# Modo de salida (se puede cambiar a: verbose, info, quiet, resume, ultra-verbose)
MODE="${MODE:-ultra-verbose}"
VALID_MODES=("verbose" "info" "quiet" "resume" "ultra-verbose")

# Función para imprimir mensajes según el modo
function log_message() {
  local level="$1"
  local message="$2"
  case "$MODE" in
    "ultra-verbose")
      echo "[$level] $message"
      set -x  # Habilitar la impresión de comandos y sus argumentos
      ;;
    "verbose")
      echo "[$level] $message"
      ;;
    "info")
      if [[ "$level" == "info" || "$level" == "error" ]]; then
        echo "[$level] $message"
      fi
      ;;
    "quiet")
      if [[ "$level" == "error" ]]; then
        echo "[$level] $message"
      fi
      ;;
    "resume")
      if [[ "$level" == "error" || "$level" == "info" ]]; then
        echo "[$level] $message"
      fi
      ;;
    *)
      echo "Modo desconocido: $MODE"
      exit 1
      ;;
  esac
}

# Comprobar si el script es la ejecución principal o está siendo incluido
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  MAIN_SCRIPT=true
else
  MAIN_SCRIPT=false
fi

# Verificar si la variable OSIRIS000_VENV_PATH está definida y tiene valor
if [ -z "$OSIRIS000_VENV_PATH" ]; then
  log_message "error" "La variable OSIRIS000_VENV_PATH no está definida o está vacía. Aborting."
  if $MAIN_SCRIPT; then
    exit 1
  else
    return 1
  fi
else
  log_message "info" "Directorio base para la instalación de FFmpeg: $OSIRIS000_VENV_PATH"
fi

# Definir el directorio base para la instalación
install_dir="$OSIRIS000_VENV_PATH/software/ffmpeg"
bin_dir="$install_dir/bin"
src_dir="$install_dir/src"

# Crear todos los directorios necesarios
log_message "info" "Creando directorios..."
mkdir -p "$src_dir" "$install_dir" "$bin_dir"

# Preguntar al usuario si desea proceder con la instalación
read -p "¿Desea proceder con la instalación de FFmpeg? (sí/no): " user_response
if [[ "$user_response" != "sí" && "$user_response" != "si" ]]; then
  log_message "info" "Instalación cancelada por el usuario."
  if $MAIN_SCRIPT; then
    exit 0
  else
    return 0
  fi
fi

# Opciones del usuario
install_deps=true
compile_only=false

# Preguntar si el usuario desea instalar las dependencias necesarias
read -p "¿Desea instalar las dependencias necesarias? (sí/no, por defecto sí): " user_deps_response
if [[ "$user_deps_response" == "no" || "$user_deps_response" == "n" ]]; then
  install_deps=false
fi

# Preguntar si el usuario desea solo compilar FFmpeg
read -p "¿Desea solo compilar FFmpeg y no instalar dependencias? (sí/no, por defecto no): " user_compile_only_response
if [[ "$user_compile_only_response" == "sí" || "$user_compile_only_response" == "si" ]]; then
  compile_only=true
fi

# Función para instalar una dependencia y manejar errores
function install_dependency() {
  local package="$1"
  log_message "info" "Instalando dependencia: $package..."
  sudo apt-get install -y "$package" || {
    log_message "error" "Error al instalar $package. Intentando resolver problemas con 'apt-get -f install'..."
    sudo apt-get -f install || {
      log_message "error" "No se pudieron resolver los problemas de dependencias con 'apt-get -f install'."
      exit 1
    }
  }
}

# Función para instalar las dependencias necesarias
function install_dependencies() {
  log_message "info" "Instalando dependencias necesarias..."
  install_dependency "nasm"
  install_dependency "yasm"
  install_dependency "build-essential"
  install_dependency "libtool"
  install_dependency "automake"
  install_dependency "autoconf"
  install_dependency "cmake"
  install_dependency "git"
  install_dependency "libass-dev"
  install_dependency "libfreetype6-dev"
  install_dependency "libgnutls28-dev"
  install_dependency "libmp3lame-dev"
  install_dependency "libvorbis-dev"
  install_dependency "libvpx-dev"
  install_dependency "pkg-config"
  install_dependency "texinfo"
  install_dependency "wget"
  install_dependency "zlib1g-dev"
  install_dependency "libfontconfig1-dev"
  install_dependency "libfribidi-dev"
  install_dependency "libharfbuzz-dev"
  install_dependency "libbrotli-dev"
  install_dependency "libgmp-dev"
  install_dependency "libidn2-dev"
  install_dependency "libmp3lame-dev"
  install_dependency "libp11-kit-dev"
  install_dependency "libtasn1-6-dev"
  install_dependency "libvorbis-dev"
}

# Función para verificar la presencia de nasm y yasm
function check_tools() {
  log_message "info" "Verificando herramientas necesarias (nasm y yasm)..."
  if ! command -v nasm >/dev/null 2>&1; then
    log_message "error" "nasm no está instalado. Asegúrese de instalarlo antes de continuar."
    exit 1
  fi

  if ! command -v yasm >/dev/null 2>&1; then
    log_message "error" "yasm no está instalado. Asegúrese de instalarlo antes de continuar."
    exit 1
  fi
}

# Función para instalar o actualizar FFmpeg
function ffmpeg_install_or_update() {
  # Instalar dependencias si es necesario
  if [[ $install_deps == true ]]; then
    install_dependencies
  fi

  # Verificar la presencia de herramientas necesarias
  check_tools

  # Obtener la última versión de FFmpeg
  log_message "info" "Obteniendo la última versión de FFmpeg..."
  latest_version=$(wget -qO- "https://ffmpeg.org/releases/" | grep -oP 'ffmpeg-\K[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n1)
  if [[ -z "$latest_version" ]]; then
    log_message "error" "No se pudo obtener la última versión de FFmpeg."
    exit 1
  fi

  ffmpeg_url="https://ffmpeg.org/releases/ffmpeg-${latest_version}.tar.gz"
  ffmpeg_filename="ffmpeg-${latest_version}.tar.gz"

  log_message "info" "URL de descarga de FFmpeg: $ffmpeg_url"

  # Descargar y extraer FFmpeg
  log_message "info" "Descargando FFmpeg $latest_version..."
  wget "$ffmpeg_url" -O "$src_dir/$ffmpeg_filename" || { log_message "error" "Error al descargar FFmpeg."; exit 1; }

  log_message "info" "Extrayendo FFmpeg..."
  tar -xzf "$src_dir/$ffmpeg_filename" -C "$src_dir" || { log_message "error" "Error al extraer FFmpeg."; exit 1; }

  # Cambiar al directorio de FFmpeg
  cd "$src_dir/ffmpeg-${latest_version}" || { log_message "error" "No se pudo cambiar al directorio ffmpeg-${latest_version}"; exit 1; }

  # Configurar y compilar FFmpeg
  log_message "info" "Configurando FFmpeg..."
  ./configure --prefix="$install_dir" || { log_message "error" "Error durante la configuración de FFmpeg."; exit 1; }

  log_message "info" "Compilando FFmpeg..."
  make -j$(nproc) || { log_message "error" "Error durante la compilación de FFmpeg."; exit 1; }

  log_message "info" "Instalando FFmpeg..."
  make install || { log_message "error" "Error durante la instalación de FFmpeg."; exit 1; }

  # Añadir FFmpeg al PATH
  log_message "info" "Añadiendo FFmpeg al PATH..."
  echo "export PATH=\"$bin_dir:\$PATH\"" >> ~/.bashrc
  source ~/.bashrc

  log_message "info" "FFmpeg instalado o actualizado correctamente en $install_dir"
}

# Ejecutar la función principal
ffmpeg_install_or_update

# Mensaje final
log_message "info" "Proceso de instalación completado."

# Salir con estado exitoso
if $MAIN_SCRIPT; then
  exit 0
else
  return 0
fi
