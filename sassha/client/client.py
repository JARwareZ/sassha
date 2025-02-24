# sassha/client/client.py
import logging
import paramiko
import sys

from sassha.core.connection import SSHConnection

logger = logging.getLogger(__name__)

class SasshaClient:
    def __init__(self, host, port=22, username=None, key_path=None):
        self.host = host
        self.port = port
        self.username = username
        self.key_path = key_path
        self.connection = SSHConnection(host, port, username, key_path)  # Usamos la clase SSHConnection

    def connect(self):
        try:
            self.connection.connect()
            logger.info(f"Conectado a {self.host}:{self.port}")
            self.interactive_shell()

        except paramiko.AuthenticationException:
            logger.error("Error de autenticación. Verifica tus credenciales.")
            sys.exit(1)
        except paramiko.SSHException as e:
            logger.error(f"Error SSH: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            sys.exit(1)

    def interactive_shell(self):
        try:
            channel = self.connection.client.invoke_shell()
            while True:
                command = input(f"{self.username}@{self.host}:~$ ")
                channel.send(command + '\n')
                while channel.recv_ready():
                    output = channel.recv(1024).decode()
                    print(output, end='')

        except KeyboardInterrupt:
            logger.info("Sesión terminada por el usuario.")
        except Exception as e:
            logger.error(f"Error en el shell interactivo: {e}")
        finally:
            self.connection.close()