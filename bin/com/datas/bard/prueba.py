import subprocess

# Definimos los parámetros del video
duracion = 10
ancho = 1280
alto = 720

# Creamos el video
video = "video_vacio.mp4"
video = ""
# Aplicamos los filtros
filtros = ["tint=color=(0,0,0.8)", "noise=mode=add,amount=0.05", "defocus=radius=10"]

# Capturamos el video de la webcam
webcam = "v4l2src device=/dev/video0"

# Agregamos el recuadro a la esquina superior izquierda
posicion = "x=0,y=0,width=200,height=200"

# Escribimos el video
comando = f"ffmpeg {video} -filter_complex '{', '.join(filtros)}' -vf 'overlay=file={webcam},{posicion}' -c:v libx264 -c:a aac -b:v 1024k -b:a 128k video_naturaleza_webcam.mp4"

# Ejecutamos el comando ffmpeg
subprocess.run(comando)
