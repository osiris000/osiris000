import sys
import importlib

def dynmodule(nombre_modulo, as_=""):
    print("Core MSG:")
    try:
        if nombre_modulo in sys.modules:
            print(f"Desmontando el módulo '{nombre_modulo}'...")
            del sys.modules[nombre_modulo]

        print(f"Montando el módulo '{nombre_modulo}'...")
        mod = importlib.import_module(nombre_modulo)

        # En lugar de modificar globals(), crea un nuevo nombre en el scope local
        if as_:  # Solo crea el alias si se proporciona
            globals()[as_] = mod
            print(f"Módulo '{nombre_modulo}' importado como {as_}")
            print(f"Use core.{as_}")
        else:
            globals()[nombre_modulo] = mod #Por defecto utiliza el nombre del modulo como alias
            print(f"Módulo '{nombre_modulo}' importado.")

    except ImportError as e:  # Especificar ImportError para mejor manejo de errores
        print(f"ERROR al importar el módulo '{nombre_modulo}':\n{e}")
    except Exception as e:
        print(f"ERROR inesperado al cargar el módulo '{nombre_modulo}':\n{e}")
  



dynmodule('lib.multiprocess',"mp")
def multiprocess(obj):
	mp.multiprocess(obj)


dynmodule('lib.processstart',"ps")
def multiprocess(obj):
	mp.multiprocess(obj)