# sassha/core/connection.py
import logging
import paramiko
import socket

logger = logging.getLogger(__name__)

class SSHConnection:
    def __init__(self, host, port=22, username=None, key_path=None):
        self.host = host
        self.port = port
        self.username = username
        self.key_path = key_path
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # For testing only, remove in production!

            if self.key_path:
                private_key = paramiko.RSAKey.from_private_key_file(self.key_path)
                self.client.connect(hostname=self.host, port=self.port, username=self.username, pkey=private_key)
            else:
                self.client.connect(hostname=self.host, port=self.port, username=self.username)

            logger.info(f"Conectado a {self.host}:{self.port}")

        except paramiko.AuthenticationException:
            logger.error("Error de autenticación. Verifica tus credenciales.")
            raise
        except paramiko.SSHException as e:
            logger.error(f"Error SSH: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            raise

    def close(self):
        if self.client:
            self.client.close()

class SSHServerConnection:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.transport = None

    def start_server(self):
        try:
            self.transport = paramiko.Transport(self.client_socket)
            self.transport.add_server_key(paramiko.RSAKey.generate(2048)) #generate a key for each server session
            from sassha.sassha.core.authentication import ServerInterface #import locally to avoid circular imports.
            self.transport.start_server(server=ServerInterface())

        except Exception as e:
            logger.error(f"Error al iniciar el servidor SSH: {e}")
            raise

    def accept_channel(self, timeout=20):
        try:
            channel = self.transport.accept(timeout)
            return channel
        except Exception as e:
            logger.error(f"Error al aceptar el canal SSH: {e}")
            raise

    def close(self):
        if self.transport:
            self.transport.close()