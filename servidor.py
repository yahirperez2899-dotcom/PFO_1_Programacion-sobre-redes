import socket
import sqlite3
from datetime import datetime


def inicializar_db():
    """Crea la base de datos y la tabla de mensajes si no existen."""
    try:
        conexion = sqlite3.connect("chat.db")
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)

        conexion.commit()
        conexion.close()

        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as error:
        print(f"Error al inicializar la base de datos: {error}")


def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    """Guarda un mensaje recibido en la base de datos."""
    try:
        conexion = sqlite3.connect("chat.db")
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))

        conexion.commit()
        conexion.close()

        return True

    except sqlite3.Error as error:
        print(f"Error al guardar el mensaje: {error}")
        return False


def inicializar_socket():
    """Configura e inicia el socket del servidor."""
    try:
        # Configuración del socket TCP/IP
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Permite reutilizar el puerto después de cerrar el servidor
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Configuración de localhost y puerto 5000
        servidor.bind(("localhost", 5000))

        # El servidor comienza a "escuchar" conexiones
        servidor.listen()

        print("Servidor escuchando en localhost:5000")

        return servidor

    except OSError as error:
        print(f"Error al iniciar el servidor: {error}")
        return None


def atender_cliente(servidor):
    """Acepta conexiones y procesa los mensajes enviados por los clientes."""

    while True:
        try:
            # Espera una conexión de un cliente
            cliente, direccion = servidor.accept()

            print(f"Cliente conectado desde {direccion[0]}")

            while True:
                # Recibe datos del cliente
                datos = cliente.recv(1024)

                # Si no recibe datos, el cliente se desconecta
                if not datos:
                    break

                mensaje = datos.decode("utf-8")

                # Obtiene la fecha y hora actual del envio
                fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Obtiene la IP del cliente
                ip_cliente = direccion[0]

                # Guarda el mensaje en la base de datos
                guardado = guardar_mensaje(
                    mensaje,
                    fecha_envio,
                    ip_cliente
                )

                if guardado:
                    # Envía una confirmación al cliente
                    respuesta = f"Mensaje recibido: {fecha_envio}"
                    cliente.sendall(respuesta.encode("utf-8"))
                else:
                    # Informa al cliente si hubo un problema con la DB
                    respuesta = "Error al guardar el mensaje."
                    cliente.sendall(respuesta.encode("utf-8"))

            cliente.close()
            print("Cliente desconectado.")

        except ConnectionResetError:
            print("El cliente cerró la conexión inesperadamente.")

        except OSError as error:
            print(f"Error en la comunicación con el cliente: {error}")


def main():
    # Inicializa la base de datos
    inicializar_db()

    # Inicializa el socket del servidor
    servidor = inicializar_socket()

    if servidor is not None:
        try:
            # Comienza a aceptar y atender clientes
            atender_cliente(servidor)

        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")

        finally:
            servidor.close()
            print("Socket del servidor cerrado.")


if __name__ == "__main__":
    main()
