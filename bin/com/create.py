import datetime

def main(args):
    print('Args dentro de create', args)
    if len(args) == 2 and args[1] == "--create":
    	#create_module_file(args[0])
    	create_module_file(args[0])
    	print("Creado módulo:",args[0])
    	#comprobar que se haya creado el archivo
    	#posibilidad de editarlo



def create_module_file(module_name):
	#comprobar si existe ruta
	#si no existe se crea el módulo por defecto
    with open(f"com/__{module_name}.py", "w") as file:
        file.write(f"def main(args):\n    print('Args dentro de {module_name}', args)\n")
        file.write(f"print('Creado módulo-comando {module_name} y fecha y hora: {datetime.datetime.now()}')\n")



print('Creado módulo-comando create y fecha y hora: 2023-09-26 08:34:08.790010')