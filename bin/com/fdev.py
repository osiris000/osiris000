import time
import datetime
import subprocess
import os
import threading
import signal
import sys
import multiprocessing
import lib.ffmpeg
import random


prueba = False
estado_proceso = False
pid_queue = multiprocessing.Queue()  # Cola compartida para almacenar el PID del proceso hijo
pid_proceso = None
yt_last_args = False

def funcion_proceso(args):
    global estado_proceso
    try:
        proceso = multiprocessing.Process(target=_funcion_interna,args=(args,))
        proceso.start()
        global pid_proceso
        pid_proceso = pid_queue.get()  # Obtenemos el PID del proceso hijo desde la cola
        proceso.join()  # Esperamos a que el proceso hijo se inicie completamente
        print("Iniciado proceso PID:", pid_proceso)  # Esto debería imprimir el valor actualizado
    except Exception as e:
        print("Error al iniciar el proceso:", e)
    finally:
        estado_proceso = True

def _funcion_interna(args):
    try:
        proceso = subprocess.Popen(args,bufsize=0,close_fds=True,restore_signals=True,shell=False,stdin=None,stdout=None,stderr=subprocess.DEVNULL)
        pid_proceso = proceso.pid
        pid_queue.put(pid_proceso)  # Pasamos el PID del proceso hijo a la cola
        print("Iniciado Hilo", pid_proceso)
    except Exception as e:
        print("Error Popen:", e)
        return

def detener_proceso():
    global estado_proceso
    global pid_proceso
    if estado_proceso:
        try:
            if pid_proceso is not None:
                os.kill(pid_proceso, signal.SIGKILL)
                estado_proceso = False
                print("Detenido proceso PID:", pid_proceso)
                pid_proceso = None
        except Exception as e:
            print("Error al detener el proceso:", e)
    else:
        print("No existe proceso abierto")



def main(args):

    yt_args = False
    global estado_proceso
    global hilo_proceso, pid_proceso
    global yt_last_args
    #global yt_start, yt_input_concat, yt_codecs, yt_output
    #global yt_input_start, yt_screen_input, yt_screen_input2, yt_v4l2_screen
    #global yt_default_progress_file, MAX_LPF


    profiles = {
    "perfil1": {
        "preset": "ultrafast",
        "vbr":"500k",
        "buffsize":"1000k"
    },
    "perfil2": {
        "preset": "slow"
    }
}

# Seleccionar un perfil
    perfil_actual = "perfil1"
    profile_name = perfil_actual

# Obtener el valor de "preset" para el perfil seleccionado


#preset
    yt_default_preset = profiles[profile_name].get("preset") if "preset" in profiles[profile_name] else "ultrafast"
    if yt_default_preset != None:
        yt_default_preset = ["-preset",yt_default_preset]
    else:
        yt_default_preset = ""

#screen
    yt_default_screen = profiles[profile_name].get("screen") if "screen" in profiles[profile_name] else "856x480"
    if yt_default_screen != None:
        yt_default_screen = ["-s",yt_default_screen]
    else:
        yt_default_screen = ""


#bufersize
    yt_default_buffer_size = profiles[profile_name].get("bufsize") if "bufsize" in profiles[profile_name] else "1500k"
    if yt_default_buffer_size != None:
        yt_default_buffer_size = ["-bufsize",yt_default_buffer_size]
    else:
        yt_default_buffer_size = ""


#VideoBitRate (vbr)
    yt_default_vbr = profiles[profile_name].get("vbr") if "vbr" in profiles[profile_name] else "1500k"
    if yt_default_vbr != None:
        yt_default_vbr = ["-b:v",yt_default_vbr]
    else:
        yt_default_vbr = ""


#AudioBitRate (abr)
    yt_default_abr = profiles[profile_name].get("abr") if "abr" in profiles[profile_name] else "128k"
    if yt_default_abr != None:
        yt_default_abr = ["-b:a",yt_default_abr]
    else:
        yt_default_abr = ""



    yt_default_audio_bitrate = "128k"
    yt_default_output_url = "rtmp://a.rtmp.youtube.com/live2/svvb-yk73-asfv-0krs-5v57"
    yt_default_progress_file = "com/datas/ffmpeg/progress_process.txt"
    MAX_LPF = 4096 # maximum length progess file



    yt_default_list_dir = "com/datas/ffmpeg/tv"

    yt_default_av_codecs = [
    "-c",
    "copy",
    "-movflags",
    "+faststart"
    ]

    yt_default_av_codecs = [
    "-c:v","libx264",
    "-c:a","aac"
    ]

    yt_start = [
    "ffmpeg",
    "-y",
    "-stream_loop",
    "-1",
    "-re"
    ]

    yt_input_concat = [
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "com/datas/ffmpeg/concat_list.txt"
    ]

    yt_screen_input = [
    "-f",
    "x11grab",
    "-video_size",
    "420x360",
    "-framerate",
    "10"
    ]

    yt_screen_input2 = [
    "-f",
    "pulse",
    "-ac",
    "2",
    "-i",
    "hw:0.1"
    ]

    yt_v4l2_input = [
    "-f",
    "v4l2",
    "-video_size",
    "856x480"
    ]

    yt_input_start = [
    "-i",
    "com/datas/ffmpeg/carta_ajuste.mp4.mkv"
    ]

    yt_input_carta = [
    "-i",
    "com/datas/ffmpeg/carta_ajuste2.mp4.mkv"
    ]

    yt_input_intro = [
  "-i",
  "com/datas/ffmpeg/intro.mp4"
    ]

    logo =[
    "-loop","1",
    "-i","com/datas/ffmpeg/logo.png",
    "-filter_complex", "[0:v]scale=-2:ih*1.8[v];[v]overlay=W-w-15:20:enable='between(t,0,inf)'",
    ]

    fscroll = [
    "-filter_complex",
    "[0] split [txt][orig];[txt] drawtext=textfile=com/datas/ffmpeg/fscroll.txt:reload=1: fontfile=lib/font/arialbd.ttf: fontcolor=#dddd11: fontsize=14: y=8: x=w-mod(max(t-1\,0)*(w+tw)/33\,(w+tw)): [txt];[txt] drawbox=x=5:y=5:w=iw:h=20:c=black@0.4:t=15 [txt];[txt] drawtext=fontfile=lib/font/arialbd.ttf: text='xBold': fontsize=8: fontcolor=#1e1eac: bordercolor=#d2bd19@0.5:borderw=1: boxborderw=2: x=w-text_w -2: y=5: [txt];[orig][txt] overlay=main_w-overlay_w-10:5"
    ]

    
    yt_codecs_start =  yt_default_preset + yt_default_screen + yt_default_abr + yt_default_vbr +  yt_default_buffer_size

    yt_codecs_rates = [
    "-pix_fmt",
    "yuv420p",
    "-g",
    "3",
    "-r",
    "15",
    "-maxrate",
    "750k",
    "-minrate",
    "128k"
    ]

    yt_codecs_start = logo + yt_codecs_start

    yt_codecs = yt_codecs_start + yt_default_av_codecs + yt_codecs_rates

    yt_output = [
    "-f",
    "flv",
    yt_default_output_url,
    "-progress",
    yt_default_progress_file,
    "-y"
    ]



    try:
        if args[0] == "youtube" or args[0] == "yt" :
            if len(args) == 1:
                args.append("intro")

            if args[1] == "intro":
                yt_args = yt_start + yt_input_intro + yt_codecs + yt_output
            elif args[1] == "concat":
                yt_args = yt_start + yt_input_concat + yt_codecs + yt_output
            elif args[1] == "start":
                yt_args = yt_start + yt_input_start + yt_codecs + yt_output
            elif args[1] == "carta":
                yt_args = yt_start + yt_input_carta + yt_codecs + yt_output
            elif args[1] == "input" or args[1] == "-i" :
                if args[2] == "v4l2" and len(args)>3:
                    yt_args = yt_start + yt_v4l2_input +["-i",args[3]] + yt_codecs + yt_output
                elif args[2] == "screen" and len(args)>3:
                    yt_args = yt_start + yt_screen_input +["-i",args[3]] + yt_screen_input2 + yt_codecs + yt_output
                else:
                    if len(args) > 2:
                        yt_args = yt_start + ["-i",args[2]] + yt_codecs + yt_output
            elif args[1] == "kill":
                if estado_proceso == True:
                    detener_proceso()
                    return
                else:
                    print("No hay proceso activo")
                    return
            else:
                print("Opción no disponible")
                return

            yt_last_args = yt_args


#            print(yt_args)
#DEL            yt_args = " ".join(yt_args)

            if  estado_proceso == False:
                print(yt_args)
                #return
                print("starting process")
                try:
                    funcion_proceso(yt_args)
                except Exception as e:
                	print("Error:",e)
                	print(yt_args)
                	return
            elif len(args) > 2 and "-c" in args:
                detener_proceso()
#                time.sleep(0.5)
                funcion_proceso(yt_args)
                estado_proceso == True
                print("Intercambio stream")
        elif args[0] == "status":
            print("status",estado_proceso)
            if yt_last_args:
                print("---Last Arguments--------------------------")
                print(yt_last_args)
                print("-------------------------------------------")
                print("---Join Arguments--------------------------")
                print(" ".join(yt_last_args))
                print("-------------------------------------------")
            if estado_proceso == True:
                print("---Estado Proceso: True--------------------")
                print("PID:",pid_proceso)
                print("-------------------------------------------")
        elif args[0] == "import":
            del args[:1]
            args.insert(0,"yt-dlp")
            print(args)
            subprocess.call(args,cwd="com/datas/ffmpeg")
        elif args[0] == "mklist":
            print("Mklist")
# Uso de la clase ConcatenadorFFmpeg
            extension = '.ts'
            archivo_concat = 'concat_list.txt'
            directorio_destino = 'com/datas/ffmpeg'
            directorio_origen = yt_default_list_dir
            concatenador = ConcatenadorFFmpeg(extension, archivo_concat, directorio_origen, directorio_destino)
            concatenador.concatenar_archivos()
        else:
            print("Comando no reconocido",args)

    except Exception as e:
        print("Se ha producido un error:",e)


def defaults():
    prueba = "in function"
    return prueba






#    "-vf",
#    "scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih),pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2",






print('Creado módulo-comando ffmpeg y fecha y hora: 2024-02-06 07:26:29.243208')



#FUNCIONES Y CLASES


class ConcatenadorFFmpeg:
    def __init__(self, extension, archivo_concat, directorio_origen, directorio_destino):
        self.extension = extension
        self.archivo_concat = archivo_concat
        self.directorio_origen = directorio_origen
        self.directorio_destino = directorio_destino

    def encontrar_archivos(self):
        archivos_mp4 = []
        for archivo in os.listdir(self.directorio_origen):
            if archivo.endswith(self.extension):
                archivos_mp4.append(archivo)
        return archivos_mp4

    def escribir_archivo_concat(self, archivos):
        random.shuffle(archivos)
        with open(os.path.join(self.directorio_destino, self.archivo_concat), 'w') as f:
            for archivo_mp4 in archivos:
                path_completo = os.path.dirname(os.path.abspath(archivo_mp4))
                f.write(f"file '{path_completo}/{self.directorio_origen}/{archivo_mp4}'\n")

    def concatenar_archivos(self):
        archivos = self.encontrar_archivos()
        if archivos:
            self.escribir_archivo_concat(archivos)
            print("Se ha creado el archivo de concatenación:", self.archivo_concat)
        else:
            print("No se encontraron archivos con la extensión especificada.")




def progress_trunk():
    tamano_actual = os.path.getsize(yt_default_progress_file)
    if tamano_actual > MAX_LPF:
        with open(yt_default_progress_file, 'r+') as archivo:
            archivo.truncate(MAX_LPF)
        print(tamano_actual)






