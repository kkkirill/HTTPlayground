from pathlib import Path
from sys import argv
from jinja2 import Environment, FileSystemLoader

PORT = 8000
URL = 'localhost'

if len(argv) > 2:
    PORT = int(argv[2])
    URL = argv[1]

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = 'templates'
STATIC_URL = 'static'

TEMPLATE_ENV = Environment(loader=FileSystemLoader(searchpath=str(Path(BASE_DIR, TEMPLATE_DIR))))
