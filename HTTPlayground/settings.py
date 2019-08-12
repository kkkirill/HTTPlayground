from pathlib import Path
from sys import argv

SERVERS_INFO = {
    'URL0': '127.0.0.1', 'PORT0': 8000,
    'URL1': '127.255.255.254', 'PORT1': 8080
}

IS_MAIN_SERVER = not int(argv[1])

PORT = SERVERS_INFO.get(f'PORT{argv[1]}', SERVERS_INFO['PORT0'])
URL = SERVERS_INFO.get(f'URL{argv[1]}', SERVERS_INFO['URL0'])

ACCESSORY_PORT = SERVERS_INFO.get(f"PORT{int(not int(argv[1]))}", "PORT1")
ACCESSORY_URL = SERVERS_INFO.get(f"URL{int(not int(argv[1]))}", "URL1")

MAIN_URL_PREFIX = f'http://{URL}:{PORT}'
ACCESSORY_URL_PREFIX = f'http://{ACCESSORY_URL}:{ACCESSORY_PORT}'

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = 'templates'
STATIC_URL = 'static'
