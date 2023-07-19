#!/bin/sh


#comprobación de requisitos, python3

if command -v python3 >/dev/null 2>&1; then
  python_version=$(python3 -V 2>&1)
  echo "Python está instalado en el sistema. Versión: $python_version"
else
  echo "Python no está instalado en el sistema."
fi

