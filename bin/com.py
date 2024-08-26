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

# Ruta del binario de osiris
osiris_bin_path = os.path.abspath(__file__)
osiris_bin_dir = os.path.dirname(osiris_bin_path)


use_command = ""
set_com=""
def_editor="subl"

# Nombre del entorno virtual
nombre_venv = "osiris_env"

# Comandos válidos
valid_commands = ["hls", "shell", "blockchain", "scanip", "sniff", "config", "fdev", "agenda", "install", "error", "chatgpt", "bard"]

# Diccionario para almacenar información sobre los módulos y sus funciones main
module_info = {}
loaded_modules = {}

# Archivo de historial
history_file = cnf.history_file

# Cargar historial de comandos
try:
    with open(history_file, "rb") as file:
        command_history = pickle.load(file)
except (FileNotFoundError, EOFError):
    command_history = []

# Guardar historial de comandos
def save_command_history():
    with open(history_file, "wb") as file:
        pickle.dump(command_history, file)

# Función para habilitar y exportar el entorno virtual
def habilitar_y_exportar_venv(nombre_venv):
    global osiris_bin_dir
    try:
        env_vars = subprocess.Popen(["printenv | grep -i osiris"], stdout=subprocess.PIPE, text=True, shell=True).communicate()[0]
        print(env_vars)
    except Exception as e:
        print("Error:", e)
    print("PYTHONPATH:", " | ".join(sys.path))

# Función para verificar la declaración de una función en un módulo
def check_function_declaration(module_name, function_name):
    if module_name in module_info:
        return module_info[module_name].get(function_name, None)

    try:
        with open(f"com/{module_name}.py", "r") as file:
            source_code = file.read()
        module_ast = ast.parse(source_code)

        main_function_found = None

        for node in ast.walk(module_ast):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                main_function_found = True

                num_arguments = len(node.args.args) if node.args else 0
                main_function_one_argument = num_arguments == 1

                break

        module_info[module_name] = {}
        module_info[module_name][function_name] = main_function_found and main_function_one_argument

        return main_function_found and main_function_one_argument

    except ImportError:
        return None

# Validación de funciones
def is_valid_function(function):
    return isinstance(function, (types.FunctionType, types.MethodType))

# Verificar si una función tiene un solo argumento
def has_single_argument(function):
    return len(inspect.signature(function).parameters) == 1

# Limpiar datos de comando
def clear_command_data(command_name):
    if command_name in module_info:
        module_info.pop(command_name)

# Cargar un módulo
def load_module(module_name):
    module_path = os.path.join("com", module_name + ".py")
    if os.path.isfile(module_path):
        main_function = check_function_declaration(module_name, "main")
        if main_function is not None and main_function:
            try:
                module_spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                loaded_modules[module_name] = module  # Almacenamos el módulo en el diccionario de módulos cargados
                return module
            except ImportError as er3:
                print(f"Error al importar {module_name}.py: {er3}")
                print("Verifique los imports del comando en su archivo. Puede montarlo y usar el modificador --edit")
                return None
        else:
            print(f"La función 'main' en {module_name}.py no está declarada correctamente o no tiene un solo argumento.")
            return None
    else:
        print(f"El archivo {module_name}.py no existe en el directorio 'com'.")
        return None

# Ejecutar el comando del módulo cargado
def execute_module_command(module, args):
    if hasattr(module, "main") and is_valid_function(module.main):
        if has_single_argument(module.main):
            module.main(args[1:])
        else:
            print(f"La función 'main' en {module.__name__}.py debe recibir exactamente un argumento.")
    else:
        print(f"La función 'main' no está definida correctamente en {module.__name__}.py")

# Bucle principal del CLI
def command_line():
    global def_editor, use_command, set_com, nombre_venv

    signal.signal(signal.SIGINT, CTRL_C)
    readline.set_history_length(cnf.history_com_size)
    readline.clear_history()
    for command in command_history:
        readline.add_history(command)

    while True:
        try:
            com = input(">>> " + use_command).strip()
            if not com:
                continue

            command_history.append(com)
            save_command_history()
            args = shlex.split(com)

            if set_com and args[0] != set_com:
                args.insert(0, set_com)

            if args[0] == "--reload":
                # Código de recarga del entorno
                continue

            handle_command(args)

        except Exception as e:
            print("ERROR:", e)

# Manejo de comandos
def handle_command(args):
    global use_command, set_com

    if args[0] == "mount" and len(args) > 1:
        if args[1] not in valid_commands:
            valid_commands.append(args[1])
            print(f"Montado: {args[1]}")
        else:
            print(f"El comando: {args[1]} ya está montado.")
        args[0] = "use"

    if args[0] == "use" and len(args) == 2:
        use_command = args[1] + "> "
        set_com = args[1]
    elif len(args) >= 2 and args[1] == "use":
        use_command = "" if len(args) == 2 else args[2] + "> "
        set_com = "" if len(args) == 2 else args[2]
    elif args[0] == "--venv":
        habilitar_y_exportar_venv(nombre_venv)
    elif args[0] == "exit":
        exit_program()
    elif args[0] == "Reset_Password":
        auth.makeauth()
    elif args[0] not in valid_commands:
        print(f"Comando: {args[0]} inválido")
    elif len(args) > 1 and args[1] == "--reset":
        clear_command_data(args[0])
        loaded_modules.pop(args[0], None)
        print(f"Módulo-comando {args[0]} desmontado")
    elif len(args) > 1 and args[1] == "--edit":
        edit_command(args[0])
    else:
        if len(args) > 1 and args[1] == "--help" and args[0] in valid_commands:
            print(fhelp.fhelp(args[0]))
        else:
            execute_command(args)

# Editar un comando
def edit_command(command):
    global def_editor
    ed = os.path.join("com", command + ".py")
    if os.path.isfile(ed):
        if def_editor in subprocess.check_output(["ps", "-aux"]).decode():
            subprocess.call([def_editor, ed])
        else:
            subprocess.call([def_editor, ed])
    else:
        print("No se encuentra el módulo a editar, use create [comando] --create para crear uno nuevo")

# Ejecutar un comando cargando el módulo si es necesario
def execute_command(args):
    if args[0] in valid_commands:
        module = loaded_modules.get(args[0]) or load_module(args[0])
        if module:
            execute_module_command(module, args)

# Salir del programa
def exit_program():
    exit_decision = input("\n¿Desea salir del programa? Escriba 'yes' o 'no': ")
    if exit_decision.lower() == "yes":
        print("\nEXIT PROGRAM\n")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        auth.access()
    elif exit_decision.lower() == "no":
        return
    else:
        exit_program()

# Manejo de señal Ctrl+C
def CTRL_C(signal, frame):
    print("\nEscriba 'exit' para salir")
    return
