from pathlib import Path
from sys import argv

PORT = 8000
URL = 'localhost'

if len(argv) > 2:
    PORT = int(argv[2])
    URL = argv[1]

BASE_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = 'templates'
STATIC_URL = 'static'
