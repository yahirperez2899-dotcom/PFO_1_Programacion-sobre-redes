import socket


def conectar_servidor():
    """Crea el socket y se conecta al servidor."""

    try:
        # Configuración del socket TCP/IP 
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Conexión al servidor en localhost y puerto 5000
        cliente.connect(("localhost", 5000))

        print("Conectado al servidor.")

        return cliente

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")
        print("Verificá que el servidor esté ejecutándose.")

        return None

    except OSError as error:
        print(f"Error de conexión: {error}")

        return None


def enviar_mensajes(cliente):
    """Permite enviar múltiples mensajes al servidor."""

    while True:
        mensaje = input(
            "Escribí un mensaje (o 'exito' para salir): "
        )

        # Finaliza el cliente solo cuando el usuario escriba "exito"
        if mensaje.lower() == "exito":
            break

        try:
            # Envía el mensaje al servidor
            cliente.sendall(mensaje.encode("utf-8"))

            # Espera la respuesta del servidor
            respuesta = cliente.recv(1024).decode("utf-8")

            print(f"Servidor: {respuesta}")

        except ConnectionResetError:
            print("El servidor cerró la conexión.")
            break

        except OSError as error:
            print(f"Error durante la comunicación: {error}")
            break


def main():
    cliente = conectar_servidor()

    if cliente is not None:
        try:
            enviar_mensajes(cliente)

        finally:
            # Cierra la conexión con el servidor 
            cliente.close()
            print("Conexión cerrada.")


if __name__ == "__main__":
    main()
