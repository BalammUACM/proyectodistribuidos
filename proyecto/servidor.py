import socket
from threading import Thread
import random
import time
from moviepy.editor import VideoFileClip
from pygame import mixer

# Simula la detección de una falla en un nodo
def detectar_falla(nodos):
    if random.random() < 0.25:  # Probabilidad de falla: 25%
        nodo_fallido = random.choice(nodos)
        return f"Falla en el nodo {nodo_fallido}"
    return "No se detectaron fallas"

# Función para manejar la solicitud de reproducción del video
def manejar_solicitud(cliente_socket, nodos):
    # Reproducir el video
    video_path = "video.mp4"
    audio_path = "audio.mp3"

    clip = VideoFileClip(video_path)
    clip.preview()

    # Reproducir el audio
    mixer.init()
    mixer.music.load(audio_path)
    mixer.music.play()

    # Verificar las fallas mientras se reproduce el video y el audio
    for segmento in range(1, 5):
        cliente_socket.sendall(f"Reproduciendo segmento {segmento}\n".encode())
        time.sleep(5)  # Simula la reproducción del segmento
        falla = detectar_falla(nodos)
        cliente_socket.sendall(falla.encode() + b'\n')

# Función para manejar la conexión de un cliente
def manejar_cliente(cliente_socket, direccion, nodos):
    print(f"Cliente conectado desde {direccion}")
    manejar_solicitud(cliente_socket, nodos)
    cliente_socket.close()
    print(f"Conexión con {direccion} cerrada")

# Función principal del servidor
def servidor():
    host = "127.0.0.1"
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind((host, port))
        servidor_socket.listen()

        print("Servidor escuchando en", (host, port))
        cliente_socket, direccion = servidor_socket.accept()
        cliente_thread = Thread(target=manejar_cliente, args=(cliente_socket, direccion, nodos))
        while True:
            #cliente_socket, direccion = servidor_socket.accept()
           # cliente_thread = Thread(target=manejar_cliente, args=(cliente_socket, direccion, nodos))
            cliente_thread.start()
        #cliente_thread.join()


# Lista de nodos
nodos = ["Nodo1", "Nodo2", "Nodo3", "Nodo4"]

# Iniciar el servidor
servidor()
