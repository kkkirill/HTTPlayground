from pathlib import Path
from settings import BASE_DIR, TEMPLATE_DIR, STATIC_URL


class FileReader:

    @staticmethod
    def read(filename: str, mode: str = 't', encoding: str = 'utf-8'):
        """binary mode - b, text mode - t"""
        is_template = filename.endswith('.html')
        path = Path(BASE_DIR, (TEMPLATE_DIR if is_template else STATIC_URL), filename)
        if path.exists():
            return path.read_text(encoding) if mode == 't' else path.read_bytes()
        else:
            raise FileNotFoundError(f'Cannot find file:\n{path}')
