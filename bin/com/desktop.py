#import osiris2
import datetime
import subprocess
import os
import sys
import importlib
import time
import signal

usuario = os.getlogin()



apps = ["dsk1","dsk2","dsk3",
"dsk4","dsk5","dsk6","dsk7",
"ipinfo","localnet","gemini"]


def recargar_modulo(nombre_modulo):
    # Si el módulo ya está cargado, lo eliminamos
    if nombre_modulo in sys.modules:
        print(f"Desmontando el módulo '{nombre_modulo}'...")
        del sys.modules[nombre_modulo]
    
    # Volvemos a importar el módulo y lo retornamos
    print(f"Montando el módulo '{nombre_modulo}'...")
    mod = importlib.import_module(nombre_modulo)
    
    # Asignamos el módulo importado al espacio de nombres global
    globals()[nombre_modulo] = mod

# Ejemplo: Recargar el módulo 'osiris2'
recargar_modulo('osiris2')
# Ahora puedes usar 'osiris2' como antes


# desktop.py



def mostrar_man():
    """Muestra la documentación del módulo."""
    print(osiris2.man)

def editar_script():
    """Edita el script actual usando nano."""
    subprocess.call(["nano", "-w", "-i", "com/" + os.path.basename(__file__)])

def iniciar_multiprocess(obj):
    """Inicia un proceso con los parámetros dados."""
    try:
        osiris2.multiprocess(obj)
        print("Proceso iniciado con los siguientes datos:")
        print(obj)
    except ValueError as e:
        print(f"Error al iniciar el proceso: {e}")

def listar_procesos():
    """Lista todos los procesos y sus detalles."""
    procesos = osiris2.process_handlers
    if not procesos:
        print("No hay procesos en ejecución.")
        return

    for nombre, handler in procesos.items():
        print(f"Nombre del proceso: {handler.name}")
        print(f"PID: {handler.pid}")  # Mostrar el PID
        print(f"En ejecución: {'Sí' if handler.is_running() else 'No'}")
        print(f"Metadata: {handler.metadata}\n")


def kill(numero):
    """Mata el proceso especificado por el número (PID) si está activo."""
    procesos = osiris2.process_handlers  # Asumiendo que este es un diccionario de procesos

    # Buscar el proceso por PID
    handler = None
    for nombre, proc_handler in procesos.items():
        print(f"Comprobando proceso: {nombre} con PID: {proc_handler.pid}")  # Mensaje de depuración
        if proc_handler.pid == numero:
            handler = proc_handler
            break

    if handler is None or not handler.is_running():
        print(f"No se encontró un proceso activo con PID {numero}.")
        return

    try:
        # Intentar enviar SIGTERM (más suave)
        os.kill(numero, signal.SIGTERM)
        print(f"Enviando SIGTERM al proceso con PID {numero}.")
        # Esperar un poco para que el proceso tenga tiempo de terminar
        time.sleep(1)

        # Verificar si el proceso aún está en ejecución
        if os.path.exists(f"/proc/{numero}"):
            print(f"Proceso con PID {numero} no se detuvo, intentando con SIGKILL.")
            os.kill(numero, signal.SIGKILL)  # Enviar SIGKILL (más agresivo)
            print(f"Enviando SIGKILL al proceso con PID {numero}.")
    except ProcessLookupError:
        print(f"Proceso con PID {numero} no se encontró.")
    except PermissionError:
        print(f"No se tiene permiso para matar el proceso con PID {numero}.")
    except Exception as e:
        print(f"Error al intentar matar el proceso con PID {numero}: {e}")



def kill_all():
    """Lista todos los procesos y sus detalles, y los termina si están en ejecución."""
    procesos = osiris2.process_handlers  # Asumiendo que este es un diccionario de procesos
    if not procesos:
        print("No hay procesos en ejecución.")
        return

    # Lista de PIDs para poder matar los procesos
    pids_to_kill = []

    print("Lista de procesos en ejecución:")
    for nombre, handler in procesos.items():
        print(f"Nombre del proceso: {handler.name}")
        print(f"PID: {handler.pid}")  # Mostrar el PID
        print(f"En ejecución: {'Sí' if handler.is_running() else 'No'}")
        print(f"Metadata: {handler.metadata}\n")

        # Si el proceso está en ejecución, lo agregamos a la lista de PIDs a matar
        if handler.is_running():
            pids_to_kill.append(handler.pid)

    # Intentar matar todos los procesos en ejecución
    for pid in pids_to_kill:
        try:
            # Intentar enviar SIGTERM (más suave)
            os.kill(pid, signal.SIGTERM)  
            print(f"Enviando SIGTERM al proceso con PID {pid}.")
            # Esperar un poco para que el proceso tenga tiempo de terminar
            time.sleep(1)  

            # Verificar si el proceso aún está en ejecución
            if os.path.exists(f"/proc/{pid}"):
                print(f"Proceso con PID {pid} no se detuvo, intentando con SIGKILL.")
                os.kill(pid, signal.SIGKILL)  # Enviar SIGKILL (más agresivo)
                print(f"Enviando SIGKILL al proceso con PID {pid}.")
        except ProcessLookupError:
            print(f"Proceso con PID {pid} no se encontró.")
        except PermissionError:
            print(f"No se tiene permiso para matar el proceso con PID {pid}.")
        except Exception as e:
            print(f"Error al intentar matar el proceso con PID {pid}: {e}")



def main(args):
    global usuario
    timestamp = int(time.time())
    print('Args input {timestamp}:', args)

    try:
        if args[0] == "man":
            mostrar_man()
        elif args[0] == "---edit":
            editar_script()
        elif args[0] == "killall":
            kill_all()
        elif args[0] == "kill":
            if len(args) > 1:
                try:
                    int(args[1])
                except:
                    print("Parámetro PID debe ser un número")
                    return
                kill(int(args[1]))
        elif args[0] in apps:
            args_0 = args[0]
            args.pop(0)
            lcom = " ".join(args)
            obj = {
                "mode": "bg",  # Cambia a "fixed" si deseas el comportamiento por defecto
                "name": None,  # Se generará automáticamente si es None
                "com": ["python3", "com/dsk/"+args_0+".py"] + args,  # Asegúrate de que este comando sea válido
                "metadata": {"user": usuario,
                            "time_start":timestamp,
			    "command":args_0 +" "+lcom
                            }
            }
            iniciar_multiprocess(obj)
        elif args[0] == "com":
            args.pop(0) 
            obj = {
                "mode": "bg",  # Cambia a "fixed" si deseas el comportamiento por defecto
                "name": None,  # Se generará automáticamente si es None
                "com": args,  # Asegúrate de que este comando sea válido
                "metadata": {"user": usuario,
                            "time_start":timestamp,
                            "command":args
                            }
            }


            print(obj)
            iniciar_multiprocess(obj)

            #subprocess.call(["python3", "com/dsk/dsk2.py"])
            print("FREE ARG")
        elif args[0] == "XARG":
            #subprocess.call(["python3", "com/dsk/dsk2.py"])
            print("FREE ARG")
        elif args[0] == "list_processes":
            listar_procesos()  # Comando para listar procesos
        elif args[0] == "show_handlers":
            print("Contenido de process_handlers:")
            print(osiris2.process_handlers)

    except Exception as e:
        print("Se ha producido un error:", e)



print(osiris2.info)
print('Creado módulo-comando desktop y fecha y hora: 2024-09-27 08:55:29.392217')
