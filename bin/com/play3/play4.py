import subprocess
import threading
import os
import signal

def reap_children(signum, frame):
    """ Recolectar cualquier proceso hijo terminado """
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except ChildProcessError:
            break

# Configurar el manejador de la señal SIGCHLD
signal.signal(signal.SIGCHLD, reap_children)

def kill_last_process():
    """ Mata el último proceso, intentando una terminación graciosa y forzada """
    global last_process
    if last_process:
        pid = last_process.pid
        print(f"Attempting to kill process quickly with SIGKILL: {pid}")
        
        try:
            os.kill(pid, signal.SIGKILL)
            last_process.wait(timeout=5)  # Espera breve para permitir limpieza
        except Exception as e:
            print(f"Quick kill failed or process still running: {e}")

        if last_process.poll() is None:  # Si el proceso sigue en ejecución
            print(f"Attempting to terminate process gracefully: {pid}")
            try:
                last_process.stdin.write(b'q\n')
                last_process.stdin.flush()
                last_process.wait(timeout=5)
            except Exception as e:
                print(f"Graceful termination failed: {e}")
                try:
                    last_process.terminate()
                    last_process.wait(timeout=5)
                except Exception as e:
                    print(f"Forced termination failed: {e}")
        else:
            print(f"Process {pid} has already been terminated.")
        
        last_process = None

def ejecutar_proceso(command, cwd):
    """ Ejecuta el proceso en segundo plano """
    global last_process

    if last_process:
        print("Killing last process:", last_process)
        kill_last_process()

    # Abrir el proceso en segundo plano
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE, close_fds=True)
    last_process = process

    print("Process started with PID:", process.pid)

def start_ffmpeg(url):
    """ Inicia el proceso ffmpeg con los parámetros especificados """
    global last_process
    global last_url
    global command
    global hls_path
    global hls_progress_file

    kill_last_process()  # Mata el proceso actual antes de iniciar uno nuevo


    command = [
    'ffmpeg',
    '-loglevel', 'warning',  # Ajusta el nivel de log según tus necesidades
    '-y', '-re', '-stream_loop', '-1', '-i', url,
    '-c:v', 'libx264', '-preset', 'veryfast',  # Ajuste de preset más balanceado
    '-tune', 'zerolatency', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-ar', '44100', '-b:a', '128k',
    '-b:v', '2800k', '-s:v', '854x480', '-maxrate:v', '5000k', '-bufsize:v', '5000k',
    '-g', '20', '-sc_threshold', '50',
    '-ignore_unknown',  # Incluir esta opción para manejar flujos desconocidos
    "-strftime","1", #Habilitar formatos fecha
    '-bsf:v', 'h264_mp4toannexb', '-bsf:a', 'aac_adtstoasc',
    '-hls_time', '2', '-hls_list_size', '30',
    '-hls_flags', '+omit_endlist+delete_segments+append_list',
    '-master_pl_name', 'master_ultrafast.m3u8',
    '-hls_segment_filename', os.path.join(hls_path, 'segment_%Y%m%d%H%M%S.ts'),
    os.path.join(hls_path, 'live.m3u8'), '-progress', hls_progress_file,
    '-fflags', '+nobuffer+igndts+discardcorrupt', '-flags', 'low_delay', '-max_delay', '0'
]


    print("Executing command in background:", " ".join(command))
    try:
        print("Creating process...")
        thread = threading.Thread(target=ejecutar_proceso, args=(command, '.'))
        thread.start()
    except Exception as e:
        print("Error starting process:", e)

    last_url = url
    print(f'Process started for URL: {url}')

# Inicializa variables globales
last_process = None
last_url = ""
command = []
hls_progress_file = "/var/www/osiris000/bin/com/datas/ffmpeg/progress_hls.txt"
hls_path = "/var/www/osiris000/html/app/mitv/channels/main/live-ts"
