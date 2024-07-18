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

    kill_last_process()

    command = [
    'ffmpeg', 
    '-loglevel', 'verbose',
    '-y', '-re', '-stream_loop', '-1', '-i', url,
    '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-ar', '44100', '-b:a', '128k', '-g', '60', '-sc_threshold', '0',
    '-map', '0:v', '-b:v:0', '800k', '-s:v:0', '426x240', '-maxrate:v:0', '856k', '-bufsize:v:0', '1200k',
    '-b:v:1', '1400k', '-s:v:1', '640x360', '-maxrate:v:1', '2800k', '-bufsize:v:1', '2400k',
    '-b:v:2', '2800k', '-s:v:2', '854x480', '-maxrate:v:2', '5600k', '-bufsize:v:2', '4800k',
    '-b:v:3', '5000k', '-s:v:3', '1280x720', '-maxrate:v:3', '10000k', '-bufsize:v:3', '8000k',
    '-map', '0:a?', '-ignore_unknown','-strftime','1',
    '-f', 'hls', '-hls_time', '2', '-hls_list_size', '20', '-hls_flags', 'delete_segments+append_list',
    '-master_pl_name', 'master_ultrafast.m3u8', '-hls_segment_filename', '/var/www/osiris000/html/app/mitv/channels/main/live-ts/live-ts_%Y%m%d%H%M%S.ts',
    '/var/www/osiris000/html/app/mitv/channels/main/live-ts/live.m3u8'
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

# Inicia el proceso con la URL deseada
#start_ffmpeg("/var/www/osiris000/bin/com/datas/ffmpeg/viajes-espaciales-4.4-sobrevivir-al-vacío.mp4")

# Puedes llamar a esta función para matar el proceso en cualquier momento
#kill_last_process()
