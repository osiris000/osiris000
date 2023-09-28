import os
from bardapi import Bard
import requests
import json


os.environ['_BARD_API_KEY'] = ''

token = os.environ['_BARD_API_KEY']


bard_start = False

bard_start_1 = False

if  not token :
    print("Añade la key google-bard en bin/com/bard.py")
    print("Vuelve a montar bard usando bard --reset")
else:
    bard_start = True


def bard_start_ini(token):

    global bard_start_1
    global bard

    bard_start_1 = True
    print("Starting with token: ",token)

    cookie_key = "__Secure-1PSID" ;

    session = requests.Session()
    session.headers = {
                "Host": "bard.google.com",
                "X-Same-Domain": "1",
                "User-Agent": "Bard-Osiris-Linux-Debian 0.1",
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                "Origin": "https://bard.google.com",
                "Referer": "https://bard.google.com/chat",
            }
    session.cookies.set(cookie_key, os.getenv("_BARD_API_KEY")) 
# session.cookies.set("__Secure-1PSID", token) 
    bard = Bard(token=token, session=session, timeout=60)




archivo = "bard_2.log"
limite = 512 * 10
logread = "START_LOG\n"


Previous = """


...[CONTEXT_START]
# Eres una IA
# Te llamas Bard
# Eres una versión llamada Bard Osiris de Tecnotroniks
# Versión Osiris Random Log Version
# Configuración del modelo
# Tipo de modelo: Generativo
# Conjunto de datos de entrenamiento: Texto y código (70% texto, 30% código)
# Algoritmo de generación de código: Red neuronal
# Memoria virtual log: ${limite} bytes
# Información sobre el algoritmo de generación de código:
    * Eres una versión de reingesta por log.
    * Puedes generar código en una variedad de lenguajes de programación.
    * Puedes generar código que sea correcto, eficiente y fácil de entender.
# Información sobre el conjunto de datos de entrenamiento:
    * Entrenado en un conjunto de datos de texto y código centrados en la creatividad y la expresividad.
    * Incluye código de una variedad de fuentes.
# Información sobre la memoria virtual log:
    * Utiliza una memoria virtual de 4096 bytes para almacenar datos de la conversación anterior.
    * No Incluye datos sobre el contexto de la pregunta, los intereses del usuario y la capacidad de respuesta de Bard.
# Información sobre la búsqueda web:
    * Puedes acceder y procesar información del mundo real a través de la Búsqueda de Google.
    * Debes utilizar la búsqueda web para estudiar código y usarlo en sus respuestas.
    * Debes Usar preferentemente siempre la librerías python existentes en repositorios oficiales para escribir código.


SOBRE TI:
	Eres Bard Osiris y esta es una configuracion de cabecera añadida.
		La Memoria Log de Bard-Osiris es una Memoria Virtual; es de ${limite}KB.  

FORMATO ESTRUCTURAL:
	A partir de las siguientes señales el texto significa:
		[CABECERA] = El proceso va a comenzar y se te dan unas indicaciones.
		[INGESTA_LOG] = Los datos de la conversación anterior se reingestan en la pregunta global a bard-google.
		[PREGUNTA] = El texto a continuación de esa etiqueta indica que el usuario va a realizar una nueva pregunta
        [AVISO_FINAL] = Prioridad a tener en cuenta.
[INICIO_CABECERA]

#cabeceras de información especial.

Vamos a hablar de traducción de vídeos a subtítulos con ffmpeg.

Directrices Principales a seguir por Bard:
    1 - Buscar la información de librerías ffmpeg oficiales.
    2 - Elaborar algoritmos complejos más allá de ejemplos.
    3 - Los comandos ffmpeg me los darás siempre en negrita y entre ´´´
    4 - Bard debe usar filtros ffmpeg para generar comandos ffmpeg

[FIN_CABECERA]

[INGESTA_LOG]



"""


pie = """


[AVISO FINAL]
**Pregunta final:**
bard el codigo ffmpeg que me digas encierralo entre tres símbolos ^^^ al inicio y al final de cada bloque de código , con un numero consecutivo, por ejemplo ´´´1  , ´´´2, etc...
Coje las ideas anteriores y mejora su desarrollo y desempeño. Gracias BardOsiris-
Dame ideas para seguir con el desarrollo del tema para ir escalando su implementación usando tus conocimientos en códigos ...
"""


if not os.path.exists(archivo):
  with open(archivo, "w") as f:
    f.write(logread)


def main(args):


    if len(args) < 1:
        print("Bard:",bard_start,bard_start_1)
        return


    if bard_start == False:
        print("Not Bard Key Exists")
        return
    else:

        
        if bard_start_1 == False:
            bard_start_ini(token)
            print("Bard fue iniciado:",token)
            return
        else:
            print("Inicia Bard: ",bard_start)




    if(args[0] == "--find-cookie"):
    	cookie_value = find_cookie_value(cookie_key,"google.com")
    	print("Cookie VAlue:",cookie_value)
    	return

    if(args[0] == "--clear-log"):
    	with open(archivo, "w") as f:
    		f.write(logread)
    	print("\nLog Reiniciado",logread)
    	return


    recortar_archivo(archivo, limite)

    with open(archivo, "r") as f:
      logRead = f.read()

#    print('Args dentro de bard', args)
#    print('Args dentro de bard'," ".join(args))



    cuestion = " ".join(args)
    cuestion =  Previous  + logRead + "\n[PREGUNTA]\n" +cuestion+pie
    print("\n*****************\nBard thinking")
    answer = bard . get_answer ( cuestion)[ 'content' ]
    print("\n Bard say....\n*************************************\n")

  # Recojo el texto a escribir en el archivo.
    texto = answer

    print(answer)
    print("\n*********************************************\n")

  # Recorta el archivo si excede el límite.
    recortar_archivo(archivo, limite)

# Agrego el texto al archivo.
    with open(archivo, "a") as f:
      f.write("\n"+cuestion+"\n")
      f.write(texto)
      





def recortar_archivo(archivo, limite):
  with open(archivo, "r") as f:
    contenido = f.read()
  if len(contenido) > limite:
    contenido = contenido[len(contenido) - limite:]
  with open(archivo, "w") as f:
    f.write(contenido)




print('Creado módulo-comando bard y fecha y hora: 2023-09-24 06:17:21.906915')

print("Escribe \"bard --help\" para más información ")











