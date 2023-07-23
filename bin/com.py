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

# Definir el array de comandos válidos
valid_commands = ["agenda", "install", "error","chatgpt"]

# Diccionario para almacenar información sobre los módulos y sus funciones main
module_info = {}
loaded_modules = {}
# Archivo para almacenar el historial de comandos
history_file = cnf.PATH_DAT + "/command_history.pkl"

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


def command_line():

    # Configurar el historial para permitir la navegación con las flechas del cursor
    readline.set_history_length(cnf.history_com_size)  # Límite de longitud del historial
    readline.clear_history()  # Limpiar el historial actual
    for command in command_history:
        readline.add_history(command)  # Agregar los comandos al historial


    com = input(">>> ")

    if not com:
        command_line()  # Llamada recursiva si no se proporcionó ningún comando


    # Agregar el comando ingresado al historial
    command_history.append(com)
    # Guardar el historial en el archivo
    save_command_history()


    args = shlex.split(com)
    if args[0] == "exit":
        exit_program()
    elif args[0] == "Reset_Password":
        auth.makeauth()
    elif args[0] not in valid_commands:
        print("Comando no reconocido:", args)
        command_line()
        return
    elif len(args) > 1 and args[1] == "reset":
        clear_command_data(args[0])
        loaded_modules.pop(args[0], None)  # Eliminamos el módulo del diccionario de módulos cargados
        command_line()  # No se ejecuta el comando después de limpiar los datos
        return;
    else:
        if len(args) > 1 and args[1] == "help" and args[0] in valid_commands:
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
                                            print(f"La función 'main' en {args[0]}.py debe recibir exactamente un argumento.")
                                    else:
                                        print(f"La función 'main' no está definida correctamente en {args[0]}.py")
                                except ImportError:
                                    print(f"Error al importar {args[0]}.py")
                            else:
                                print(f"La función 'main' en {args[0]}.py debe recibir exactamente un argumento.")
                        else:
                            print(f"La función 'main' no está declarada en {args[0]}.py")
                    else:
                        if len(args) > 1 and args[1] == "create":
                            create_module_file(args[0])
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

    command_line()  # Llamada recursiva para continuar con el siguiente comando


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

def create_module_file(module_name):
    with open(f"com/{module_name}.py", "w") as file:
        file.write(f"def main(args):\n    print('Args dentro de {module_name}', args)\n")
        file.write(f"print('Creado módulo-comando {module_name} y fecha y hora: {datetime.datetime.now()}')\n")

def clear_command_data(command_name):
    if command_name in module_info:
        module_info.pop(command_name)
        print(f"Datos del comando '{command_name}' eliminados.")
    else:
        print(f"No hay datos para el comando '{command_name}'.")




def exit_program():
    exit_decision = input("¿ Desea salir del programa ? type 'yes' or 'no' ")
    if exit_decision.lower() == "no" :
        command_line()
    elif exit_decision.lower() == "yes" :
        print("\nEXIT PROGRAM\n")
        auth.access()
    else:
        exit_program()
