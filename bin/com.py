import auth
import importlib.util
import fhelp
import os
import shlex
import types
import ast
import datetime
import inspect
import readline
import pickle
import cnf
import signal
import lib.osiris.common as common
import sys
import subprocess
import time

def habilitar_y_exportar_venv(nombre_venv):


    # Comando para habilitar el entorno virtual
    comando_habilitar = f"sh source com/{nombre_venv}/bin/activate"

    # Ejecutar el comando para habilitar el entorno virtual

    try:
        subprocess.run(comando_habilitar, shell=True)
        print("Init com:",comando_habilitar)
    except Exception as e:
        print("Error habilitando:",e)


    # Exportar el entorno virtual
    comando_exportar = f"bash eval export PYTHONPATH=\".:com/{nombre_venv}lib/python3.9/site-packages\""

    # Ejecutar el comando para exportar el entorno virtual

    try:
        subprocess.run(comando_exportar, shell=True)
        print("Init com:",comando_exportar)
    except Exception as e:
        print("Error Exportando:",e)

    if os.environ.get("PYTHONPATH"):
        print("##########")
        #return
    else:
    	print("..........")

# Nombre de tu entorno virtual
nombre_venv = "osiris_env"

# Llamada a la función para habilitar y exportar el entorno virtual

common.f()

# Definir el array de comandos válidos
valid_commands = ["hls","shell","blockchain","scanip","sniff","config","fdev","agenda", "install", "error","chatgpt","bard"]

# Diccionario para almacenar información sobre los módulos y sus funciones main
module_info = {}
loaded_modules = {}
# Archivo para almacenar el historial de comandos
history_file = cnf.history_file

try:
    # Intentar cargar el historial de comandos desde el archivo
    with open(history_file, "rb") as file:
        command_history = pickle.load(file)

except (FileNotFoundError, EOFError):
    # Si el archivo no existe o está vacío, crear una nueva lista
    command_history = []


# Función para guardar el historial en el archivo
def save_command_history():
    with open(history_file, "wb") as file:
        pickle.dump(command_history, file)


use_command = ""
set_com = ""
def_editor = "subl";


def command_line():
    global def_editor
    global use_command
    global set_com
    global nombre_venv
    signal.signal(signal.SIGINT,CTRL_C)
    # Configurar el historial para permitir la navegación con las flechas del cursor
    readline.set_history_length(cnf.history_com_size)  # Límite de longitud del historial
    readline.clear_history()  # Limpiar el historial actual
    for command in command_history:
        readline.add_history(command)  # Agregar los comandos al historial
#    time.sleep(0.3)
    try:
        com = input(">>> "+use_command)
        com = com.lstrip()
        if com == "":
            command_line()
            return
    except Exception as e:
        print("ERROR 1:",e)


    if not com:
        try:
            command_line()  # Llamada recursiva si no se proporcionó ningún comando
        except Exception as e:
            print("ERROR 2:",e)

    # Agregar el comando ingresado al historial
    command_history.append(com)
    # Guardar el historial en el archivo
    save_command_history()



    args = shlex.split(com)



    if set_com:
        if args[0] != set_com:
            args.insert(0,set_com)

    if args[0] == "--venv":
        habilitar_y_exportar_venv(nombre_venv)
        print("Activando venv:",nombre_venv)
        command_line()

    if args[0] == "mount" and len(args) > 1:
        if args[1] not in valid_commands:
            valid_commands.append(args[1])
            print("Montado:"+args[1])
            args[0] = "use"
        else:
            print("El comando:"+args[1]+":está montado")
            args[0] = "use"
        print("exit mount")


    if args[0] == "use" and len(args) == 2:
        use_command = args[1]+"> "
        set_com = args[1]
        command_line()
        return
    elif len(args) == 2 and args[1] == "use":
        use_command = ""
        set_com = ""
        command_line()
        return
    elif len(args) == 3 and args[1] == "use":
        use_command = args[2]+"> "
        set_com = args[2]
        command_line()
        return
    elif args[0] == "exit":
        exit_program()
    elif args[0] == "Reset_Password":
        auth.makeauth()
    elif args[0] not in valid_commands:
        print(f"Comando: {args[0]} , inválido")
        command_line()
        return
    elif len(args) > 1 and args[1] == "--reset":
        clear_command_data(args[0])
        loaded_modules.pop(args[0], None)  # Eliminamos el módulo del diccionario de módulos cargados
        print("Módulo-comando "+args[0]+" desmontado")
        command_line()  # No se ejecuta el comando después de limpiar los datos
    elif len(args) > 1 and args[1] == "--edit":

        ed = "com/"+ args[0] + ".py"

        if os.path.isfile(ed):
        # Comprobar si Sublime Text ya está abierto
            if "subl" in subprocess.check_output(["ps", "-aux"]).decode():
            # Si ya está abierto, enviar el comando "open" a la instancia existente
                subprocess.call([def_editor, ed])
            else:
            # Si no está abierto, iniciar Sublime Text y abrir el archivo
                subprocess.call([def_editor, ed])
        else:
            print("No se encuentra el módulo a editar, use create [comando] --create para crear uno nuevo")
        command_line()
    else:
        if len(args) > 1 and args[1] == "--help" and args[0] in valid_commands:
            print(fhelp.fhelp(args[0]))
        else:
            if args[0] in valid_commands:
                if args[0] not in loaded_modules:
                    module_path = os.path.join("com", args[0] + ".py")
                    if os.path.isfile(module_path):
                        main_function = check_function_declaration(args[0], "main")
                        if main_function is not None:
                            if main_function:
                                try:
                                    module_spec = importlib.util.spec_from_file_location(args[0], module_path)
                                    module = importlib.util.module_from_spec(module_spec)
                                    module_spec.loader.exec_module(module)
                                    loaded_modules[args[0]] = module  # Almacenamos el módulo en el diccionario de módulos cargados

                                    if hasattr(module, "main") and is_valid_function(module.main):
                                        if has_single_argument(module.main):
                                            module.main(args[1:])
                                        else:
                                            print(f"La función 'main' en {args[0]}.py debe recibir exactamente argumentos.")
                                    else:
                                        print(f"La función 'main' no está definida correctamente en {args[0]}.py")
                                except ImportError as er3:
                                    print(f"Error al importar {args[0]}.py")
                                    print("Error:",er3)
                                    print("Faltan dependencias python (pip)")
                                    print("Verifique los imports del comando en su archivo. Puede montarlo y usar el modificador --edit")
                                    print("Compruebe que se ha activado y exportado el entorno virtual")
                                    print("use el comando shell para instalar las dependencias con pip manualmente o desde la instalación de osiris")
                                    print(f"pruebe >>>shell> pip install {er3.name}")
                            else:
                                print(f"La función 'main' en {args[0]}.py debe recibir exactamente un argumento.")
                        else:
                            print(f"La función 'main' no está declarada en {args[0]}.py")
                    else:
                        if len(args) > 1 and args[1] == "--create":
                            print("Use comando create")
                            #create_module_file(args[0])
                        else:
                            print(f"El archivo {args[0]}.py no existe en el directorio 'com'.")
                else:
                    module = loaded_modules[args[0]]
                    if hasattr(module, "main") and is_valid_function(module.main):
                        if has_single_argument(module.main):
                            module.main(args[1:])
                        else:
                            print(f"La función 'main' en {args[0]}.py debe recibir exactamente un argumento.")
                    else:
                        print(f"La función 'main' no está definida correctamente en {args[0]}.py")
    try:
        command_line()  # Llamada recursiva para continuar con el siguiente comando
    except Exception as e:
        print("ERROR 3:",e)

# resto codigo


def check_function_declaration(module_name, function_name):
    if module_name in module_info:
        return module_info[module_name].get(function_name, None)

    try:
        with open(f"com/{module_name}.py", "r") as file:
            source_code = file.read()
        module_ast = ast.parse(source_code)

        main_function_found = None  # Inicializar en None

        for node in ast.walk(module_ast):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                main_function_found = True

                # Contar los argumentos en la función 'main'
                num_arguments = len(node.args.args) if node.args else 0
                main_function_one_argument = num_arguments == 1

                break

        module_info[module_name] = {}
        module_info[module_name][function_name] = main_function_found and main_function_one_argument

        return main_function_found and main_function_one_argument

    except ImportError:
        return None

def is_valid_function(function):
    return (isinstance(function, types.FunctionType) or
            isinstance(function, types.MethodType))

def has_single_argument(function):
    return len(inspect.signature(function).parameters) == 1

def clear_command_data(command_name):
    if command_name in module_info:
        module_info.pop(command_name)

def exit_program():
    exit_decision = input("\n¿ Desea salir del programa ? type 'yes' or 'no' ")
    if exit_decision.lower() == "no" :
        command_line()
    elif exit_decision.lower() == "yes" :
        print("\nEXIT PROGRAM\n")
        signal.signal(signal.SIGINT,signal.SIG_DFL)
        auth.access()
    else:
        exit_program()



def CTRL_C(signal,frame):
    print("Excriba “exit” para salir")
#    command_line()
    return




#start_print_loop()
