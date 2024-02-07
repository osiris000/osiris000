import time
import datetime
import subprocess
import os
import threading
import signal
import sys



estado_proceso = False
hilo_proceso = None
pid_proceso = None
def funcion_proceso(args):
    global estado_proceso
    global hilo_proceso
    global pid_proceso

    def run_auxiliar():
        global estado_proceso
        global pid_proceso
        try:
            proceso = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pid_proceso = proceso.pid
            print("Iniciado proceso PID:", pid_proceso)
            while True:
                linea = proceso.stdout.readline().decode("utf-8")
                if not linea:
                    break
                print(linea, end="")
        finally:
            estado_proceso = False
            print("Finalizado Popen")

    hilo_proceso = threading.Thread(target=run_auxiliar)
    hilo_proceso.start()
    estado_proceso = True







    hilo_proceso = threading.Thread(target=run_auxiliar)
    hilo_proceso.start()
    estado_proceso = True

def detener_proceso():
    global estado_proceso
    global pid_proceso
    if estado_proceso:
        os.kill(pid_proceso, signal.SIGTERM)
        estado_proceso = False
        print("Detenido proceso PID:",pid_proceso)


def main(args):
    global estado_proceso
    global hilo_proceso
    global yt_start, yt_input_concat, yt_codecs, yt_output
    global yt_input_start

    try:
        name_com = os.path.splitext(__file__)[0].split("/")[-1]
        file_com = __file__
        if args[0] == "edit" and len(args) > 1:
            if args[1] == "help":
                open = "help/"+name_com+".hlp"
            elif args[1] == "com":
                open = file_com
            else:
                print("use 'edit help' para editar el archivo de ayuda")
                print("use 'edit com' para editar el archivo del comando")
                return
            subprocess.call(["nano", "-w","-i",open])
        elif args[0] == "youtube":
            if len(args) == 1:
                args.append("intro")
                print(args)

            if args[1] == "intro":
                yt_args = yt_start + yt_input_intro + yt_codecs + yt_output
            elif args[1] == "concat":
                yt_args = yt_start + yt_input_concat + yt_codecs + yt_output
            elif args[1] == "kill":
                if estado_proceso == True:
                    detener_proceso()
                    return
                else:
                    print("No hay proceso activo")
            else:
                print("Opción no disponible")
                return

            if  estado_proceso == False:
                funcion_proceso(yt_args)
            elif len(args) > 2 and args[2] == "-c":
                detener_proceso()
                time.sleep(1)
                funcion_proceso(yt_args)
                estado_proceso == True
                print("Intercambio stream")
                return


            return
        elif args[0] == "status":
            print("status",estado_proceso)

    except Exception as e:
        print("Se ha producido un error:",e)


yt_start = [
    "ffmpeg",
    "-re",
    "-stream_loop",
    "-1"
]

yt_input_concat = [
    "-i",
    "concat:com/datas/ffmpeg/nacionalistas.ts|com/datas/ffmpeg/zorrax.ts|com/datas/ffmpeg/rhc.ts",
]

yt_input_intro = [

  "-i",
  "/home/osiris/Vídeos/vokoscreenNG-2024-02-06_22-06-43.mp4"

]



yt_codecs = [
    "-preset",
    "ultrafast",
    "-c:a",
    "aac",
    "-s",
    "640x480",
    "-c:v",
    "h264",
    "-pix_fmt",
    "yuv420p",
    "-r",
    "25",
    "-g",
    "4",
    "-b:a",
    "128k",
    "-b:v",
    "2500k",
    "-threads",
    "5"
]

yt_output = [
    "-f",
    "flv",
    "rtmp://a.rtmp.youtube.com/live2/g8pm-sau2-va7c-tyg5-1ppy"
]


print('Creado módulo-comando ffmpeg y fecha y hora: 2024-02-06 07:26:29.243208')
