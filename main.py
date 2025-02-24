# main.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sassha: Un cliente y servidor SSH versátil.
"""

import argparse
import logging
import sys

from sassha.client.client import SasshaClient
from sassha.server.server import SasshaServer

__author__ = 'LoboGuardian'
__copyright__ = "Copyright 2025, LoboGuardian"
__credits__ = ["LoboGuardian"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "LoboGuardian"
__email__ = "loboguardian@"
__status__ = "Beta"

# Configuración de logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Función principal que maneja la lógica de Sassha."""
    parser = argparse.ArgumentParser(description="Sassha: Cliente y servidor SSH.")
    subparsers = parser.add_subparsers(dest='command', help='Subcomandos: client, server')

    # Subparser para el cliente
    client_parser = subparsers.add_parser('client', help='Ejecutar el cliente SSH.')
    client_parser.add_argument('host', help='Dirección del servidor SSH.')
    client_parser.add_argument('-p', '--port', type=int, default=22, help='Puerto del servidor SSH.')
    client_parser.add_argument('-u', '--user', help='Nombre de usuario para la conexión SSH.')
    client_parser.add_argument('-k', '--key', help='Ruta a la llave privada SSH.')

    # Subparser para el servidor
    server_parser = subparsers.add_parser('server', help='Ejecutar el servidor SSH.')
    server_parser.add_argument('-p', '--port', type=int, default=2222, help='Puerto del servidor SSH.')

    args = parser.parse_args()

    if args.command == 'client':
        logger.info("Ejecutando el cliente Sassha.")
        client = SasshaClient(args.host, args.port, args.user, args.key)
        try:
            client.connect()
        except Exception as e:
            logger.error(f"Error en el cliente: {e}")
            sys.exit(1)

    elif args.command == 'server':
        logger.info("Ejecutando el servidor Sassha.")
        server = SasshaServer(args.port)
        try:
            server.start()
        except Exception as e:
            logger.error(f"Error en el servidor: {e}")
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()