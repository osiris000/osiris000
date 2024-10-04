#API_KEY = os.getenv("GOOGLE_API_KEY")  # Cambiar a variable de entorno


# Configuración del API
API_KEY = "AQUI LA KEY DE GEMINI"

import google.generativeai as genai
import os
import json
from PIL import Image
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import time

# Configuración del API
genai.configure(api_key=API_KEY)

# Inicialización del modelo generativo
model = genai.GenerativeModel("gemini-1.5-flash")

# Variables globales
conversation_context = ""
load = ""
last_response = ""
topic = ""  # Tema de conversación

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

def load_image(file_path):
    """Carga y muestra una imagen usando PIL."""
    try:
        img = Image.open(file_path)
        img.show()  # Muestra la imagen
        return img
    except Exception as e:
        messagebox.showerror("Error", f"Error cargando la imagen {file_path}: {e}")
        return None

def show_text_window(text):
    """Muestra el texto en una ventana de tkinter con soporte para selección y copia."""
    root = tk.Tk()
    root.title("Contenido de la conversación")
    text_widget = scrolledtext.ScrolledText(root, wrap="word")
    text_widget.insert(tk.END, text)
    text_widget.pack(expand=True, fill="both")
    text_widget.config(state=tk.NORMAL)  # Permite selección de texto
    root.mainloop()

def generate_with_image(image_path):
    """Genera texto a partir de una imagen usando la API de Gemini."""
    image = load_image(image_path)
    if image:
        response = model.generate_content(image=image)
        return response.text
    return None

def generate_response(user_input):
    """Genera una respuesta del modelo basada en la entrada del usuario."""
    global conversation_context, last_response, topic
    conversation_context += f"User: {user_input}\n"
    try:
        response = model.generate_content(conversation_context)
        response_text = response.text
        conversation_context += f"AI: {response_text}\n"
        last_response = response_text  # Guarda la última respuesta
        return response_text
    except Exception as e:
        messagebox.showerror("Error", f"Error generando contenido con el modelo: {e}")
        return None

def save_request(user_input):
    """Guarda la solicitud del usuario en un archivo."""
    save_file("com/datas/lastrequest.gemini", user_input)

def save_answer():
    """Guarda la última respuesta generada en un archivo."""
    global last_response
    save_file("com/datas/lastanswer.gemini", last_response)

def save_context():
    """Guarda el contexto de la conversación en un archivo."""
    save_file("com/datas/context.gemini", conversation_context)

def autosave():
    """Guarda automáticamente la última respuesta y el contexto."""
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

def export_context(filename):
    """Exporta el contexto de la conversación a un archivo JSON."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({"context": conversation_context}, f)
        print(f"Contexto exportado a {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Error exportando contexto: {e}")

def import_context(filename):
    """Importa el contexto de una conversación desde un archivo JSON."""
    global conversation_context
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            conversation_context = data.get("context", "")
        print(f"Contexto importado desde {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Error importando contexto: {e}")

def search_context(term):
    """Busca un término en el contexto de la conversación."""
    results = [line for line in conversation_context.splitlines() if term in line]
    return results if results else ["No se encontraron coincidencias."]






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
    global model, conversation_context, load, last_response, topic

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
            if len(args) > 1 and is_file(args[1]):
                generated_text = generate_with_image(args[1])
                if generated_text:
                    conversation_context += f"AI: {generated_text}\n"
                    print(" \n→", generated_text)
            else:
                messagebox.showerror("Error", "Imagen no encontrada o no especificada.")
            return

        elif command == "--sw" or command == "--showwin":
            if conversation_context:
                show_text_window(conversation_context)
            else:
                messagebox.showinfo("Información", "No hay texto para mostrar.")
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
            save_answer()
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

        elif command == "--s" or command == "--send":
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
                export_context(args[1])
            else:
                messagebox.showerror("Error", "No se especificó nombre para exportar.")
            return

        elif command == "--imp" or command == "--import":
            if len(args) > 1:
                import_context(args[1])
            else:
                messagebox.showerror("Error", "No se especificó nombre para importar.")
            return

        elif command == "--s" or command == "--search":
            if len(args) > 1:
                results = search_context(" ".join(args[1:]))
                print("Resultados de búsqueda:")
                for line in results:
                    print(" -", line)
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

        elif command == "--r" or command == "--reset":
            conversation_context = ""
            load = ""
            last_response = ""
            topic = ""
            print("Todos los valores han sido reseteados.")
            return            

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
