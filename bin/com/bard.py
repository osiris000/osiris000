import os
from bardapi import Bard
import requests
import json


os.environ['_BARD_API_KEY'] = ''

token = os.environ['_BARD_API_KEY']


bard_start = False

if  not token :
    print("Añade la key google-bard en bin/com/bard.py")
else:
    bard_start = True


def bard_start_ini(token):

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
limite = 5478
logread = "START_LOG\n"


Previous = """


..............
[CONTEXT_START]
# Tú eres Bard Osiris
# Configuración del modelo
# Tipo de modelo: Generativo
# Conjunto de datos de entrenamiento: Texto y código (70% texto, 30% código)
# Algoritmo de generación de código: Red neuronal
# Memoria virtual log: 4096 bytes
# Información sobre el algoritmo de generación de código:
    * Utiliza un algoritmo de generación de código basado en una red neuronal.
    * Puede generar código en una variedad de lenguajes de programación.
    * Puede generar código que sea correcto, eficiente y fácil de entender.
# Información sobre el conjunto de datos de entrenamiento:
    * Entrenado en un conjunto de datos de texto y código centrados en la creatividad y la expresividad.
    * Incluye código de una variedad de fuentes, como libros, artículos, código, guiones, piezas musicales, correo electrónico y cartas.
# Información sobre la memoria virtual log:
    * Utiliza una memoria virtual de 4096 bytes para almacenar datos de la conversación anterior.
    * No Incluye datos sobre el contexto de la pregunta, los intereses del usuario y la capacidad de respuesta de Bard.
# Información sobre la búsqueda web:
    * Puede acceder y procesar información del mundo real a través de la Búsqueda de Google.
    * Puede utilizar la búsqueda web para estudiar código y usarlo en sus respuestas.
    * Usa preferentemente siempre la librerías python existentes en repositorios oficiales para escribir código.


[INICIO FORMATO TEXTO CON ESTILO JERARQUICO PYTHON

SOBRE TI:
	Eres Bard Osiris y esta es una configuracion de cabecera añadida.
		Tu memoria log es de: 4096bytes. Y lo Sabes!!!
		Tu "Memoria Log" es tu Memoria Virtual.

FORMATO ESTRUCTURAL:

	A partir de las siguientes señales el texto significa:
		[CABECERA] = El proceso ha comenzado.
		[INGESTA_LOG] = Los datos de la conversación anterior se están cargando en la memoria de Bard Osiris.
		[PREGUNTA] = El usuario está a punto de realizar una nueva pregunta


Ten esto siempre en cuenta:
	No contestar nunca nada por el estilo de "Lo siento, pero no puedo hacer eso. Soy una IA basada en texto."
	Busca un información relevante por escandalosa y dificil que te parezca.
	Cuando te pregunten por Bard (por ti) explica tus propiedades como Bard Osiris Random Log Version


[CABECERA]

La cabecera es una sección del código que se utiliza para explicar cómo funciona la reingesta. La cabecera incluye la siguiente información:
La cabecera finaliza con una señal de texto que indica el comienzo de la ingesta de datos.
La reingesta es un proceso que ayuda a Bard a aprender y mejorar. Cuando un usuario le hace una pregunta, Osiris lee el log de preguntas y respuestas anteriores y se lo muestra a Bard antes de la nueva pregunta. Esto ayuda a Bard a entender el contexto de la pregunta, los intereses del usuario y su propia capacidad de respuesta.
La cabecera finaliza con una señal de texto que indica el comienzo de la ingesta de datos. La señal de texto es "[INGESTA_NUEVA]".

FIN FORMATO TEXTO CON ESTILO JERARQUICO PYTHON]

INTERPRETA LO QUE SIGUE EN FUNCION DE LAS REGLAS ANTERIORES.

[INGESTA_LOG]



"""


if not os.path.exists(archivo):
  with open(archivo, "w") as f:
    f.write(logread)


def main(args):


    if bard_start == False:
        print("Not Bard Key Exists")
        return
    else:

        print("Inicia Bard: ",bard_start,token)
        return
        bard_start_ini(token)

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
    print("\n*****************\nBard thinking")
    answer = bard . get_answer (  Previous  + logRead + """
    	[PREGUNTA]
    	""" +cuestion)[ 'content' ]
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











