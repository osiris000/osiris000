import os
import signal
import sys
import auth
import com

# Ruta del archivo de log
LOG_FILE = "com/datas/osiris_process_log.txt"

def handle_sigchld(signum, frame):
    """Manejador de señal SIGCHLD."""
    with open(LOG_FILE, 'a') as log_file:
        while True:
            try:
                # Esperar a que terminen los procesos hijos y recoger su estado
                pid, status = os.waitpid(-1, os.WNOHANG)
                if pid == 0:
                    # No hay procesos hijos terminados
                    break
                else:
                    log_message = f"Proceso hijo {pid} terminado con estado {status}\n"
                    print(log_message.strip())
                    log_file.write(log_message)
            except ChildProcessError:
                # No hay más procesos hijos
                break

def main():
    """Función principal de la aplicación."""
    # Registrar el manejador de señales para SIGCHLD
    signal.signal(signal.SIGCHLD, handle_sigchld)
    
    try:
        auth.run()
    except Exception as e:
        print("\n\nError:", e)
        print("Line:", e.__traceback__.tb_lineno)
        com.command_line()
    finally:
        print("\nSE HA PRODUCIDO UN ERROR INESPERADO\n")

if __name__ == "__main__":
    main()
