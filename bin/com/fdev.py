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
import requests
import re
import lib.core as core


# Determinar la ruta completa del script en ejecución
ruta_script = os.path.abspath(__file__)

# Determinar el directorio del script en ejecución
directorio_script = os.path.dirname(ruta_script)


# Determinar la ruta del directorio que deseas agregar a PYTHONPATH
directorio_a_agregar = os.path.join(directorio_script, 'play3')
print(directorio_script)

# Verificar si el directorio existe
if os.path.isdir(directorio_a_agregar):
    # Añadir el directorio al sys.path
    if not directorio_a_agregar in sys.path:
        sys.path.append(directorio_a_agregar)
        print(f"Directorio '{directorio_a_agregar}' agregado a PYTHONPATH.")
    else:
        print("Ya existe path en sys:",directorio_a_agregar)
 #       sys.path = [path for path in sys.path if path != directorio_a_agregar]
else:
    print(f"El directorio '{directorio_a_agregar}' no existe.")

# Imprimir sys.path para verificar
print("sys.path:", sys.path)

# Ahora puedes importar módulos desde el directorio 'play3'
try:
    core.dynmodule("play4","play3")
    play3 = core.play3
#    import play4 as play3 # Suponiendo que arch.py está en el directorio 'play3'
    print("Play3.4 hls Imported")
    #play3.detect_memory_leak()  # Llamar a alguna función en arch.py
except ImportError as e:
    print("No se pudo importar el módulo:", e)




cookies = ""
last_url = False
prueba = False
estado_proceso = False
pid_queue = multiprocessing.Queue()  # Cola compartida para almacenar el PID del proceso hijo
pid_proceso = None
yt_last_args = False


lineInput = None
def_output = "rtmp://rtmp.rumble.com/live/r-3enppr-kk9w-l1xl-1abb59"
def_output = "rtmp://a.rtmp.youtube.com/live2/svvb-yk73-asfv-0krs-5v57"
def_fout = "flv"
def_progress_file = "com/datas/ffmpeg/progress_process.txt"
def_seek_start = None #"00:38:17"
def_audio_filter = "aresample=async=1,loudnorm=I=-16:TP=-1.5:LRA=11"
def_preset = "ultrafast"
def_screen = "1280x720"
def_fps = "24"
def_intro_file = "com/datas/ffmpeg/intro.mp4"
def_profile = "youtube:2"
def_logo_tv = "logo.png"
def_fdir = yt_default_list_dir = "com/datas/ffmpeg"
def_crf = "23"
def_re = True
def_ar = "44100"
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
        "vbr":"0",
        "abr":"128k",
        "ar":def_ar,
        "bufsize":"6000k",
        "stream_loop":None,
        "input":lineInput,
        "maxrate":"3000k",
        "minrate":None,
        "fout":"flv",
        "output":def_output,
        "progress":def_progress_file,
        "ss":def_seek_start,
        "fps":"30",
        "crf":def_crf,
        "screen":"1280x720",
        "audio_filter":def_audio_filter,
        "logo": "logos/mtosierratv-p.png"
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


        "makets": {
        "re":None,
        "profileType":"mp4 to ts",
        "preset": def_preset,
        "vbr":None,
        "abr":None,
        "bufsize":None,
        "stream_loop":None,
        "input":lineInput,
        "maxrate":None,
        "minrate":None,
        "output":"com/datas/ffmpeg/defts.ts",
        "progress":"com/datas/ffmpeg/makets_progress.ts",
        "ss":def_seek_start,
        "screen":def_screen,
        "fout":"mpegts",
        "audio_filter":def_audio_filter
    },

    
    "hls": {

    'input':play3.hls_default_input,
   
    'com':[    
    'ffmpeg',
    '-y',
    '-re',
    '-loglevel', 'warning',
    '-f', 'lavfi','color=c=black:s=854x480',
    '-i',play3.hls_default_input,
    '-stream_loop', '-1', 
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
    '-hls_segment_filename', os.path.join(play3.hls_path, '%Y%m%d%H%M%S.ts'),
    os.path.join(play3.hls_path, 'live.m3u8'), '-progress', play3.hls_progress_file,
    '-fflags', '+genpts+igndts+discardcorrupt', '-flags', 'low_delay', '-max_delay', '0',
    '-reconnect', '1', '-reconnect_streamed', '1', '-reconnect_delay_max', '2', '-metadata', play3.ffcom_metadata]

}


}


play = []


input_protocols = ["http://","https://",'rtmp://'] #protocolos válidos input server
iprot = tuple(input_protocols)


intn = 0
lib_url = False

user_agent = []


def main(args):

    yt_args = False
    global estado_proceso
    global hilo_proceso, pid_proceso
    global yt_last_args
    global def_profile
    global last_url
    global play
    global intn,lib_url,iprot
    #global yt_start, yt_input_concat, yt_codecs, yt_output
    #global yt_input_start, yt_screen_input, yt_screen_input2, yt_v4l2_screen
    #global yt_default_progress_file, MAX_LPF
    global cookies, user_agent

    global lineInput, def_re, def_intro_file, def_output,def_progress_file,def_seek_start,def_audio_filter,def_preset,def_screen,def_fps,def_crf,def_ar
    global profiles
    global yt_default_list_dir,def_fdir


    profile_name = def_profile

    try:
        yt_default_list_dir = os.path.abspath(yt_default_list_dir)
    except Exception as e:
        print("Error (Path) : ",e)

    if args[0] == "probe":
        if len(args) > 1:
            subprocess.call(["ffprobe",args[1]])
            print("\nEnd Probe\n")
        else:
            print("Probe + Input")
        return

    if args[0] == "view":
        print("\n---- view ---------------------------\n")
        if len(args)>1:
            if args[1] == "proc":
                try:
                    multiprocess("Xproc",["date"])
                except Exception as e:
                    print("ERROR:",e)
                #play3.detener_proceso("mi_stream")
                try:
                    play3.listar_procesos()
                except Exception as e:
                    print("OPCION PARA PLAY5:".e)
            if args[1] == "profiles":
                print(profiles)
                return
            elif args[1] == "profile":
                if len(args) > 2:
                    if args[2] in profiles:
                        print("view profile:"+args[2]+"\n",profiles[args[2]])
                    else:
                        print("Profile: "+args[2]+" :Not exists")
                else:
                    print("Profile Active:",def_profile,"\n")
                    print("",profiles[def_profile],"\n")
            elif args[1] == "progress": 
#value = profiles.get(args[2], {}).get(args[3], None)
#                print(profiles[def_profile]["progress"])
                try:
                    print("\n---------- Progress TV ---")
                    subprocess.call(["tail",profiles[def_profile]["progress"],"-n","13"])
                    print("\n------ Progress HLS ---")
                    subprocess.call(["tail",play3.hls_progress_file,"-n","13"]) 
                except Exception as e:
                     print("Error:",e)
            elif args[1] == "lib":
                mostrar_datos_del_archivo()
            elif args[1] == "play":
                if len(args)>2:
                    try:
                        if int(args[2]) > 0 and int(args[2]) <= len(play):
                            print("VIEW PLAY:",str(args[2]))
                            print("VALUE:",play[int(args[2]) - 1])
                        else:
                            print("Número fuera de rango:",args[2])
                    except Exception as e:
                        if isinstance(args[2], int) == False:
                            print(" -> view play Requiere un número como parámetro")
                        else:
                            print("ERROR:",e)
        print("\n----------End View\n")
        return
    elif args[0] == "ls":
        if len(args)>1:
            try:
                intn = int(args[1])
                args[1] = play[int(intn) - 1]
            except Exception as e:
                intn = 0

            if os.path.isdir(yt_default_list_dir+"/"+args[1]):
                yt_default_list_dir = yt_default_list_dir+"/"+args[1]
            elif os.path.isdir(args[1]):
                yt_default_list_dir = args[1]
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
        print(" End ls:",os.path.abspath(yt_default_list_dir))
        return
    elif args[0] == "play":
        if len(args)>1:
            if args[1] == "tv":
                if len(args)>2:
                    if args[2] == "lasturl":
                        main(["yt","lasturl"])
                        return   
                    try:
                        intn = int(args[2])
                        if  intn > 0:
                            print(" PLay:"+str(intn))
                            if len(args)>3:
                                if args[3] == "probe":
                                    subprocess.call(["ffprobe","-i",yt_default_list_dir +"/"+ play[int(intn) - 1]])
                                    print("--End Probe-----------------")
                                    return
                            if play[int(intn) - 1].startswith(iprot):
                                main([ play[int(intn) - 1]]) 
                                main(["yt","lasturl"])
                            else:
                                parse_input(yt_default_list_dir + "/" + play[int(intn) - 1])
                                main(["yt","-i",yt_default_list_dir + "/" + play[int(intn) - 1],"-c"])
                    except Exception as e:
                        print(" ERROR:",e)
#### PLAY HLS
            elif args[1] == "hls":
                print("play3 hls started")
                hlscom = profiles["hls"]
#                play3.gestor.hello("Albert")
                if len(args)>2:
                    try:
                        if args[2] == "kill":
                            print("KILLING LAST PROCESS")
                            play3.kill_last_process()
                            return
                        intn = int(args[2])
                        if  intn > 0 and len(args) == 3:
                            if play[int(intn)-1].startswith(iprot):
                                print(" Hls PLay URL:"+str(intn))
                                lib_url = ""
                                main(["geturl",play[int(intn) - 1]])
                                if lib_url != "":
#                                    play3.start_ffmpeg(lib_url)
                                    print("Play LIB import")
                                    check_i = check_url_type(lib_url)
#                                    print("chk",check_i)
                                    if check_i == "Directory":
                                        print("INVALID URL:",lib_url)
                                        return
                                    elif check_i == "Timeout":
                                        print("TIMEOUT INSPECT FOR:",lib_url)                                       
                                    else:
                                        print("--->",profiles["hls"])
                                        play3.start_ffmpeg(lib_url,hlscom)
                                        print("Play Lib Direct")

                            else:
                                print("\n Hls PLay FILE:"+str(intn)+"\n")
                                play3.start_ffmpeg(yt_default_list_dir +"/"+ play[int(intn) - 1],hlscom)
                            print("\n → " ,play[int(intn) - 1] +"\n ")  
                            return
                        elif len(args)>3:
                            if args[3] == "probe":
                                if play[int(intn)-1].startswith(iprot):
                                    last_url = ""
                                    main([play[int(intn)-1]])
                                    if last_url != "":
                                        print("End probe HLS URL PARSED")
                                    else:
                                        print("ERROR INPUT FOR PROBE")
                                        print("Intento CON URL ORIGINAL",play[int(intn)-1])
                                        subprocess.call(["ffprobe","-i", play[int(intn) - 1]])
                                        print("End probe HLS URL ORIGINAL")
                                else:
                                    subprocess.call(["ffprobe","-i",yt_default_list_dir +"/"+ play[int(intn) - 1]])
                                print("--End Probe-----------------")
                                return
                            if play3.last_process != None:
                                print("DETECTED PROCESS:",play3.last_process.pid)
                            else:
                                print("NEW PROCESS WHITE")
                            return
                    except Exception as e:
                        if args[2] == "lasturl":
                            print("\nLASTURL\n")
                            if last_url != "" and last_url != False:
                                print("Playing Last_url:",last_url)
                                play3.start_ffmpeg(last_url,hlscom)
                            else:
                                print("NO EXISTE URL EN VARIABLE last_url")
                        return
                        print(" ERROR:",e)
                        return
            elif args[1] == "mpv":
                print("MPV COM")
                try:
                    intn = int(args[2])
                    if  intn > 0:
                        print(" MPV PLay:"+str(intn))
                        subprocess.Popen(["scripts/plaympv.sh",os.path.abspath("" + yt_default_list_dir +"/"+ play[int(intn) - 1])],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,shell=False)
                except Exception as e:
                    if args[2].startswith(iprot):
                        main([args[2]])
                        if last_url != "" and last_url != False and last_url != None:
                            subp = subprocess.Popen(["scripts/plaympv.sh",last_url],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,shell=False)
                            print("HTTP DIRECT:",last_url)
                        return
                    elif args[2] == "lasturl":
                        if last_url != "" and last_url != False and last_url != None:
                            subp = subprocess.Popen(["/home/osiris/plaympv.sh",last_url],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,shell=False)
                            print("LAST URL:",last_url)                                                
                    else:
                        print("MPV Exception:",e)
        print(" End Play")
        return
    elif args[0] == "set":
        if len(args) >1:
            try:
#cambio de valor en perfil
                if args[1] == "profile":
                #seleccion de perfil comproblar si existe en variable objeto profiles
                    if len(args)>2:
                        if args[2] in profiles:
#                            print("in profiles",args[2])
                            if len(args)>3:
                                if args[3] in profiles[args[2]]:
#                                    print("Key:"+args[3]+" in profile:"+args[2])
                                    if len(args)>4:
                                        value = profiles.get(args[2], {}).get(args[3], None)
                                        print("Value change to:",value)
                                        profiles[args[2]][args[3]] = args[4]
                                        print("Profile:",args[2],profiles[args[2]])
                                else:
                                    print("NOT Key:"+args[3]+" in profile:"+args[2])
                            else:
                                def_profile = args[2]
                                print("SET PROFILE:",def_profile)
                        else:
                            print("No existe en profiles:",args[2])
                elif args[1] == "lib":
                    guardar_datos_en_archivo()
            except Exception as e:
                print("Error in set:",e)
        print("Exit Set:",args)
        return



#output
    yt_default_re = profiles[profile_name].get("re") if "re" in profiles[profile_name] else def_re
    if yt_default_re == True :
        yt_default_re = ["-re"]
    else:
        yt_default_re = []


#input
    yt_default_input = profiles[profile_name].get("input") if "input" in profiles[profile_name] else def_intro_file
    if yt_default_input != None and yt_default_input != "None":
        yt_default_input = ["-i",yt_default_input]
    else:
        yt_default_input = []


#preset
    yt_default_preset = profiles[profile_name].get("preset") if "preset" in profiles[profile_name] else "ultrafast"
    if yt_default_preset != None and yt_default_preset !="None":
        yt_default_preset = ["-preset",yt_default_preset]
    else:
        yt_default_preset = []


#screen
    yt_default_screen = profiles[profile_name].get("screen") if "screen" in profiles[profile_name] else "856x480"
    if yt_default_screen != None and yt_default_screen != "None":
        yt_default_screen = ["-s",yt_default_screen]
    else:
        yt_default_screen = []


#bufersize
    yt_default_buffer_size = profiles[profile_name].get("bufsize") if "bufsize" in profiles[profile_name] else "1500k"
    if yt_default_buffer_size != None and yt_default_buffer_size != "None":
        yt_default_buffer_size = ["-bufsize",yt_default_buffer_size]
    else:
        yt_default_buffer_size = []


#VideoBitRate (vbr)
    yt_default_vbr = profiles[profile_name].get("vbr") if "vbr" in profiles[profile_name] else "1500k"
    if yt_default_vbr != None and yt_default_vbr != "None":
        yt_default_vbr = ["-b:v",yt_default_vbr]
    else:
        yt_default_vbr = []


#AudioBitRate (abr)
    yt_default_abr = profiles[profile_name].get("abr") if "abr" in profiles[profile_name] else "128k"
    if yt_default_abr != None and yt_default_abr != "None":
        yt_default_abr = ["-b:a",yt_default_abr]
    else:
        yt_default_abr = []

#Audio Rate (crf)
    yt_default_ar = profiles[profile_name].get("ar") if "ar" in profiles[profile_name] else def_ar
    if yt_default_ar != None and yt_default_ar != "None":
        yt_default_ar = ["-ar",yt_default_ar]
    else:
        yt_default_crf = []

#crf factor (crf)
    yt_default_crf = profiles[profile_name].get("crf") if "crf" in profiles[profile_name] else "22"
    if yt_default_crf != None and yt_default_crf != "None":
        yt_default_crf = ["-crf",yt_default_crf]
    else:
        yt_default_crf = []


#minrate
    yt_default_minrate = profiles[profile_name].get("minrate") if "minrate" in profiles[profile_name] else "256k"
    if yt_default_minrate != None  and yt_default_minrate != "None":
        yt_default_minrate = ["-minrate",yt_default_minrate]
    else:
        yt_default_minrate = []


#maxrate
    yt_default_maxrate = profiles[profile_name].get("maxrate") if "maxrate" in profiles[profile_name] else "750k"
    if yt_default_maxrate != None and yt_default_maxrate != "None":
        yt_default_maxrate = ["-maxrate",yt_default_maxrate]
    else:
        yt_default_maxrate = []



#fout -- format output
    yt_default_fout = profiles[profile_name].get("fout") if "fout" in profiles[profile_name] else def_fout
    if yt_default_fout != None and yt_default_fout != "None":
        yt_default_fout = ["-f",yt_default_fout]
    else:
        yt_default_fout = []




#output
    yt_default_output_url = profiles[profile_name].get("output") if "output" in profiles[profile_name] else def_output
    if yt_default_output_url != None and yt_default_output_url != "None" :
        yt_default_output_url = [yt_default_output_url]
    else:
        yt_default_output_url = ""


#progress
    yt_default_progress_file = profiles[profile_name].get("progress") if "progress" in profiles[profile_name] else def_progress_file
    if yt_default_progress_file != None and yt_default_progress_file != "None" :
        yt_default_progress_file = ["-progress",yt_default_progress_file]
    else:
        yt_default_progress_file = []


#seek start
    yt_default_seek_start = profiles[profile_name].get("ss") if "ss" in profiles[profile_name] else "00:00:00.000"
    if yt_default_seek_start != None and yt_default_seek_start != "None":
        yt_default_seek_start = ["-ss",yt_default_seek_start]
    else:
        yt_default_seek_start = []


#stram_loop
    yt_default_stream_loop = profiles[profile_name].get("stream_loop") if "stream_loop" in profiles[profile_name] else "-1"
    if yt_default_stream_loop != None and yt_default_stream_loop != "None":
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

# logo default (image)

    yt_logo_tv = profiles[profile_name].get("logo") if "logo" in profiles[profile_name] else def_logo_tv
    if yt_logo_tv != None:
        if yt_logo_tv == "":
            yt_logo_tv = def_logo_tv
    else:
        yt_logo_tv = def_logo_tv




    sudo_usr = ["sudo","-u","osiris"]

    sudo_usr = []

#    yt_default_output_url = "rtmp://a.rtmp.youtube.com/live2/svvb-yk73-asfv-0krs-5v57"
    MAX_LPF = 4096 # maximum length progess file

    yt_default_av_codecs = [
    "-c",
    "copy"
    ]

    yt_default_av_codecs = [
    "-c:a","aac" ] + yt_default_ar  + ["-c:v","h264",   
	"-bsf:v","h264_mp4toannexb",
	"-bsf:a","aac_adtstoasc",
    "-movflags",
    "+faststart"
 ]

    yt_start = ["ffmpeg"] + user_agent + ["-y"] + yt_default_stream_loop +  yt_default_re  + yt_default_seek_start

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
    logo_input = ["-i","com/datas/ffmpeg/"+yt_logo_tv]
    
    logo = logo_loop + logo_input + [
    "-filter_complex", "[0:v]scale=-2:ih*1.8[v];[v]overlay=15:20:enable='between(t,0,inf)'",
    ]

    fscroll = [
  '-vf',"drawtext=fontfile=lib/font/arialbd.ttf:textfile=com/datas/ffmpeg/fscroll.txt:y=5:x=10:fontsize=42:fontcolor=white:reload=1:enable='lt(mod(t\,15)\,4)'",
     ]

    
    yt_codecs_start =  ["-loglevel","warning"] +  yt_default_preset + yt_default_screen + yt_default_abr + yt_default_vbr +  yt_default_buffer_size

    yt_codecs_rates = yt_default_audio_filter + [
    "-pix_fmt",
    "yuv420p",
    "-g",
    "15"
    ] + yt_default_fps + yt_default_maxrate + yt_default_minrate

    yt_codecs_start =  logo +  yt_codecs_start
    yt_metadata = ["-metadata","'text=osiristvscreen'"]
    yt_codecs = yt_codecs_start + yt_default_av_codecs + yt_default_crf + yt_codecs_rates + yt_metadata

    yt_output = yt_default_fout + yt_default_output_url + yt_default_progress_file 

    try:
        if args[0].startswith("http://") or args[0].startswith("https://"):
            main(["geturl",args[0]])
            return


        if args[0] == "youtube" or args[0] == "yt" :
            
            if len(args) == 1:
                if profiles[def_profile]["input"] != None and profiles[def_profile]["input"] != "None":
                    args.append("-i")
                    args.append(profiles[def_profile]["input"])
                else:
                    args.append("intro")
            if args[1] == "lasturl":
                if last_url:
                    print("MAIN:",last_url)
                    parse_input(last_url)
                    main(["yt","-i",last_url,"-c","-M","Lasturl mode change stream"])
                    return
                else:
                    print("No Existe last_url:".last_url,lib_url)
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
            argse = ["yt-dlp", "-f", "[height<=720]", "--get-url", args[1]]
            try:
                p = subprocess.Popen(argse, cwd="com/datas/ffmpeg", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                output, _ = p.communicate()
                output = output.decode('utf-8').strip()
#                print(":::::::::::::::::::::",output)
                if not output.startswith("http://") and not output.startswith("https://"):
#                    print("cccccccccccc")
#                    return
            # Retry without the -f option if the first attempt fails
                    argse = ["yt-dlp", "--get-url", args[1]]
                    p = subprocess.Popen(argse, cwd="com/datas/ffmpeg", stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    output, _ = p.communicate()
                    output = output.decode('utf-8').strip()
                    output = parse_lasturl(output)
                    print("===================>",output)
                if output.startswith("http://") or output.startswith("https://"):
                    try:
                        subprocess.call(["ffprobe", "-i", output])
                        pi = True
                        last_url = output
                        lib_url = output
                    except Exception as e:
                        print("ERROR:", e)
                        pi = False
                else:
                    pi = False
                    lib_url = args[1]

                if pi == True:
                    print("Establecido lasturl a:", last_url)
                    with open("com/datas/lasturl.txt","w") as luf:
                        luf.write(last_url)
                else:
                    print("EXTRACT ERROR")
        
                if output != "":
                    print("URL:", output)
            except Exception as e:
                print("ERROR-:", e)
                return 
            return

        elif args[0] == "import":
            del args[:1]
            args.insert(0,"yt-dlp")
            print(args)
            subprocess.call(["sudo"]+args,cwd="com/datas/ffmpeg")
        elif args[0] == "mklist":
            print("Mklist")
            if len(args) > 1:
                directorio_origen = args[1]
            else:
                directorio_origen = 'com/datas/ffmpeg/playlist'
            print("Concat-dir:",args[1])
            directorio_destino = "com/datas/ffmpeg"
# Uso de la clase ConcatenadorFFmpeg
            extension = '.ts'
            archivo_concat = 'concat_list.txt'
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
    global user_agent
    if parametro.startswith("http://") or parametro.startswith("https://"):
        user_agent = ["-headers","user-agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'"]
        return "http"
    elif os.path.exists(parametro):
        user_agent = []
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
            print(f"Se ha creado el archivo de concatenación: {self.archivo_concat}")
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
        #subprocess.call(["sudo","-u","osiris","bash","com/otvkill"])
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




def guardar_datos_en_archivo():
    # Nombre del archivo
    nombre_archivo = "datos.txt"

    # Abrir el archivo en modo append y lectura ('a+')
    archivo = open(nombre_archivo, 'a+')

    try:
        # Pedir inputs
        canal = input("Ingrese el canal: ")
        url = input("Ingrese la URL: ")
        descripcion = input("Ingrese la descripción: ")
        xdata = input("Ingrese el xdata: ")

        # Formato de la línea a agregar
        linea = f'[canal:"{canal}",url:"{url}",descripcion:"{descripcion}",xdata:"{xdata}"]\n'

        # Escribir la línea en el archivo
        archivo.write(linea)

        print("Datos guardados exitosamente.")
    finally:
        # Cerrar el archivo
        archivo.close()


def mostrar_datos_del_archivo():
    global play
    play = []
    nombre_archivo = "datos.txt"
    s = 0
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            
        for linea in lineas:
            # Remover los caracteres de inicio y fin: '[', ']'
            linea = linea.strip()[1:-1]
            # Dividir la línea en partes separadas por comas
            partes = linea.split(',')
            # Crear un diccionario para almacenar los datos
            datos = {}
            for parte in partes:
                # Dividir cada parte en clave y valor, pero solo una vez
                clave, valor = parte.split(':', 1)
                # Remover las comillas del valor y espacios extra
                valor = valor.strip().strip('"')
                # Remover espacios y comillas de la clave
                clave = clave.strip().strip('"')
                # Agregar al diccionario
                datos[clave] = valor
            play.append(datos['url'])
            s=s+1

            # Mostrar los datos de manera legible
            print(f"{s} - Canal: {datos['canal']} \n  Descripción: {datos['descripcion']}  |||  xData: {datos['xdata']}")
            print(" ",datos['url'],"\n")
    except FileNotFoundError:
        print(f"El archivo {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")


def check_url_type(url, timeout=10):
    try:
        # Perform a HEAD request to get headers only with a timeout
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        
        # Extract the Content-Type header
        content_type = response.headers.get('Content-Type', '').lower()
        
        # Common Content-Types for directories
        directory_content_types = ['text/html', 'text/plain']
        
        # Check if the URL is likely a directory
        if any(content_type.startswith(ct) for ct in directory_content_types):
            print("INVALID CONTENT-TYPE:", content_type)
            return 'Directory'
        else:
            print("Content-type:",content_type)
            return 'File'   
    except requests.Timeout:
        print("Request timed out")
        return 'Timeout'
    
    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return 'Error'



def parse_lasturl(lasturl):
  """Divide lasturl en dos URLs si contiene un salto de línea, concatenándolas con '-i'."""
  if '\n' in lasturl:
    urls = lasturl.splitlines()
    return urls[1] + ' -i ' + urls[0] + ' '  # Concatenando con '-i'
  else:
    return lasturl  # Dejando lasturl como está si es una sola URL










