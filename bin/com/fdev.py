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



last_url = False
prueba = False
estado_proceso = False
pid_queue = multiprocessing.Queue()  # Cola compartida para almacenar el PID del proceso hijo
pid_proceso = None
yt_last_args = False
profile_name = "youtube:2"

lineInput = None
def_output = "rtmp://a.rtmp.youtube.com/live2/g8pm-sau2-va7c-tyg5-1ppy"
#def_output = "rtmp://rtmp.rumble.com/live/r-3errs2-0lxe-yh55-d509ca"
def_progress_file = "com/datas/ffmpeg/progress_process.txt"
def_seek_start = None #"00:38:17"
def_audio_filter = None #"volume=2.2"
def_preset = "ultrafast"
def_screen = "1280x720"
def_fps = "24"
def_intro_file = "com/datas/ffmpeg/intro.mp4"

profiles = {
    "youtube:1": {
        "profileType":"Youtube Live Streaming 480p",
        "preset": def_preset,
        "vbr":"1000k",
        "abr":"128k",
        "bufsize":"1296k",
        "stream_loop":"-1",
        "input":lineInput,
        "maxrate":"648k",
        "output":def_output,
        "progress":def_progress_file,
        "ss":def_seek_start,
        "screen":"640x420"
    },
        "youtube:2": {
        "profileType":"Youtube Live Streaming 720p",
        "preset": def_preset,
        "vbr":"4000k",
        "abr":"128k",
        "bufsize":"10000k",
        "stream_loop":"-1",
        "input":lineInput,
        "maxrate":"4500k",
        "minrate":"3500k",
        "output":def_output,
        "progress":def_progress_file,
        "ss":def_seek_start,
        "fps":"24",
        "screen":"1280x720"
    },

        "rumble:860": {
        "profileType":"Rumble 860",
        "preset": def_preset,
        "vbr":"5000k",
        "abr":"128k",
        "bufsize":"15000k",
        "stream_loop":None,
        "input":lineInput,
        "maxrate":"6000k",
        "minrate":"860k",
        "output":def_output,
        "progress":def_progress_file,
        "ss":def_seek_start,
        "screen":def_screen,
        "audio_filter":def_audio_filter
    },

        "rumble:640": {
        "profileType":"Rumble 480",
        "preset": def_preset,
        "vbr":"3500k",
        "abr":"128k",
        "bufsize":"12000k",
        "stream_loop":None,
        "input":lineInput,
        "maxrate":"4500k",
        "minrate":"640k",
        "output":def_output,
        "progress":def_progress_file,
        "ss":def_seek_start,
        "screen":def_screen,
        "audio_filter":def_audio_filter
    },


        "rumble:480": {
        "profileType":"Rumble 480",
        "preset": def_preset,
        "vbr":"2500k",
        "abr":"128k",
        "bufsize":"10000k",
        "stream_loop":None,
        "input":lineInput,
        "maxrate":"3500k",
        "minrate":"480k",
        "output":def_output,
        "progress":def_progress_file,
        "ss":def_seek_start,
        "screen":def_screen,
        "audio_filter":def_audio_filter
    },

    "perfil2": {
        "preset": "slow"
    }
}


play = []


def_fdir = yt_default_list_dir = "com/datas/ffmpeg"

def main(args):

    yt_args = False
    global estado_proceso
    global hilo_proceso, pid_proceso
    global yt_last_args
    global def_profile
    global last_url
    global play
    #global yt_start, yt_input_concat, yt_codecs, yt_output
    #global yt_input_start, yt_screen_input, yt_screen_input2, yt_v4l2_screen
    #global yt_default_progress_file, MAX_LPF


    global lineInput, def_intro_file, def_output,def_progress_file,def_seek_start,def_audio_filter,def_preset,def_screen,def_fps
    global profiles
    global yt_default_list_dir,def_fdir

    if args[0] == "view":
        if len(args)>1:
            if args[1] == "profiles":
                print(profiles)
                return
        print("End View")
        return
    elif args[0] == "ls":
        if len(args)>1:
            if os.path.isdir(yt_default_list_dir+"/"+args[1]):
                yt_default_list_dir = yt_default_list_dir+"/"+args[1]
            elif args[1] == "*":
                yt_default_list_dir = def_fdir
            else:
                print(" IS NOT PATH")
                return
        print("---------------")
        file_list = list_files(yt_default_list_dir)
        play = []
        n = 0
        for file in file_list:
            n = n + 1
            print("   "+str(n)+" - "+file)
            play.append(file)
        print("---------------")
        print(" End ls")
        return
    elif args[0] == "play":
        if len(args)>1:
            if args[1] == "tv":
                if len(args)>2:
                    try:
                        intn = int(args[2])
                        if  intn > 0:
                            print(" PLay:"+str(intn))
                            print(" yt -i \"" + yt_default_list_dir +"/"+ play[int(intn) - 1] +"\" -c")
                            if len(args)>3:
                                if args[3] == "probe":
                                    subprocess.call(["ffprobe","-i",yt_default_list_dir +"/"+ play[int(intn) - 1]])
                                    print("--End Probe-----------------")
                                    return
                            main(["yt","-i",yt_default_list_dir + "/" + play[int(intn) - 1],"-c"])
                            return
                    except Exception as e:
                        print(" ERROR:",e)
                        return
        print(" End Play")
        return

#input
    yt_default_input = profiles[profile_name].get("input") if "input" in profiles[profile_name] else def_intro_file
    if yt_default_input != None:
        yt_default_input = ["-i",yt_default_input]
    else:
        yt_default_input = ""


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


#minrate
    yt_default_minrate = profiles[profile_name].get("minrate") if "minrate" in profiles[profile_name] else "256k"
    if yt_default_minrate != None:
        yt_default_minrate = ["-minrate",yt_default_minrate]
    else:
        yt_default_minrate = []


#maxrate
    yt_default_maxrate = profiles[profile_name].get("maxrate") if "maxrate" in profiles[profile_name] else "750k"
    if yt_default_maxrate != None:
        yt_default_maxrate = ["-maxrate",yt_default_maxrate]
    else:
        yt_default_maxrate = []


#output
    yt_default_output_url = profiles[profile_name].get("output") if "output" in profiles[profile_name] else def_output
    if yt_default_output_url != None:
        yt_default_output_url = [yt_default_output_url]
    else:
        yt_default_output_url = ""


#progress
    yt_default_progress_file = profiles[profile_name].get("progress") if "progress" in profiles[profile_name] else def_progress_file
    if yt_default_progress_file != None:
        yt_default_progress_file = ["-progress",yt_default_progress_file]
    else:
        yt_default_progress_file = ""


#seek start
    yt_default_seek_start = profiles[profile_name].get("ss") if "ss" in profiles[profile_name] else "00:00:00.000"
    if yt_default_seek_start != None:
        yt_default_seek_start = ["-ss",yt_default_seek_start]
    else:
        yt_default_seek_start = []


#stram_loop
    yt_default_stream_loop = profiles[profile_name].get("stream_loop") if "stream_loop" in profiles[profile_name] else "-1"
    if yt_default_stream_loop != None:
        yt_default_stream_loop = ["-stream_loop",yt_default_stream_loop]
    else:
        yt_default_stream_loop = []


#audio_filter
    yt_default_audio_filter = profiles[profile_name].get("audio_filter") if "audio_filter" in profiles[profile_name] else ""
    if yt_default_audio_filter != None:
        if yt_default_audio_filter == "":
            yt_default_audio_filter = []
        else:
            yt_default_audio_filter = ["-af",yt_default_audio_filter]
    else:
        yt_default_audio_filter = []



#fps (frames x segundo - output)

    yt_default_fps = profiles[profile_name].get("fps") if "fps" in profiles[profile_name] else def_fps
    if yt_default_fps != None:
        if yt_default_fps == "":
            yt_default_fps = []
        else:
            yt_default_fps = ["-r",yt_default_fps]
    else:
        yt_default_fps = []




    sudo_usr = ["sudo","-u","osiris"]

#    yt_default_output_url = "rtmp://a.rtmp.youtube.com/live2/svvb-yk73-asfv-0krs-5v57"
    MAX_LPF = 4096 # maximum length progess file

    yt_default_av_codecs = [
    "-c",
    "copy"
    ]

    yt_default_av_codecs = [
    "-c:v","h264",
    "-c:a","aac",
	"-bsf:v","h264_mp4toannexb",
	"-bsf:a","aac_adtstoasc",
    "-movflags",
    "+faststart"
    ]

    yt_start = [
    "ffmpeg",
    "-y"] + yt_default_stream_loop + ["-re"] + yt_default_seek_start 


    yt_start_intro = [
    "ffmpeg",
    "-y"] + ["-stream_loop","-1"] + ["-re"]  

    yt_input_concat = [
    "-f",
    "concat",
    "-safe",
    "0",
    "-i",
    "com/datas/ffmpeg/concat_list.txt"
    ]

    yt_default_region_screen = ":0.0+100,100"

    yt_screen_input = [
    "-f",
    "x11grab",
    "-video_size",
    "640x480",
    "-framerate",
    "10"
    ]

    yt_screen_input2 = [
    "-f",
    "alsa",
    "-ac",
    "2",
    "-i",
    "pulse"
    ]

    yt_v4l2_input = [
    "-f",
    "v4l2",
    "-video_size",
    "856x480"
    ]

    yt_input_start = [
    "-i",
    "com/datas/ffmpeg/start.mkv"
    ]

    yt_input_carta = [
    "-i",
    "com/datas/ffmpeg/carta.mkv"
    ]

    yt_input_intro = [
  "-i",
  def_intro_file
    ]


    logo_loop = ["-loop","1"]
    logo_loop = []
    logo_input = ["-i","com/datas/ffmpeg/logo.png"]
    
    logo = logo_loop + logo_input + [
    "-filter_complex", "[0:v]scale=-2:ih*1.8[v];[v]overlay=W-w-15:20:enable='between(t,0,inf)'",
    ]

    fscroll = [
  '-vf',"drawtext=fontfile=lib/font/arialbd.ttf:textfile=com/datas/ffmpeg/fscroll.txt:y=5:x=10:fontsize=42:fontcolor=white:reload=1:enable='lt(mod(t\,15)\,4)'",
     ]

    
    yt_codecs_start =   yt_default_preset + yt_default_screen + yt_default_abr + yt_default_vbr +  yt_default_buffer_size

    yt_codecs_rates = yt_default_audio_filter + [
    "-pix_fmt",
    "yuv420p",
    "-g",
    "2"
    ] + yt_default_fps + yt_default_maxrate + yt_default_minrate

    yt_codecs_start =  logo +  yt_codecs_start
    yt_metadata = ["-metadata","'text=osiristv-fdev'"]
    yt_codecs = yt_codecs_start + yt_default_av_codecs + yt_codecs_rates + yt_metadata

    yt_output = [
    "-f",
    "flv"] + yt_default_output_url + yt_default_progress_file 

    try:
        if args[0].startswith("http://") or args[0].startswith("https://"):
            main(["geturl",args[0]])
            return


        if args[0] == "youtube" or args[0] == "yt" :
            
            if len(args) == 1:
                args.append("intro")


            if args[1] == "lasturl":
                if last_url:
                    print("MAIN:",last_url)
                    main(["yt","-i",last_url,"-c","-M","Lasturl mode change stream"])
                    return
                else:
                    print("No Existe last_url")
                return
            elif args[1] == "intro":
                yt_args = yt_start_intro + yt_input_intro + yt_codecs + yt_output
            elif args[1] == "concat":
                yt_args = yt_start + yt_input_concat + yt_codecs + yt_output
            elif args[1] == "start":
                yt_args = yt_start + yt_input_start + yt_codecs + yt_output
            elif args[1] == "carta":
                yt_args = yt_start + yt_input_carta + yt_codecs + yt_output
            elif args[1] == "input" or args[1] == "-i" :
                if args[2] == "v4l2" and len(args)>3:
                    yt_args = yt_start + yt_v4l2_input +["-i",args[3]] + yt_codecs + yt_output
                elif args[2] == "screen" and len(args)>=3:	
                    if len(args) == 3:
                        print(",,,,,,,,,,")
                        args.append(yt_default_region_screen)
                    yt_args = sudo_usr + yt_start + yt_screen_input +["-i",args[3]] + yt_screen_input2 + yt_codecs + yt_output
                else:
                    if len(args) > 2:
                        try:
                    	    pInput = parse_input(args[2])
                        except Exception as e:
                    	    print("Error Parse Input:",e)
                    	    print("Args:",args[2])
                    	    return
                        if pInput:
                            subprocess.call(["ffprobe","-i",args[2]])
                        else:
                            print("Error Input:",args[2])
                            return
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
            print(" ".join(yt_args))

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
                estado_proceso == True
                kill_l = pid_proceso
                print("Intercambio stream")
                interchange2(yt_args,kill_l)
                return
#                detener_proceso()

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

        elif args[0] == "geturl" and len(args) > 1:
            argse = ["yt-dlp", "-f", "best[height<=720]/best", "--get-url", args[1]]
            try:
                p = subprocess.Popen(argse, cwd="com/datas/ffmpeg", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                output, _ = p.communicate()
                output = output.decode('utf-8').strip()
                if output.startswith("http://") or output.startswith("https://"):
                    try:
                        subprocess.call(["ffprobe","-i",output])
                        pi = True
                        last_url = output
                    except Exception as e:
                        print("ERROR:",e)
                        pi = False
                if pi == True:
                    print("Escriba 'yt lasturl' y pulse enter para cambiar stream a:",last_url)
                else:
                    print("ERROR PI")    
                print("URL:", output)
            except Exception as e:
                print("ERROR:", e)
            return

        elif args[0] == "import":
            del args[:1]
            args.insert(0,"yt-dlp")
            print(args)
            subprocess.call(args,cwd="com/datas/ffmpeg")
        elif args[0] == "mklist":
            print("Mklist")
# Uso de la clase ConcatenadorFFmpeg
            extension = '.mp4'
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





itc_time = 5


def interchange(yt_args,kill_l):
    global itc_time
    d = 0
    global pid_proceso
    funcion_proceso(yt_args)
    while d <= itc_time:
        print(".",d+1)
        d = d +1
        if d == itc_time:
            try:
                os.kill(kill_l, signal.SIGKILL)
#uso os kill en vez de subprocess                            subprocess.call(["kill",str(kill_l)],shell=True)
#                print("KILL:",kill_l)
                break
            except Exception as e:
                print("CH PID WARN",e)
                break
        time.sleep(1)
    print("New:",pid_proceso)
    return


def interchange2(yt_args,kill_l):
    global itc_time
    d = 0
    global pid_proceso
#    input("Pulse Enter para matar el proceso anterior:"+str(kill_l))
    try:
        os.kill(kill_l, signal.SIGKILL)
#uso os kill en vez de subprocess                            subprocess.call(["kill",str(kill_l)],shell=True)
        #print("KILL:",kill_l)
    except Exception as e:
        print("CH PID WARN",e)
 #   print("KILL:",kill_l)
    funcion_proceso(yt_args)
 #   print("New Proceso iniciado:",pid_proceso)
    return




#    "-vf",
#    "scale=iw*min(1920/iw\,1080/ih):ih*min(1920/iw\,1080/ih),pad=1920:1080:(1920-iw*min(1920/iw\,1080/ih))/2:(1080-ih*min(1920/iw\,1080/ih))/2",

def parse_input(parametro):
    if parametro.startswith("http://") or parametro.startswith("https://"):
        return "http"
    elif os.path.exists(parametro):
        return "file"
    else:
        return False




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



def list_files(directory):
    files = os.listdir(directory)
    files.sort()    
    numbered_files = []
    for index, file in enumerate(files, start=1):
        numbered_files.append(f"{file}")
    return numbered_files







def progress_trunk():
    tamano_actual = os.path.getsize(yt_default_progress_file)
    if tamano_actual > MAX_LPF:
        with open(yt_default_progress_file, 'r+') as archivo:
            archivo.truncate(MAX_LPF)
        print(tamano_actual)


def funcion_en_segundo_plano():
    # Tarea a ejecutar en segundo plano
    return

def thread():
    hilo = threading.Thread(target=funcion_en_segundo_plano)
    hilo.daemon = True
    hilo.start()



def funcion_proceso(args):
    global estado_proceso
    try:
        subprocess.call(["sudo","-u","osiris","bash","com/otvkill"])
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









print('Creado módulo-comando ffmpeg y fecha y hora: 2024-02-06 07:26:29.243208')

