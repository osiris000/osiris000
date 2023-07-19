#!/bin/sh


#comprobación de requisitos, python3

if command -v python3 >/dev/null 2>&1; then
  echo "Python3 está instalado en el sistema."
else
  echo "Python3 no está instalado en el sistema."
fi

