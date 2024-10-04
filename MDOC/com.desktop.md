
## Manual de Uso del Módulo "desktop"

Este manual de uso te ayudará a comprender cómo funciona el módulo "desktop" y cómo utilizarlo para ejecutar diferentes comandos y aplicaciones.

### Descripción General

El módulo "desktop" es un script en Python que proporciona una interfaz de línea de comandos para interactuar con diferentes aplicaciones y procesos, incluyendo la ejecución de comandos personalizados, la gestión de procesos en segundo plano (background) y la visualización de información del sistema. 

### Requisitos Previos

* **Python 3:** Asegúrate de tener Python 3 instalado en tu sistema.
* **Módulo "osiris2":** El módulo "desktop" depende del módulo "osiris2" para la gestión de procesos y la ejecución de comandos.  Asegúrate de que "osiris2" esté instalado y disponible en tu sistema.

### Cómo Ejecutar el Módulo

1. **Abre una terminal o línea de comandos.**
2. **Navega hasta la ubicación del archivo "desktop.py".**
3. **Ejecuta el módulo usando el comando:** `>>>destop> <comando> <argumentos>`
4. **Reemplaza `<comando>` y `<argumentos>` con los comandos y argumentos específicos que deseas utilizar.**

### Comandos Disponibles

**Comandos generales:**

* **`man`:** Muestra la documentación del módulo.
* **`---edit`:** Edita el script "desktop.py" usando el editor de texto `nano`.
* **`killall`:** Termina todos los procesos iniciados por el módulo "desktop".
* **`kill <PID>`:** Termina el proceso con el PID especificado.
* **`list_processes`:** Lista todos los procesos que están en ejecución en el sistema.
* **`show_handlers`:** Muestra el contenido del diccionario de procesos en "osiris2".

**Comandos para aplicaciones:**

* **`<nombre de la aplicación>` <argumentos>:** Ejecuta la aplicación especificada en segundo plano. Los nombres de las aplicaciones disponibles son:
    * `dsk1`, `dsk2`, `dsk3`, `dsk4`, `dsk5`, `dsk6`, `dsk7`
    * `ipinfo`, `localnet`

**Comando para comandos personalizados:**

* **`com <comando> <argumentos>`:** Ejecuta el comando personalizado especificado en segundo plano. 

**Ejemplo:**

```bash
# Ejecutar la aplicación "dsk2" con los argumentos "arg1" y "arg2"
>>>destop> dsk2 arg1 arg2

# Ejecutar el comando "ls -l" en segundo plano
>>>destop> com ls -l
```

### Argumentos de Línea de Comando

Los argumentos de línea de comando son valores que se proporcionan después del comando principal para especificar opciones o parámetros adicionales.

**Para la mayoría de los comandos:**

* **`<argumentos>`:** Los argumentos necesarios para ejecutar el comando o la aplicación especificada.

**Ejemplos:**

```bash
# Ejecutar el comando "kill" con el PID 1234
>>>destop> kill 1234

# Ejecutar la aplicación "dsk1" con los argumentos "archivo.txt"
>>>destop> dsk1 archivo.txt
```

### Opciones de Configuración

El módulo "desktop" no tiene archivos de configuración específicos.

### Ejemplos de Uso

```bash
# Mostrar la documentación del módulo
>>>destop> man

# Editar el script "desktop.py"
>>>destop> ---edit

# Terminar todos los procesos iniciados por el módulo "desktop"
>>>destop> killall

# Terminar el proceso con PID 1234
>>>destop> kill 1234

# Listar todos los procesos que están en ejecución en el sistema
>>>destop> list_processes

# Mostrar el contenido del diccionario de procesos en "osiris2"
>>>destop> show_handlers

# Ejecutar la aplicación "dsk2" con los argumentos "arg1" y "arg2"
>>>destop> dsk2 arg1 arg2

# Ejecutar el comando "ls -l" en segundo plano
>>>destop> com ls -l
```

### Solución de Problemas

* **Error al importar el módulo "osiris2":** Asegúrate de que el módulo "osiris2" esté instalado y disponible en tu sistema.
* **Error al ejecutar un comando o aplicación:** Verifica la sintaxis del comando o aplicación y asegúrate de que los argumentos sean correctos.
* **Error al matar un proceso:** Asegúrate de que el PID proporcionado sea válido y que tengas permisos para terminar el proceso. 

### Notas Adicionales

* El módulo "desktop" utiliza el módulo "osiris2" para la gestión de procesos. Es posible que se requieran permisos especiales para iniciar o terminar ciertos procesos.
* Para ejecutar la aplicación "ipinfo", es necesario tener una conexión a Internet.
* El módulo "desktop" está en desarrollo, por lo que es posible que se agreguen nuevas funciones o comandos en el futuro.

