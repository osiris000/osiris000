import subprocess
import threading

def kill_last_process():
    global last_process
    if last_process:
        print("Attempting to terminate last process gracefully:", last_process)
        try:
            last_process.stdin.write(b'q\n')
            last_process.stdin.flush()
            last_process.wait(timeout=5)
        except Exception as e:
            print("Graceful termination failed:", e)
            try:
                last_process.terminate()
                last_process.wait(timeout=5)
            except Exception as e:
                print("Forced termination failed:", e)
        finally:
            last_process = None


def ejecutar_proceso(command, cwd):
    global last_process

    if last_process:
        print("Killing last process:", last_process)
        try:
            last_process.terminate()
            last_process.wait(timeout=5)
        except Exception as e:
            print("Error terminating last process:", e)

    # Abrir el proceso en segundo plano
    process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.PIPE, close_fds=True)
    last_process = process

    # No se inician hilos para manejar stdout ni stderr

    # No se espera a que el proceso termine aquí
    # process.wait()

    print("Process started with PID:", process.pid)



def start_ffmpeg(url):
    global last_process
    global last_url
    global command
    global hls_path
    global hls_progess_file
    kill_last_process()

    command = [
    'ffmpeg', 
    '-loglevel', 'warning',
    '-y', '-re', '-stream_loop', '-1', '-i', url,
    '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-ar', '44100', '-b:a', '128k', '-g', '16', '-sc_threshold', '30',
    '-bsf:v', 'h264_mp4toannexb', '-bsf:a', 'aac_adtstoasc', # Añadir filtros BSF
    '-b:v', '2800k', '-s:v', '854x480', '-maxrate:v', '5600k', '-bufsize:v', '4800k',
    '-ignore_unknown','-strftime','1',
    '-fflags', '+nobuffer', '-flags', 'low_delay', '-max_delay', '0', # Ajustes de latencia
    '-f', 'hls', '-hls_time', '2', '-hls_list_size', '30', '-hls_flags', 'delete_segments+append_list',
    '-master_pl_name', 'master_ultrafast.m3u8',
    '-hls_segment_filename', hls_path+'/segment_%Y%m%d%H%M%S.ts',
    hls_path+'/live.m3u8','-progress',hls_progess_file
]


    print("Executing command in background:", " ".join(command))
    try:
        print("Creating process...")
        thread = threading.Thread(target=ejecutar_proceso, args=(command, '.'))
        thread.start()
        # No se espera a que el hilo termine
        # thread.join()
    except Exception as e:
        print("Error:", e)

    last_url = url
    print(f'Process started for URL: {url}')



# Inicializa variables globales
last_process = None
last_url = ""
command = []
hls_progess_file = "/var/www/osiris000/bin/com/datas/ffmpeg/progress_hls.txt"
hls_path = "/var/www/osiris000/html/app/mitv/channels/main/live-ts"
# Inicia el proceso con la URL deseada
#start_ffmpeg("/var/www/osiris000/bin/com/datas/ffmpeg/viajes-espaciales-4.4-sobrevivir-al-vacío.mp4")

# Puedes llamar a esta función para matar el proceso en cualquier momento
#kill_last_process()
