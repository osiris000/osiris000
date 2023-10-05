import os
from bardapi import Bard
import requests
import json
import hashlib

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
    TokenEncode = hash = hashlib.sha512(token.encode("utf-8")).hexdigest()
    print("Starting with token: ",TokenEncode)

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
limite = 8 * 512
logread = "START_LOG\n"


Previous = ""
pie = ""


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
            print("Bard fue iniciado\n")
            return
        else:
            print("Inicia Bard: ",bard_start)




    if args[0] == "--find-cookie":
    	cookie_value = find_cookie_value(cookie_key,"google.com")
    	print("Cookie VAlue:",cookie_value)
    	return

    if args[0] == "--clear-log":
    	with open(archivo, "w") as f:
    		f.write(logread)
    	print("\nLog Reiniciado",logread)
    	return


    if args[0] == "--load-header":

        if len(args) < 2:
            print("Faltan argumentos")
            return
        elif len(args) == 2:
            try:
                with open(args[1], "r") as f:
                    global Previous
                    Previous = f.read().rstrip()
                    print("leido y cargado",args[1])
                    return
            except FileNotFoundError:
                print("\nError:\n",FileNotFoundError)
                return
        return

    if args[0] == "--clear-header":
        Previous = ""
        print("Cabecera borrada")
        return

    if args[0] == "--show-header":
        print("Contenido de Header:\n",Previous)
        return





    recortar_archivo(archivo, limite)

    with open(archivo, "r") as f:
      logRead = f.read()

#    print('Args dentro de bard', args)
#    print('Args dentro de bard'," ".join(args))



    cuestion = " ".join(args)
    cuestion =  Previous  + cuestion + pie
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











