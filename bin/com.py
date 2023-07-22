
import os , shlex , cnf , auth, fhelp, datetime, inspect, ast, types


# Definir el array de comandos válidos
valid_commands = ["agenda", "install","error"]



# Diccionario para almacenar información sobre los módulos y sus funciones main
module_info = {}


def command_line():
    com = input(">>> ")

    if not com:
        command_line()  # Llamada recursiva si no se proporcionó ningún comando

    args = shlex.split(com)

    if args[0] == "exit":
        exit()
    elif args[0] == "Reset_Password":
        auth.makeauth()
    elif len(args) > 1 and args[1] == "clear":
        clear_command_data(args[0])
    else:
        if len(args) > 1 and args[1] == "help" and args[0] in valid_commands:
            print(fhelp.fhelp(args[0]))
        else:
            if args[0] in valid_commands:
                if os.path.isfile(args[0] + ".py"):
                    main_function = check_function_declaration(args[0], "main")
                    if main_function is not None:
                        if main_function:
                            try:
                                exec(f"import {args[0]}")
                                module = eval(args[0])
                                if hasattr(module.main, "__call__") and callable(module.main):
                                    module.main(args[1:])
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
                        print(f"El archivo {args[0]}.py no existe.")
            else:
                print("Comando no reconocido:", args)

    command_line()  # Llamada recursiva para continuar con el siguiente comando


def check_function_declaration(module_name, function_name):
    if module_name in module_info:
        return module_info[module_name].get(function_name, None)

    try:
        with open(f"{module_name}.py", "r") as file:
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

def create_module_file(module_name):
    with open(f"{module_name}.py", "w") as file:
        file.write(f"def main(args):\n    print('Args dentro de {module_name}', args)\n")
        file.write(f"print('Creado módulo-comando {module_name} y fecha y hora: {datetime.datetime.now()}')\n")

def clear_command_data(command_name):
    if command_name in module_info:
        module_info.pop(command_name)
        print(f"Datos del comando '{command_name}' eliminados.")
    else:
        print(f"No hay datos para el comando '{command_name}'.")




def exit():
	exitf = input("¿ Desea salir del programa ? type 'yes' or 'no' ")
	if exitf == "no" :
		command_line()
	elif exitf == "yes" :
		print("\nEXIT PROGRAM\n")
		auth.access()
	else:
		exit()
