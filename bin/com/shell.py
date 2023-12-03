import subprocess


def main(args):
    print('Args dentro de shell', args)
    try:
        subprocess.call(args)
    except Exception as e:
        print("ERROR:",e)
    return


print('Creado módulo-comando shell y fecha y hora: 2023-11-28 12:12:24.596228')
