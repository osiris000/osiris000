

import datetime
import subprocess
import os




def main(args):
    print('Args dentro de {module_name}', args)


    try:
        if args[0] == "--edit":
            subprocess.call(["nano", "-w","-i","com/"+os.path.basename(__file__)])

    except Exception as e:
        print("Se ha producido un error:",e)


print('Creado módulo-comando x y fecha y hora: 2024-02-06 07:24:05.452535')
