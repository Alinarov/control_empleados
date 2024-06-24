import socket

def obtener_nombre_servidor():
    try:
        nombre_servidor = socket.gethostname()
        return nombre_servidor
    except Exception as e:
        print("Error al obtener el nombre del servidor:", e)
        return None

