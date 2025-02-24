# sassha/server/server.py
import logging
import socket
import threading
import paramiko

from sassha.core.authentication import ServerInterface
from sassha.core.connection import SSHServerConnection

logger = logging.getLogger(__name__)

class SasshaServer:
    def __init__(self, port=2222):
        self.port = port
        self.sock = None

    def start(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('0.0.0.0', self.port))
            self.sock.listen(100)
            logger.info(f"Servidor SSH escuchando en el puerto {self.port}")

            while True:
                client, addr = self.sock.accept()
                logger.info(f"Conexión entrante desde {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(client,))
                client_thread.start()

        except Exception as e:
            logger.error(f"Error en el servidor: {e}")
        finally:
            if self.sock:
                self.sock.close()

    def handle_client(self, client_sock):
        try:
            connection = SSHServerConnection(client_sock)
            connection.start_server()
            channel = connection.accept_channel()

            if channel is None:
                logger.error("No se pudo obtener un canal.")
                return

            channel.send("Bienvenido a Sassha Server!\n")
            while True:
                command = channel.recv(1024).decode().strip()
                if not command:
                    break
                # Implement command handling here. For example:
                channel.send(f"Comando recibido: {command}\n")

        except Exception as e:
            logger.error(f"Error al manejar el cliente: {e}")
        finally:
            connection.close()