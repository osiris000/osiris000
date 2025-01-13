#!/bin/bash
## Script Bash completo para diagnóstico y reparación no invasivos de Osiris 🛠️




# --- Variables ---
LOG_FILE="osiris_diagnostic.log"
WEBROOT="/var/www/osiris000/html" # Ajusta a tu webroot
PHP_FPM_SERVICES=("php7.4-fpm" "php8.0-fpm" "php8.1-fpm") # Añade más versiones de PHP-FPM si es necesario

# --- Funciones ---

function check_usb {
  local result=$(lsusb | grep "046d:c050")
  echo "Comprobando estado del puerto USB 4-1..." >> "$LOG_FILE"
  if [[ -n "$result" ]]; then
    echo "Ratón Logitech conectado. Intentando reiniciar el servicio udev..." >> "$LOG_FILE"
    systemctl restart udev
    sleep 5
    result=$(lsusb | grep "046d:c050")
    if [[ -n "$result" ]]; then
      echo "Ratón Logitech conectado tras reiniciar udev. 👌" >> "$LOG_FILE"
    else
      echo "Problema persiste con el ratón Logitech. Intentando reiniciar el kernel... ⚠️" >> "$LOG_FILE"
      sudo reboot
    fi
  else
    echo "Ratón Logitech NO conectado. Verifica la conexión física. ⚠️" >> "$LOG_FILE"
  fi
}

function check_apache_php {
  echo "Comprobando configuración de Apache y PHP-FPM..." >> "$LOG_FILE"
  # Comprobar si el módulo php está cargado en Apache.
  apache2ctl -M | grep php >> "$LOG_FILE" 2>&1
  local php_module_loaded=$?
  if [ $php_module_loaded -ne 0 ]; then
      echo "Módulo PHP no cargado en Apache. Habilítalo y reinicia Apache. ⚠️" >> "$LOG_FILE"
      return 1
  fi

  # Comprobar estado de php-fpm (búsqueda extendida)
  local fpm_service_found=false
  for fpm_service in "${PHP_FPM_SERVICES[@]}"; do
    if systemctl is-active "$fpm_service" > /dev/null 2>&1; then
      echo "Servicio php-fpm ($fpm_service) encontrado y activo. 👍" >> "$LOG_FILE"
      fpm_service_found=true
      break
    fi
  done

  if ! $fpm_service_found; then
    echo "No se encontró ningún servicio php-fpm activo entre los listados.  Busca manualmente. ⚠️" >> "$LOG_FILE"
    return 1 # Indica fallo
  fi


  # Revisar errores en logs de Apache (si existen)
  if [ -f "/var/log/apache2/error.log" ]; then
      echo "Revisando errores en /var/log/apache2/error.log..." >> "$LOG_FILE"
      cat /var/log/apache2/error.log | grep -E "Primary script unknown|PHP Warning" >> "$LOG_FILE" 2>&1
  else
      echo "Archivo de error de Apache no encontrado. ⚠️" >> "$LOG_FILE"
  fi
  apache2ctl graceful  # Reiniciar suavemente Apache
  echo "Apache reiniciado suavemente. 👍" >> "$LOG_FILE"
}


function check_apache_ssl {
    echo "Comprobando configuración SSL de Apache y renovando certificados con Certbot..." >> "$LOG_FILE"
    # Buscar certificados existentes
    local cert_path=$(find "$WEBROOT" -maxdepth 1 \( -name "*.crt" -o -name "*.pem" \) 2>/dev/null)

    if [[ -n "$cert_path" ]]; then
        echo "Certificados encontrados en: $cert_path" >> "$LOG_FILE"
        # Intentar renovar los certificados con Certbot
        sudo certbot renew --quiet >> "$LOG_FILE" 2>&1
        local renew_status=$?
        if [ $renew_status -eq 0 ]; then
            echo "Certificados renovados correctamente. 👍" >> "$LOG_FILE"
            apache2ctl graceful >> "$LOG_FILE" 2>&1
            echo "Apache reiniciado suavemente tras la renovación de certificados. 👍" >> "$LOG_FILE"
        else
            echo "Error al renovar los certificados con Certbot. Revisa el log de Certbot y la configuración de tu dominio. 😥" >> "$LOG_FILE"
        fi
    else
        echo "No se encontraron certificados SSL en $WEBROOT.  Intenta obtener un certificado nuevo con Certbot. ⚠️" >> "$LOG_FILE"
        # Obtener un certificado nuevo con Certbot (necesitas especificar tu dominio y posiblemente opciones adicionales)
        #Comprueba que el directorio webroot sea accesible por certbot
        sudo certbot certonly --webroot -w "$WEBROOT" -d osiris000.duckdns.org >> "$LOG_FILE" 2>&1 # Reemplaza osiris000.duckdns.org con tu dominio
        if [ $? -eq 0 ]; then
            echo "Certificado obtenido correctamente. 👍" >> "$LOG_FILE"
            apache2ctl graceful >> "$LOG_FILE" 2>&1
            echo "Apache reiniciado suavemente tras obtener un nuevo certificado. 👍" >> "$LOG_FILE"
        else
            echo "Error al obtener un certificado con Certbot. Revisa el log de Certbot y la configuración de tu dominio. 😥" >> "$LOG_FILE"
        fi

    fi
}


function check_chrome {
    echo "Revisando Chrome..." >> "$LOG_FILE"
    echo "Cierra y vuelve a abrir Chrome manualmente para descartar problemas temporales.  👍" >> "$LOG_FILE"
}

function check_fontconfig {
    echo "Comprobando Fontconfig..." >> "$LOG_FILE"
    echo "Este script no puede corregir la advertencia de Fontconfig. Revisa manualmente el archivo /usr/share/fontconfig/conf.avail/05-reset-dirs-sample.conf.  ⚠️" >> "$LOG_FILE"
}

function check_nginx_logs {
  echo "Comprobando logs de Nginx..." >> "$LOG_FILE"
  if [ -f "/var/log/nginx/error.log" ]; then
    echo "Archivo de error de Nginx encontrado. Revisando..." >> "$LOG_FILE"
    tail -n 100 /var/log/nginx/error.log >> "$LOG_FILE" 2>&1
  else
    echo "Archivo de error de Nginx NO encontrado. ⚠️" >> "$LOG_FILE"
  fi
}

function check_mysql_logs {
  echo "Comprobando logs de MySQL..." >> "$LOG_FILE"
  if [ -f "/var/log/mysql/error.log" ]; then
    echo "Archivo de error de MySQL encontrado. Revisando..." >> "$LOG_FILE"
    tail -n 100 /var/log/mysql/error.log >> "$LOG_FILE" 2>&1
  else
    echo "Archivo de error de MySQL NO encontrado. ⚠️" >> "$LOG_FILE"
  fi
}

# --- Ejecución del script ---

echo "===================================="
echo " Iniciando diagnóstico de Osiris..."
echo "====================================" > "$LOG_FILE"

#check_usb
check_apache_php
#check_apache_ssl
check_chrome
check_fontconfig
check_nginx_logs
check_mysql_logs

echo "===================================="
echo " Diagnóstico finalizado.  El reporte se encuentra en: $LOG_FILE"
echo "====================================" >> "$LOG_FILE"
echo "Reporte generado en: $LOG_FILE"


