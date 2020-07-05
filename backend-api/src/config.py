import os
import re
import logging

DEBUG = True
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT', '5000'))
DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_NAME = re.search(r'/(\w+)$', DATABASE_URL).group(1)

logging.basicConfig(
    filename=os.getenv('SERVICE_LOG', 'server.log'),
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(levelname)s: %(asctime)s pid:%(process)s "
    "module:%(module)s %(message)s",
    datefmt='%d/%m/%y %H:%M:%S',
)
