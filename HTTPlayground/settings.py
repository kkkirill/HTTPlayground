from pathlib import Path
from sys import argv
from jinja2 import Environment, FileSystemLoader

SERVERS_INFO = {
    'URL0': '127.0.0.1', 'PORT0': 8000,
    'URL1': '0.0.0.0', 'PORT1': 8080  # 127.255.255.254
}

SALT = "удав"

IS_MAIN_SERVER = not int(argv[1])

PORT = SERVERS_INFO.get(f'PORT{argv[1]}', SERVERS_INFO['PORT0'])
URL = SERVERS_INFO.get(f'URL{argv[1]}', SERVERS_INFO['URL0'])

ACCESSORY_PORT = SERVERS_INFO.get(f"PORT{1 - int(argv[1])}", "PORT1")
ACCESSORY_URL = SERVERS_INFO.get(f"URL{1 - int(argv[1])}", "URL1")

MAIN_URL_PREFIX = f'http://{URL}:{PORT}'
ACCESSORY_URL_PREFIX = f'http://{ACCESSORY_URL}:{ACCESSORY_PORT}'

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = 'templates'
STATIC_URL = 'static'

TEMPLATE_ENV = Environment(loader=FileSystemLoader(searchpath=str(Path(BASE_DIR, TEMPLATE_DIR))))
