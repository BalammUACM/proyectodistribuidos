import socket

# Función para conectar al servidor y solicitar la reproducción del video
def solicitar_reproduccion():
    host = "192.128.0.2"
    port = 1000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
        cliente_socket.connect((host, port))

        while True:
            mensaje = cliente_socket.recv(1024).decode()
            print(mensaje)
            if mensaje.startswith("Falla"):
                print("¡Se detectó una falla en un nodo!")
            elif mensaje.startswith("No se detectaron"):
                print("No se detectaron fallas en los nodos.")

# Solicitar la reproducción del video
solicitar_reproduccion()
