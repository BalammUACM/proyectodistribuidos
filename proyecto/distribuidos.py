import random
import time
import socket
import pickle
from threading import Thread
import pygame
import moviepy.editor as mp


# Variable global para indicar si el programa debe seguir ejecutándose
seguir_ejecutando = True

# Simula la detección de una falla en un nodo
def detectar_falla(nodos):
    if random.random() < 0.25:  # Probabilidad de falla: 25%
        nodo_fallido = random.choice(nodos)
        print(f"Falla en el nodo {nodo_fallido} pero el usuario disfrutará de su video")
        return True
    return False

# Función para cargar y reproducir un segmento de video y audio
def reproducir_segmento(segmento):
    try:
        print(f"Reproduciendo segmento {segmento}")
        video_path = "video.mp4"
        audio_path = "audio.mp3"
        
        # Cargar el video
        video = mp.VideoFileClip(video_path)

        # Extraer el audio del video
        audio = video.audio

        # Reproducir el video
        pygame.init()
        pygame.display.set_caption("Reproducción de video")
        screen = pygame.display.set_mode(video.size)
        video.preview(fps=30, audio=audio, screen=screen)

    except Exception as e:
        print("Error en la reproducción del segmento:", e)

# Función para el servidor que verifica fallas y envía señales al cliente
def servidor(nodos):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind(("localhost", 12345))
        servidor_socket.listen(1)
        print("Servidor iniciado. Esperando conexión...")
        cliente_socket, addr = servidor_socket.accept()
        print("Cliente conectado.")

        with cliente_socket:
            while seguir_ejecutando:
                for segmento in range(1, 5):
                    if detectar_falla(nodos):
                        cliente_socket.send(pickle.dumps(True))  # Envía señal de falla al cliente
                        print("Señal de falla enviada al cliente.")
                    else:
                        cliente_socket.send(pickle.dumps(False))  # Envía señal de no falla al cliente
                        print("Reproducción normal, continúa la reproducción.")
                    
                    # Inicia la reproducción del segmento de video y audio en un hilo separado
                    segmento_thread = Thread(target=reproducir_segmento, args=(segmento,))
                    segmento_thread.start()
                    segmento_thread.join()  # Espera a que termine la reproducción del segmento
                    time.sleep(0.5)

# Función para el cliente que recibe señales del servidor y reproduce el video y audio
def cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        cliente_socket.connect(("localhost", 12345))

        while seguir_ejecutando:
            falla_detectada = pickle.loads(cliente_socket.recv(1024))  # Recibe señal del servidor
            if falla_detectada:
                print("Se detectó una falla, pero se continúa reproduciendo el video.")
            else:
                print("No se detectaron fallas.")
            
            # Reproduce el video y audio en el cliente
            reproducir_segmento(1)  
            time.sleep(0.5)

# Lista de nodos
nodos = ["Nodo1", "Nodo2", "Nodo3", "Nodo4"]

# Inicia el servidor y el cliente en hilos separados
servidor_thread = Thread(target=servidor, args=(nodos,))
cliente_thread = Thread(target=cliente)

servidor_thread.start()
cliente_thread.start()

# Espera a que los hilos terminen
servidor_thread.join()
cliente_thread.join()

# Al salir de los hilos, detenemos la ejecución del programa
seguir_ejecutando = False


