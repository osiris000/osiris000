from flask import Flask
import requests
import ffmpeg

# Función para procesar una imagen enviada desde el navegador
def process_image(data):
  # Convertir la cadena de datos de la imagen en un objeto `Blob`
  blob = b64decode(data)

  # Obtener el nombre de archivo de la imagen
  filename = "image.jpg"

  # Guardar la imagen en el disco
  with open(filename, "wb") as f:
    f.write(blob)

  # Convertir la imagen a un flujo HLS
  ffmpeg.input(filename).output("image.m3u8").run()

# Función para procesar un video enviado desde el navegador
def process_video(data):
  # Convertir la cadena de datos del video en un objeto `Blob`
  blob = b64decode(data)

  # Obtener el nombre de archivo del video
  filename = "video.mp4"

  # Guardar el video en el disco
  with open(filename, "wb") as f:
    f.write(blob)

  # Convertir el video a un flujo HLS
  ffmpeg.input(filename).output("video.m3u8").run()

# Escuchar las solicitudes POST
app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
  # Obtener el tipo de contenido de la solicitud
  content_type = request.headers["Content-Type"]

  # Si el tipo de contenido es image/jpeg, procesar la imagen
  if content_type == "image/jpeg":
    data = request.data
    process_image(data)

  # Si el tipo de contenido es video/mp4, procesar el video
  elif content_type == "video/mp4":
    data = request.data
    process_video(data)

  # Devolver un mensaje de éxito
  return "OK"

# Iniciar el servidor
app.run(host="0.0.0.0", port=8080)





def main(args):
    print('Args dentro de error', args)






print('Creado módulo-comando error y fecha y hora: 2023-07-22 17:36:46.637688')
