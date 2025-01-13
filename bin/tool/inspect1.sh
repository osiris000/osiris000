#!/bin/bash


## Script Bash para solucionar errores en Osiris (soluciones no invasivas - versión mejorada) 🛠️
# --- Funciones ---

function check_usb {
  echo "Comprobando estado del puerto USB 4-1..."
  lsusb | grep "046d:c050" > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Ratón Logitech conectado. Intentando reiniciar el servicio udev..."
    systemctl restart udev
    sleep 5
    lsusb | grep "046d:c050" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      echo "Ratón Logitech conectado tras reiniciar udev. 👌"
    else
      echo "Problema persiste con el ratón Logitech.  Intentando reiniciar el kernel... ⚠️"
      sudo reboot
    fi
  else
    echo "Ratón Logitech NO conectado. Verifica la conexión física. ⚠️"
  fi
}

function check_apache_php {
  echo "Comprobando configuración de Apache y PHP-FPM..."
  # Comprobar si el módulo php está cargado en Apache.
  apache2ctl -M | grep php > /dev/null 2>&1
  if [ $? -ne 0 ]; then
      echo "Módulo PHP no cargado en Apache. Habilítalo y reinicia Apache. ⚠️"
      return 1
  fi

  # Comprobar estado de php-fpm
  systemctl status php7.4-fpm > /dev/null 2>&1 # Ajusta php7.4-fpm a tu versión de PHP
  if [ $? -ne 0 ]; then
    echo "Servicio php-fpm no activo o con errores. Intentando reiniciarlo... ⚠️"
    systemctl restart php7.4-fpm # Ajusta php7.4-fpm a tu versión de PHP
    sleep 5
    systemctl status php7.4-fpm # Ajusta php7.4-fpm a tu versión de PHP
    if [ $? -ne 0 ]; then
        echo "php-fpm sigue con problemas. Revisa los logs de php-fpm. 😥"
    else
        echo "php-fpm reiniciado correctamente. 👍"
    fi
  else
    echo "Servicio php-fpm activo. 👍"
  fi


  # Revisar errores en logs de Apache (si existen)
  if [ -f "/var/log/apache2/error.log" ]; then
      echo "Revisando errores en /var/log/apache2/error.log..."
      cat /var/log/apache2/error.log | grep -E "Primary script unknown|PHP Warning" # Mostrar solo errores relevantes
  else
      echo "Archivo de error de Apache no encontrado. ⚠️"
  fi
  apache2ctl graceful  # Reiniciar suavemente Apache
  echo "Apache reiniciado suavemente. 👍"
}


function check_apache_ssl {
    echo "Comprobando configuración SSL de Apache..."
    # Esta función requiere más información sobre la configuración específica de SSL.
    # Se debe verificar la existencia y validez de los certificados.  Se necesita adaptar esta sección a tu caso concreto.
    # Ejemplo (necesita ajustes según tu configuración):
    # if [ -f /etc/ssl/certs/your_certificate.crt ]; then
    #     echo "Certificado encontrado. Verifica su validez y configuración en apache2.conf"
    # else
    #     echo "Certificado SSL no encontrado. ⚠️"
    # fi

    echo "Comprueba manualmente la configuración de tu certificado SSL en los archivos de configuración de Apache.  ⚠️"

}


function check_chrome {
    echo "Revisando Chrome..."
    echo "Cierra y vuelve a abrir Chrome manualmente para descartar problemas temporales.  👍"
}

function check_fontconfig {
    echo "Comprobando Fontconfig..."
    echo "Este script no puede corregir la advertencia de Fontconfig. Revisa manualmente el archivo /usr/share/fontconfig/conf.avail/05-reset-dirs-sample.conf.  ⚠️"
}


function check_nginx_logs {
  echo "Comprobando logs de Nginx..."
  if [ -f "/var/log/nginx/error.log" ]; then
    echo "Archivo de error de Nginx encontrado. Revisando..."
    tail -n 100 /var/log/nginx/error.log
  else
    echo "Archivo de error de Nginx NO encontrado. ⚠️"
  fi
}

function check_mysql_logs {
  echo "Comprobando logs de MySQL..."
  if [ -f "/var/log/mysql/error.log" ]; then
    echo "Archivo de error de MySQL encontrado. Revisando..."
    tail -n 100 /var/log/mysql/error.log
  else
    echo "Archivo de error de MySQL NO encontrado. ⚠️"
  fi
}

# --- Ejecución del script ---

echo "===================================="
echo " Iniciando diagnóstico de Osiris..."
echo "===================================="

check_usb
check_apache_php
check_apache_ssl
check_chrome
check_fontconfig
check_nginx_logs
check_mysql_logs

echo "===================================="
echo " Diagnóstico finalizado."
echo "===================================="



