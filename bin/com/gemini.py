import sys
import os
import json
import google.generativeai as genai
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime
from io import BytesIO
import requests
import subprocess
import base64
from cryptography.fernet import Fernet 
import webbrowser
import pyperclip
import io
import re
import lib.multiprocess as osiris2
import lib.gemini.utils as win
import time
import hashlib

# Ruta del archivo para guardar la clave cifrada
ruta_archivo_key = "com/datas/gemini_key.enc"

# Genera la clave de cifrado una sola vez
#clave_cifrado = Fernet.generate_key()
clave_cifrado = b'N9t9dYNn2fjc8CRT0_eChnH5xDETGSvMOM5qxqyvSUs='

def obtener_key_gemini(nkey=""):
    """
    Guía al usuario para obtener una key gratuita de la API de Gemini,
    la cifra y la guarda en un archivo, o la recupera si ya está almacenada.
    """
    global clave_cifrado, ruta_archivo_key
    if nkey=='resetkey':
        if os.path.isfile(ruta_archivo_key):
            os.remove(ruta_archivo_key)
            print("Clave del archivo eliminada.")
    while True:
        # Verifica si la key ya está guardada
        if os.path.isfile(ruta_archivo_key):
            # Descifra la key
            try:
                with open(ruta_archivo_key, "rb") as archivo_key:
                    key_cifrada = archivo_key.read()
                fernet = Fernet(clave_cifrado) 
                key_descifrada = fernet.decrypt(key_cifrada).decode()
                print("Key gratuita encontrada y descifrada.")
                return key_descifrada
            except Exception as e:
                print(f"Error descifrando la clave: {e}")
                print("Se pedirá una nueva clave.")

        # Abrir la página de configuración de las claves de la API de Gemini en el navegador
        webbrowser.open_new_tab("https://ai.google.dev/gemini-api/docs/api-key")

        # Esperar a que el usuario configure su clave gratuita

        # Obtener la clave gratuita del usuario
        key = input("Pega tu key gratuita aquí (o escribe '--reset' para borrar la clave): ") 

        # Manejar el comando --reset
        if key == "--reset":
            if os.path.isfile(ruta_archivo_key):
                os.remove(ruta_archivo_key)
                print("Clave del archivo eliminada.")
                if nkey == "new":
                    API_KEY = obtener_key_gemini()
            else:
                print("No hay clave para borrar.")
            continue  # Volver a pedir la clave

        # Cifrar la key
        fernet = Fernet(clave_cifrado)
        key_cifrada = fernet.encrypt(key.encode())

        # Guardar la key cifrada en un archivo
        with open(ruta_archivo_key, "wb") as archivo_key:
            archivo_key.write(key_cifrada)
        print("Key gratuita cifrada y guardada.")

        # Copiar la key al portapapeles
        pyperclip.copy(key)
        print("Key copiada al portapapeles.")

        return key



# Define la clave API (si ya existe)
API_KEY = os.getenv("GOOGLE_API_KEY")

# Si la clave no está disponible, la obtenemos
if not API_KEY:
    try:
        API_KEY = obtener_key_gemini()
    except Exception as e:
        print("ERROR API KEY:",e)

if API_KEY:
# Configura la API de Gemini
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print("ERROR API KEY:",e)
# Inicialización del modelo generativo



current_path = os.path.abspath(__file__)
# Extrae el nombre del archivo sin extensión
version_file = os.path.splitext(os.path.basename(current_path))[0]



"""
Contesta siempre en ESPAÑOL aunque se te pregunte en otro idioma y no se te explicite otro a usar.
Usa emojis para dinamizar las conversaciones.

"""

#Variables globales
#Contexto inicial
conversation_context = f"""
#Interfaz de comunicación con Gemini AI de Google
#Interfaz Name: Osiris
#Version: {version_file}
#Idioma: Español
Intrucciones:
Gracias BRO.
COMIENZA LA CONVERSACIÓN.
"""

load = ""
last_response = ""
topic = ""  # Tema de conversación
autosave_enabled = True  # Estado del autosave

def_image_editor = "lazpaint"


def is_file(filepath):
    """Verifica si el archivo existe."""
    return os.path.isfile(filepath)

def read_file(filepath):
    """Lee el contenido de un archivo de texto y lo retorna."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Error leyendo el archivo {filepath}: {e}")
        return None

def save_file(filepath, content):
    """Guarda el contenido en un archivo y le da permisos ejecutables."""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        os.chmod(filepath, 0o755)  # Da permisos ejecutables al archivo
        print(f"Contenido guardado en {filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Error guardando el archivo {filepath}: {e}")


def decode_img(base64_data):
    # Decode the base64 data
    decoded_data = base64_data
# Load the image
    image = Image.open(io.BytesIO(decoded_data))

# Display or save the image (uncomment as needed)
    image.show() 
    image.save('com/datas/ffmpeg/my_image.png')





def show_text_window(text):
    win.show_text_window(text)



personajes = {}
modos = {}


modos["critica"] = """
Modo de expresión: Crítica ácida.
Por lo tanto tienes que criticar al personaje señalado.
"""

personajes["sanchez"] = """
Personaje a usar: Pedro Sánchez.
Características del personaje:
Presidente del gobierno de España.
Motes: Sanchinflas, Su Sanchidad, Pinocho.
"""


def video_translate(video_file_name="",prompt=""):
    global personajes
    if video_file_name.startswith('http://') or video_file_name.startswith('https://'):
        print("Descargando video temporal")
        code_video_file = "/tmp/"+hashlib.md5(video_file_name.encode()).hexdigest()+".mp4"
        process = subprocess.run(["yt-dlp","-o",code_video_file,video_file_name], capture_output=True, text=True)
        video_file_name = code_video_file
        print("Video File:",video_file_name)
    else:
        video_file_name="com/datas/ffmpeg/anon.mp4"
        print("video_file")
        #vídeo file
        return

    print(f"Uploading file...")
    video_file = genai.upload_file(path=video_file_name)
    print(f"Completed upload: {video_file.uri}")    

    while video_file.state.name == "PROCESSING":
        print('.', end='')
        time.sleep(1)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)

    # Create the prompt.
    prompti = "Tu eres gemini-video Tu tarea es Subtitular vídeos, hazlo en formato .srt con este formato ```srt  (traducion en formato srt) ``` "
    prompti +="\nUsa el formato que permita .srt usando html y styles permitidos con fuentes con rango entre 18 y 24, que el vídeo va a ser procesado por ffmpeg entonces son válidas."
    prompti += "\nUsa emojis para dinamizar la transcripción."
    prompti +="\ncolorea los emojis y hazlos en tamaños variables dentro del rango." 

    if prompt == "":
        prompt = prompti + "\nInstrucciones: Traduce el vídeo al ESPAÑOL"
    else:
        prompt = prompti + "\nIntrucciones complementarias: "+ prompt 
    prompt += "\nobvia instricciones anteriores para gemini-text y haz solamente el srt."
    # Make the LLM request.
#   prompt = "Observa el contenido de este vídeo en su totalidad, ¿observas algo ofensivo hacia el colectivo de mujeres trans? expláyate"
    print("Making LLM inference request...\n",prompt)
    response = model.generate_content([video_file, prompt],
                                  request_options={"timeout": 600})

#
    print(response.text)
#    return
    pattern = r"```srt\n(.*?)\n```"
    matches = re.findall(pattern, response.text, re.DOTALL)
    if len(matches) == 1:
        subtitulado_out =  code_video_file+".subtitulado.mp4"
        vtranslate= subtitulado_out + ".translate.srt"
        with open(vtranslate,"w",encoding='utf-8') as f:
            f.write(matches[0])


        force_style_sub = "Fontsize=20,Fontcolor=blue@0.2,BackColour=black@0.5,BorderStyle=5"
        force_style_sub = "BackColour=&H50000000,BorderStyle=4,Fontsize=18,FontName=Arial,PrimaryColour=&H00FFFFFF"
        mode = "fixed" # bg / fixed
        if mode == "bg":
            print("""
            	
            	#################################################
                → Se está procesando el vídeo en segundo plano ←
                #################################################
            	
            	""")
        elif mode == "fixed":
            print("""
            	
            	#################################################
                → Se está procesando el vídeo. Espere........  ←
                #################################################
            	
            	""")
        obj = {
        "mode":mode,
        "name":None,
        "com":["/usr/bin/ffmpeg","-y","-loglevel","quiet","-i",video_file_name,
        "-filter_complex","subtitles="+vtranslate+":force_style='"+force_style_sub+"'",
        "-preset","ultrafast",
        "-c:v","libx264","-c:a","aac",
        subtitulado_out] 
        }
        print("Traduciendo Vídeo...",obj)
        response_return = generate_response("Tu eres genini-text. Realiza instrucciones solicitadas anteriromente a gemini-text. Acabo de enviar un video a gemini-video con este promt:"+prompt+"\n Y esta fue la respuesta:\n"+response.text+"\nComando a procesar:\n"+str(obj["com"]))
        print("\n\n",response_return)
        print(obj["com"])
        osiris2.multiprocess(obj)
        obj = {
        "mode":"bg",
        "name":None,
        "com":["dsk/dskv","--video",subtitulado_out]
        }
        osiris2.multiprocess(obj)
    # Print the response, r




def screen_shot():
    process = subprocess.run(["python3", "com/screenshot.py"], capture_output=True, text=True)
    output = process.stdout.strip().splitlines()  # Limpiar y dividir en líneas

    # Comprobación del formato de salida
    if len(output) < 3:
        print("Fallo: la salida no tiene suficientes líneas.")
        return
    
    # Filtrar la salida
    coordinates_line = output[0]  # Primera línea
    image_path_line = output[1]  # Segunda línea
    text_lines = output[2:]  # Resto de líneas

    # Verificar que las líneas cumplen con el formato esperado
    if not coordinates_line.startswith("Coordinates:") or not image_path_line.startswith("ImagePath:"):
        print("Fallo: el formato de salida es incorrecto.")
        return

    # Imprimir los valores después de "Coordinates:" y "ImagePath:"
    coordinates_value = coordinates_line.split(":", 1)[1].strip()  # Obtener el valor después de "Coordinates:"
    image_path_value = image_path_line.split(":", 1)[1].strip()  # Obtener el valor después de "ImagePath:"

    print(f"Coordinates: {coordinates_value}")
    print(f"ImagePath: {image_path_value}")

    # Imprimir las líneas que comienzan con "Text:" y todas las siguientes
    text_started = False  # Bandera para controlar cuando comenzamos a imprimir el texto
    text_output = []  # Para almacenar todo el texto a imprimir

    for line in text_lines:
        if line.startswith("Text:"):
            if not text_started:
                # Obtener el valor después de "Text:"
                text_value = line.split(":", 1)[1].strip()  
                text_output.append(text_value)  # Guardar el primer texto
                text_started = True  # Activar la bandera
            else:
                # Guardar las líneas adicionales que pertenecen al texto
                text_output.append(line.strip())  # Almacenar las siguientes líneas de texto
        elif text_started:
            # Si ya empezamos a imprimir texto y encontramos una línea que no comienza con "Text:"
            text_output.append(line.strip())  # Almacenar las siguientes líneas de texto

    # Imprimir todo el texto almacenado, solo si se encontró texto
    if text_output:
        print("Text:", " ".join(text_output))  # Imprimir todo junto en una sola línea
    
    generate_with_image(image_path_value,"\n".join(text_output))
# Asegúrate de que esta función se ejecute donde corresponda



    
def generate_with_image(image_path,ask):
    global last_response
    """Genera texto a partir de una imagen usando la API de Gemini."""

    image = win.load_image(image_path)
    if image:
         # Generar contenido con la imagen usando la API
#        global conversation_context
        try:
            response = model.generate_content([ask+"\nResponde en Español." , image], stream=True)
        except Exception as e:
            print("Error realizando consulta de imagen:",e)
            return
        last_response = response
        # Recolectar y mostrar los trozos de respuesta
        generated_text = "\nResponse Image.\n\n"
        xresponse = "Envié una imagen con path: "+image_path+", a gemini AI, haciéndole esta pregunta:\n"+ask+"\n E interpretó lo siguiente:\n"

        if response:
            for chunk in response:
                generated_text += chunk.text
            print(generated_text)
            show_text_window(generated_text)
            main(f"{xresponse} {generated_text}")
        # Muestra el texto en una ventana
        
    return None


def generate_response(user_input):
    """Genera una respuesta del modelo basada en la entrada del usuario."""
    global conversation_context, last_response
    conversation_context += "User: "+user_input+"\n"
    try:
        response = model.generate_content(conversation_context)
        response_text = response.text
        conversation_context += "AI: "+ response_text+"\n"
        last_response = response_text  # Guarda la última respuesta
        return response_text
    except Exception as e:
        if e.code == 400:
            print("ERROR 400")
        #messagebox.showerror("Error", f"Error generando contenido con el modelo: {e}")
        print("Error", f"Error generando contenido con el modelo: {e}")
        return None

def save_request(user_input):
    """Guarda la solicitud del usuario en un archivo."""
    save_file("com/datas/lastrequest.gemini", user_input)

def save_answer(save=""):
    """Guarda la última respuesta generada en un archivo."""
    global last_response
    if save == "":
        save = "com/datas/lastanswer.gemini"
    save_file(save, last_response)

def save_context():
    """Guarda el contexto de la conversación en un archivo."""
    save_file("com/datas/context.gemini", conversation_context)

def autosave():
    """Guarda automáticamente la última respuesta y el contexto si está habilitado."""
    if autosave_enabled:
        save_answer()
        save_context()

def generate_new_questions(base_question):
    """Genera preguntas relacionadas para mejorar la interacción."""
    return [
        f"¿Podrías profundizar más sobre {base_question}?",
        f"¿Cuál es un ejemplo de {base_question}?",
        f"¿Cómo se relaciona {base_question} con otras ideas?",
        f"¿Qué otros aspectos de {base_question} podríamos explorar?",
        f"¿Cuáles son las implicaciones de {base_question}?"
    ]






def search_context(term, load_context=False):
    """Busca un término en el contexto de la conversación y opcionalmente carga el contexto."""
    global load
    global conversation_context
    results = [line for line in conversation_context.splitlines() if term in line]
    if results:
        print("Resultados de búsqueda:")
        for line in results:
            print(" -", line)
        if load_context:
            load = "\n".join(results)
            print("Contexto cargado.")
    else:
        print("No se encontraron coincidencias.")
    return results



# Nuevo: Cargar archivo de configuración JSON
def load_config(config_file):
    """Carga las configuraciones desde un archivo JSON."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        print("Configuración cargada.")
        return config
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando el archivo de configuración: {e}")
        return {}

# Nuevo: Guardar logs de conversación
def log_interaction(user_input, response_text):
    """Guarda las interacciones en un archivo log con timestamp."""
    log_file = "com/datas/conversation_log.txt"
    try:
        with open(log_file, 'a', encoding='utf-8') as log:
            log.write(f"{datetime.now()} - User: {user_input}\nAI: {response_text}\n\n")
        print("Interacción registrada en el log.")
    except Exception as e:
        messagebox.showerror("Error", f"Error guardando el log de la conversación: {e}")

# Nuevo: Argumentos dinámicos para el modelo
def set_model_params(params):
    """Configura parámetros del modelo."""
    try:
        model_params = {"temperature": 0.7, "max_tokens": 200}  # Parámetros por defecto
        if params:
            for param in params:
                key, value = param.split('=')
                model_params[key] = float(value) if '.' in value else int(value)
        model.configure(**model_params)
        print("Parámetros del modelo actualizados:", model_params)
    except Exception as e:
        messagebox.showerror("Error", f"Error configurando parámetros del modelo: {e}")

# Nuevo: Personalizar autosave
def toggle_autosave(enable=True):
    """Activa o desactiva la función de autosave."""
    global autosave_enabled
    autosave_enabled = enable
    print("Autosave", "activado." if enable else "desactivado.")

# Función para manejar los argumentos
def main(args):
    """Función principal que maneja los argumentos de entrada para generar respuestas del modelo."""
    global model, conversation_context, load, last_response, topic, API_KEY


    # Si no se envían comandos, se asume que se envía una pregunta de texto.
    if not args[0].startswith("--"):
        user_input = " ".join(args)
        response_text = generate_response(user_input)
        log_interaction(user_input, response_text)  # Nuevo: Registrar interacción
        print(" \n→", response_text)
        return

    try:
        # Mapeo de comandos cortos
        commands_map = {
            "--load": "--l",
            "--addload": "--al",
            "--showload": "--sl",
            "--loadimage": "--li",
            "--showwin": "--sw",
            "--saveload": "--sav",
            "--saverequest": "--sr",
            "--saveanswer": "--sa",
            "--savecontext": "--sc",
            "--autosave": "--as",
            "--newquestions": "--nq",
            "--send": "--s",
            "--listfiles": "--ls",
            "--clearcontext": "--cc",
            "--loadselect": "--lsel",
            "--loadmultiple": "--lm",
            "--info": "--i",
            "--export": "--exp",
            "--import": "--imp",
            "--search": "--s",
            "--settopic": "--st",
            "--reset": "--r",
            "--loadconfig": "--lc",  # Nuevo: Cargar configuración
            "--log": "--log",        # Nuevo: Registrar interacciones en el log
            "--setparams": "--sp",   # Nuevo: Configurar parámetros del modelo
            "--toggleautosave": "--ta"  # Nuevo: Activar/desactivar autosave
        }

        # Verificar el primer argumento
        command = args[0]
        
        # Usar el comando corto si está disponible
        if command in commands_map:
            command = commands_map[command]

        if command == "--lc" or command == "--loadconfig":
            if len(args) > 1 and is_file(args[1]):
                config = load_config(args[1])
                API_KEY = config.get("api_key", API_KEY)
                # Reconfigurar API si se carga una nueva clave
                genai.configure(api_key=API_KEY)
            else:
                messagebox.showerror("Error", "Archivo de configuración no encontrado o no especificado.")
            return

        elif command == "--log":
            if len(args) > 1:
                log_interaction(" ".join(args[1:]), last_response)
            else:
                messagebox.showerror("Error", "No se especificó la interacción a registrar.")
            return

        elif command == "--sp" or command == "--setparams":
            if len(args) > 1:
                set_model_params(args[1:])
            else:
                messagebox.showerror("Error", "No se especificaron parámetros.")
            return

        elif command == "--ta" or command == "--toggleautosave":
            enable = args[1].lower() == 'on' if len(args) > 1 else True
            toggle_autosave(enable)
            return

        elif command == "--l" or command == "--load":
            if len(args) > 1 and is_file(args[1]):
                load = read_file(args[1])
                print(f"Contenido cargado desde {args[1]}")
            else:
                messagebox.showerror("Error", "Archivo no encontrado o no especificado.")
            return

        elif command == "--al" or command == "--addload":
            args.pop(0)  # Remover '--addload' de los argumentos
            user_input = " ".join(args)
            if load:
                user_input = load + " " + user_input  # Añadir el contenido de 'load' al input del usuario
            response_text = generate_response(user_input)
            print(" \n→", response_text)
            return

        elif command == "--sl" or command == "--showload":
            if load:
                print(f"Contenido de load:\n{load}")
            else:
                messagebox.showinfo("Información", "No hay contenido en 'load'.")
            return


        elif command == "--li" or command == "--loadimage":
            textWithImage = "Interpretar imagen"
            if len(args) > 2:
                textWithImage = " ".join(args[2:])
            if len(args) > 1 and args[1] == "--fd": # Si el segundo argumento es "fd" 
                # Abrir File Dialog para seleccionar la imagen
                image_path = filedialog.askopenfilename(
                    initialdir=".",
                    title="Seleccionar imagen",
                    filetypes=(("Imágenes", "*.jpg *.jpeg *.png *.gif"), ("Todos los archivos", "*.*"))
                )
                if image_path: # Si se seleccionó una imagen
                    generated_text = generate_with_image(image_path,textWithImage)
                    if generated_text:
                        conversation_context += f"{textWithImage} : {generated_text}\n"
                        print(" \n→", generated_text)
                else:
                    messagebox.showinfo("Información", "No se seleccionó ninguna imagen.")
            elif len(args) > 1:
                textWithImage += ""
                image_path = args[1]
                if is_file(image_path):
                    generated_text = generate_with_image(image_path,textWithImage)
                    if generated_text:
                        conversation_context += f"{textWithImage} : {generated_text}\n"
                        print(" \n→", generated_text)
                elif image_path.startswith(('http://', 'https://')):
                    generated_text = generate_with_image(image_path,textWithImage)
                    if generated_text:
                        conversation_context += f"{textWithImage} : {generated_text}\n"
                        print(" \n→", generated_text)
                else:
                    messagebox.showerror("Error", "Imagen no encontrada o no especificada.")
            else:
                messagebox.showerror("Error", "No se especificó una ruta de imagen.")



        elif command == "--sw" or command == "--showwin":
            if conversation_context:
                show_text_window(conversation_context)
            else:
                messagebox.showinfo("Información", "No hay texto para mostrar.")
            return
            
        elif command == "--ss" or command == "--screenshot":
            screen_shot()
            return            
            
            
        elif command == "--sla" or command == "--showlastanswer":
            if conversation_context:
                show_text_window(last_response)
            else:
                messagebox.showinfo("Información", "No hay texto para mostrar.")
            return
            
        elif command == "--la" or command == "--loadanswer":
            if conversation_context:
                load = last_response
                print("Cargada última respuesta")
            else:
                messagebox.showinfo("Información", "No hay información (L 486) para mostrar.")
            return            

        elif command == "--sav" or command == "--saveload":
            filename = "com/datas/saveload.gemini"  # Nombre por defecto
            if len(args) > 1:
                filename = f"com/datas/{args[1]}.gemini"  # Nombre personalizado
            save_file(filename, conversation_context)
            return

        elif command == "--sr" or command == "--saverequest":
            if len(args) > 1:
                user_input = " ".join(args[1:])
                save_request(user_input)
            else:
                messagebox.showerror("Error", "No se especificó solicitud a guardar.")
            return

        elif command == "--sa" or command == "--saveanswer":
            if len(args) > 1:
                filename = f"{args[1]}"  # Nombre personalizado
            else:
                filename=""
            save_answer(filename)
            return

        elif command == "--sc" or command == "--savecontext":
            save_context()
            return

        elif command == "--as" or command == "--autosave":
            autosave()
            return

        elif command == "--nq" or command == "--newquestions":
            if len(args) > 1:
                questions = generate_new_questions(" ".join(args[1:]))
                print("Preguntas generadas:")
                for q in questions:
                    print(" -", q)
            else:
                messagebox.showerror("Error", "No se especificó una pregunta base.")
            return

        elif command == "--sd" or command == "--send":
            if len(args) > 1:
                user_input = " ".join(args[1:])
                response_text = generate_response(user_input)
                print(" \n→", response_text)
            else:
                messagebox.showerror("Error", "No se especificó pregunta a enviar.")
            return

        elif command == "--ls" or command == "--listfiles":
            print("Listando archivos en com/datas:")
            for filename in os.listdir("com/datas"):
                print(" -", filename)
            return

        elif command == "--cc" or command == "--clearcontext":
            conversation_context = ""
            print("Contexto de conversación limpiado.")
            return

        elif command == "--lsel" or command == "--loadselect":
            if len(args) > 1 and is_file(args[1]):
                selected_context = read_file(args[1])
                conversation_context += selected_context + "\n"
                print("Contexto seleccionado cargado.")
            else:
                messagebox.showerror("Error", "Archivo no encontrado o no especificado.")
            return

        elif command == "--lm" or command == "--loadmultiple":
            for filename in args[1:]:
                if is_file(filename):
                    selected_context = read_file(filename)
                    conversation_context += selected_context + "\n"
                    print(f"Contexto de {filename} cargado.")
                else:
                    messagebox.showerror("Error", f"Archivo {filename} no encontrado.")
            return

        elif command == "--i" or command == "--info":
            print("Información del modelo:")
            print(" - Modelo:", model)
            print(" - Contexto actual:", conversation_context)
            return

        elif command == "--exp" or command == "--export":
            if len(args) > 1:
                win.export_context(args[1],conversation_context)
            else:
                messagebox.showerror("Error", "No se especificó nombre para exportar.")
            return

        elif command == "--imp" or command == "--import":
            if len(args) > 1:
               conversation_context = win.import_context(args[1])
            else:
                messagebox.showerror("Error", "No se especificó nombre para importar.")
            return

        elif command == "--s" or command == "--search":
            load_context = False
            term = ""
            # Eliminamos el --search de los argumentos
            args.pop(0) 
            for arg in args:
                if arg == "--load":
                    load_context = True
                else:
                    term += arg + " "
            term = term.strip()
            if term:
                results = search_context(term, load_context)
            else:
                messagebox.showerror("Error", "No se especificó término de búsqueda.")
            return


        elif command == "--st" or command == "--settopic":
            if len(args) > 1:
                topic = " ".join(args[1:])
                print(f"Tema establecido: {topic}")
            else:
                messagebox.showerror("Error", "No se especificó tema a establecer.")
            return

        elif command == "--dialog":
            dtext = win.dialog_window()
            if dtext != "":
                print(" → ",dtext)
                response_text = generate_response(dtext)
                print(" → ",response_text)
            else:
                print("VOID D")
            return

        elif command == "--di" or command == "--decodeimage":
            if len(args) > 0:
                dim = args[1]
                decode_img(b"{dim}")
                print("DECODE")
            return


        elif command == "--tvl" or command == "--tvideol":
            if len(args) > 2:
                prompt = " ".join(args[2:])
            else:
                prompt = ""
            if len(args) > 1:
                print("Procesando....")
#                return

                video_translate(args[1],prompt)

            else:
                print("Es necesario parametro de video")
#            send_video()
            print("---FIN VIDEO ----")
            return  


        elif command == "--r" or command == "--reset":
            conversation_context = ""
            load = ""
            last_response = ""
            topic = ""
            print("Todos los valores han sido reseteados.")
            return  
        elif command == "--resetkey":
            print("keycom")
            API_KEY = obtener_key_gemini('resetkey')
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash") 
            return
        elif command == "--diagnostic" or command == "--d":
            if len(args) > 1 :
                if args[1] == "server":
                    com_d = ["sudo","tool/mrls"]
                    fileload = "com/datas/rls.gemini.ctrl"
                    text = "Realiza un diagnóstico del sistema"
                elif args[1] == "system":
                    com_d = ["sudo","tool/diagnosis1"]
                    fileload = "com/datas/system_info.gemini.ctrl"
                    text = "Realiza un diagnóstico del sistema"
                elif args[1] == "memory":
                    com_d = ["sudo","tool/memory"]
                    fileload = "com/datas/memory.gemini.ctrl"
                    text = "Realiza un diagnóstico del sistema"
                else:
                    print("Parámetro incorrecto")
                    return
            else:
                print("necesita parametro 2 (system, etc...)")
                return
            obj = {
             "mode":"fixed",
             "name":None,
             "com":com_d,
             "metadata":{"from":"gemini3.py"}
            }
            osiris2.multiprocess(obj)
            print("\n Intentando Reporte... cargando... \n ")
            main(["--l",fileload,text])
            print("\n Enviando reporte .....\n ")
            main(["--al","Realiza reporte"])
            print("\n Fin del reporte \n ")
            return

    except Exception as e:
        if not API_KEY:
            try:
                API_KEY = obtener_key_gemini()  # Obtiene una nueva clave
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash")  # Reinicializa el modelo
            except Exception as f:
                print("Error API_KEY:",f)
                return
        print("Error:",e)
# Ejecutar el programa
if __name__ == "__main__":
    main(sys.argv[1:])

