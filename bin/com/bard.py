import os
from bardapi import Bard
import requests
import json
import hashlib
import subprocess

os.environ['_BARD_API_KEY'] = 'g4GdblwfckOqajYNm6Y0BGeONQpnXDNph7jFo8XI6RjiJci3K5SJL66ZdXXCaviUcQxA.'

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
    "User-Agent": "Mozilla / Bard-OsirisB-Linux-Debian 0.1.1",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/chat",
    "X-Google-Length": "256000",  # longitud esperada de la respuesta
    "X-Google-Explanation": "false",  # solicitar una explicación adicional
    }
    session.cookies.set(cookie_key, os.getenv("_BARD_API_KEY")) 

    try:
        bard = Bard(token=token, session=session, timeout=60)
    except Exception as e:
        print(f"ERROR:{e}")
        return




def create_dir(path):
    """
    Crea un directorio si no existe.

    Args:
        path: La ruta del directorio a crear.

    Returns:
        True si el directorio se creó correctamente, False si el directorio ya existía.
    """

    try:
        os.makedirs(path)
        return True
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            return True
        else:
            raise


try:
    create_dir(dir_edit)
except Exception as e:
    print("Error",e)


dir_edit = "com/datas/bard"
archivo = "bard_2.log"
limite = 6 * 8 * 512
logread = "START_LOG\n"
answer = ""
Previous = ""
Footer = ""

contenido = ""

if not os.path.exists(archivo):
  with open(archivo, "w") as f:
    f.write(logread)
    f.close()
else:
  with open(archivo,"r") as f:
    contenido = f.read()
    f.close()

def main(args):

    global answer
    global contenido
    if len(args) < 1:
        print("Bard:",bard_start,bard_start_1)
        return


    if bard_start == False:
        print("Not Bard Key Exists")
        return
    else:

        
        if bard_start_1 == False:
            bard_start_ini(token)
            #print("Bard fue iniciado\n")
            return
        else:
            print("Inicia Bard: ",bard_start)



    if args[0] == "--edit":
        try:
            filename = args[1]
            subprocess.call(["nano", "-w","-i",dir_edit +"/"+ filename])
            return
        except Exception as e:
            print("Error:", e)
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
                with open(dir_edit+"/"+args[1], "r") as f:
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

    if args[0] == "--answer" :
    	if len(args) == 1 :
    	    print("Last answer:\n",answer)
    	    return
    	elif args[1] == "edit":
    	    print("EDIT ANSWER")
    	    try:
    	        with open(dir_edit + "/_answer","w") as f:
    	            f.write(answer)
    	            f.close()
    	        subprocess.call(["nano", "-w", "-i", dir_edit + "/_answer" ])
    	    except Exception as e:
    	        print("ERROR:",e)
    	        return
    	    return
    	else:
    	    print("unknow answer")
    	    return
    	    


    if args[0] == "--load-footer":

        if len(args) < 2:
            print("Faltan argumentos")
            return
        elif len(args) == 2:
            try:
                with open(dir_edit+"/"+args[1], "r") as f:
                    global Footer
                    Footer = f.read().rstrip()
                    print("leido y cargado",args[1])
                    return
            except FileNotFoundError:
                print("\nError:\n",FileNotFoundError)
                return
        return

    if args[0] == "--clear-footer":
        Footer = ""
        print("Footer borrado")
        return

    if args[0] == "--show-footer":
        print("Contenido de Footer:\n",Footer)
        return

    if args[0] == "--log":
        print("READLOG:\n",contenido)
        return



    recortar_archivo(archivo, limite)

    with open(archivo, "r") as f:
      logRead = f.read()

#    print('Args dentro de bard', args)
#    print('Args dentro de bard'," ".join(args))



    cuestion = " ".join(args)
    cuestion =  Previous  + cuestion + Footer
    print("\n*****************\nBard thinking")

    #answer = bard . get_answer ( cuestion)
    #print("RESPONSE:",answer)
    #return

    
    try:
        answer = bard . get_answer(cuestion)["content"]
    except Exception as e:
        print("Error:",e)
        print("Compruebe que su key no ha cambiado")
        return
    
    print("\n Bard say....\n*************************************\n")

  # Recojo el texto a escribir en el archivo.

    print(answer)
    print("\n*********************************************\n")

  # Recorta el archivo si excede el límite.
    recortar_archivo(archivo, limite)

# Agrego el texto al archivo.
    with open(archivo, "a") as f:
      f.write("\n"+cuestion+"\n")
      f.write(answer)
      





def recortar_archivo(archivo, limite):
  global contenido
  with open(archivo, "r") as f:
    contenido = f.read()
  if len(contenido) > limite:
    contenido = contenido[len(contenido) - limite:]
  with open(archivo, "w") as f:
    f.write(contenido)




print('Creado módulo-comando bard y fecha y hora: 2023-09-24 06:17:21.906915')

print("Escribe \"bard --help\" para más información ")











