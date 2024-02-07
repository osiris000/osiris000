import pyaudio
import time

# Definimos los parámetros del micrófono
frecuencia_muestreo = 8000
canales = 1

# Iniciamos el flujo de audio
audio = pyaudio.PyAudio()
stream = audio.open(
    format=pyaudio.paInt16,
    channels=canales,
    rate=frecuencia_muestreo,
    input=True,
    frames_per_buffer=2048,
)

# Iniciamos el temporizador
inicio = time.time()

# Bucle para escuchar el micrófono
while time.time() - inicio < 10:
    # Leemos los datos del micrófono
    audio_data = stream.read(2048)

    # Convertimos los datos a texto
    audio_texto = audio_data.decode("utf-8")

    # Imprimimos el texto a la consola
    print(audio_texto)

# Cerramos el flujo de audio
stream.close()

# Detenemos el objeto de audio
audio.terminate()
