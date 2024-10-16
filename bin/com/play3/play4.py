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
    """ Mata el último proceso """
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


def listar_procesos():
     print("FUTURE PLAY 5")


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


def start_ffmpeg(url,com=""):
    """ Inicia el proceso ffmpeg con los parámetros especificados """
    global last_process
    global last_url
    global command
    global hls_path
    global hls_progress_file
    global ffcom_metadata
    kill_last_process()  # Mata el proceso actual antes de iniciar uno nuevo


    command = [
    'ffmpeg',
    '-y',
    '-re',
    '-loglevel', 'warning',
    '-f', 'lavfi', '-i', 'color=c=black:s=854x480',
    '-stream_loop', '-1', '-i', url,  # Aplicar stream_loop aquí
    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
    '-af', 'aresample=async=1,loudnorm=I=-16:TP=-1.5:LRA=11',
    '-filter_complex', '[1:v]scale=854:480[scaled];[0:v][scaled]overlay=shortest=1',
    '-map', '0:v',
    '-map', '1:a',
    '-c:v', 'libx264', '-preset', 'ultrafast',
    '-tune', 'zerolatency', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-ar', '44100', '-b:a', '128k',
    '-b:v', '2500k', '-s:v', '854x480', '-maxrate:v', '3000k', '-bufsize:v', '5000k',
    '-g', '20', '-sc_threshold', '50',
    '-ignore_unknown',
    '-strftime', '1',
    '-bsf:v', 'h264_mp4toannexb', '-bsf:a', 'aac_adtstoasc',
    '-f','hls',
    '-hls_time', '3', '-hls_list_size', '30',
    '-segment_list_flags','+live',
    '-hls_flags', '+omit_endlist+delete_segments+append_list',
    '-master_pl_name', 'master_ultrafast.m3u8',
    '-hls_segment_filename', os.path.join(hls_path, '%Y%m%d%H%M%S.ts'),
    os.path.join(hls_path, 'live.m3u8'), '-progress', hls_progress_file,
    '-fflags', '+genpts+igndts+discardcorrupt', '-flags', 'low_delay', '-max_delay', '0',
    '-reconnect', '1', '-reconnect_streamed', '1', '-reconnect_delay_max', '2', '-metadata', ffcom_metadata
]

    # si se recibe el comando se sustituye command
    if com:
        command = com

    print("Executing command in background:", " ".join(command))
    try:
        print("Creating process...")
        thread = threading.Thread(target=ejecutar_proceso, args=(command, '.'))
        thread.start()
    except Exception as e:
        print("Error starting process:", e)

    last_url = url
    print(f"\n Process started for URL: {url}\n")

# Inicializa variables globales
last_process = None
last_url = ""
command = []
hls_progress_file = "/var/www/osiris000/bin/com/datas/ffmpeg/progress_hls.txt"
hls_default_input = "/var/www/osiris000/bin/com/datas/ffmpeg/intro.mp4"
hls_path = "/var/www/osiris000/html/app/mitv/channels/main/live-ts"
ffcom_metadata = "text=osiristv-hls-main"

