import socket
import sys
 
# Crear socket
socketConexion = socket.socket()
 
# Servidor de conexión
servidor = input("Introduzca la dirección IP o nombre del servidor: ")
# El puerto a utilizar (el servidor debe estar escuchando en este puerto)
puerto = int(input("Introduzca el puerto de conexión: "))
 
try:
    # Conectar el socket del cliente con el servidor en el puerto indicado
    socketConexion.connect((servidor, puerto))
except socket.error as message:
    print("Falló la conexión con el servidor {} por el puerto {}".format(servidor, puerto))
    print(message)
    sys.exit()  
 
# Recibir y mostrar el mensaje del servidor
mensajeServidor = socketConexion.recv(1024)
print(mensajeServidor.decode())
# Cerrar el socket
socketConexion.close()