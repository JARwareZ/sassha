# sassha/core/authentication.py
import logging
import paramiko

logger = logging.getLogger(__name__)

class ServerInterface(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Implement authentication logic here. For example:
        if username == 'test' and password == 'test':
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        # Implement public key authentication logic here.
        # This is a basic example and should be enhanced for production.
        # You would typically check if the provided key matches a stored key for the user.
        # For example, you might read keys from a file or a database.
        logger.info(f"Intento de autenticación de clave pública para el usuario: {username}")
        # Basic example: allow all keys for 'test' user
        if username == 'test':
            logger.info("Autenticación de clave pública permitida para el usuario 'test'.")
            return paramiko.AUTH_SUCCESSFUL
        logger.info("Autenticación de clave pública denegada.")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        # Indicate allowed authentication methods
        return "password,publickey"

    def check_channel_shell_request(self, channel):
        # Allow shell requests
        return True