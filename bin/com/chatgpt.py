import requests

# Declarar la API key como una constante
API_KEY = ""
ORGANIZATION = ""
MODEL = "text-davinci-003"  # Utilizamos el modelo GPT-3.5 en lugar de GPT-2.5
URL = "https://api.openai.com/v1/engines"

def get_chat_response(input_text):
    url = f"{URL}/{MODEL}/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "Organization": f"{ORGANIZATION}"
    }
    data = {
        "prompt": input_text,
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return None

def main(args):
    print("Args dentro de chatgpt.py:", args)

    if not API_KEY:
        print("No se proporcionó la clave de API.")
        return

    print("¡Bienvenido a ChatGPT!")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit", "q"]:
            print("¡Hasta luego!")
            break

        if not user_input.strip():
            print("No se proporcionó ningún mensaje.")
            continue
        
        response = get_chat_response(user_input)
        if response is not None:
            print("ChatGPT:", response)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])  # Pasamos los argumentos sin el primer elemento que es el nombre del script



print('Creado módulo-comando chatgpt y fecha y hora: 2023-07-23 10:18:36.718879')
