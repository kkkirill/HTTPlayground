from http.cookies import SimpleCookie
from pathlib import Path
from HTTPlayground.settings import BASE_DIR, TEMPLATE_DIR, STATIC_URL, ACCESSORY_URL_PREFIX


def send_headers(request, response_code: int = 200, content_type: str = 'text/plain', **kwargs):
    request.send_response(response_code)
    request.send_header('Content-type', content_type)
    request.send_header('Access-Control-Allow-Credentials', 'true')
    request.send_header('Access-Control-Allow-Origin', f'{ACCESSORY_URL_PREFIX}')
    for k, v in kwargs.items():
        request.send_header(k, v)
    request.end_headers()


class CookieHandler:
    @staticmethod
    def is_cookie(request, cookie_pair: dict):
        raw_cookies = request.headers.get('Cookie')
        cookies = SimpleCookie(raw_cookies)
        k, v = tuple(cookie_pair.items())[0]
        cookie = cookies.get(f'{k}')
        return getattr(cookie, 'value', None) == v

    @staticmethod
    def get_cookie(request):
        return SimpleCookie(request.headers.get('Cookie'))

    @classmethod
    def generate_cookie(cls, request, cookie_pair: dict):
        cookie = cls.get_cookie(request)
        k, v = tuple(cookie_pair.items())[0]
        cookie[f"{k}"] = v
        cookie[f"{k}"]['path'] = '/'
        cookie[f"{k}"]['httponly'] = True
        return cookie.output(header='', sep='')


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


class TokensDB:
    token_base = set()

    @classmethod
    def is_token_valid(cls, token):
        return token in cls.token_base

    @classmethod
    def add_token(cls, token):
        cls.token_base.add(token)

    @classmethod
    def remove_token(cls, token):
        cls.token_base.remove(token)
