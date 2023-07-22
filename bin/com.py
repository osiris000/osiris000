
import os , shlex , cnf , auth, fhelp, datetime


# Definir el array de comandos válidos
valid_commands = ["agenda", "install","error"]


def command_line():
    while True:
        com = input(">>> ")

        if not com:
            continue

        args = shlex.split(com)

        if args[0] == "exit":
            exit()
        elif args[0] == "Reset Password":
            auth.makeauth()
        else:
            if len(args) > 1 and args[1] == "help" and args[0] in valid_commands:
                print(fhelp.fhelp(args[0]))
            else:
                if args[0] in valid_commands:
                    if os.path.isfile(args[0] + ".py"):
                        print("Command", args[0], args[1:])
                        # Aquí puedes llamar a funciones relacionadas con el módulo 'agenda' o 'install'
                        try:
                            exec(f"import {args[0]}")
                            module = eval(args[0])
                            module.main(args[1:])  # Pasar los argumentos al módulo importado
                        except ImportError:
                            print(f"Error al importar {args[0]}.py")
                    else:
                        if len(args) > 1 and args[1] == "create":
                            create_module_file(args[0])
                        else:
                            print(f"El archivo {args[0]}.py no existe.")
                else:
                    print("Comando no reconocido:", args)

def create_module_file(module_name):
    with open(f"{module_name}.py", "w") as file:
        file.write(f"def main(args):\n    print('Args dentro de {module_name}', args)\n")
        file.write(f"print('Creado módulo-comando {module_name} y fecha y hora: {datetime.datetime.now()}')\n")


def exit():
	exitf = input("¿ Desea salir del programa ? type 'yes' or 'no' ")
	if exitf == "no" :
		command_line()
	elif exitf == "yes" :
		print("\nEXIT PROGRAM\n")
		auth.access()
	else:
		exit()
