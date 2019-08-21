from functools import wraps
from http.cookies import SimpleCookie
from pathlib import Path
from mimetypes import guess_type
from HTTPlayground.settings import BASE_DIR, STATIC_URL


def require_http_methods(request_method_list, error_handler):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.command not in request_method_list:
                return error_handler(request, *args, **kwargs)
            return func(request, *args, **kwargs)
        return inner
    return decorator


def send_headers(request, response_code: int = 200, content_type: str = 'text/plain', **kwargs):
    request.send_response(response_code)
    request.send_header('Content-type', content_type)
    for k, v in kwargs.items():
        request.send_header(k, v)
    request.end_headers()


def process_static(request):
    filename = request.path.rsplit('/', 1)[-1]
    path = Path(BASE_DIR, STATIC_URL, filename)
    if path.exists():
        send_headers(request, content_type=guess_type(request.path)[0])
        return path.read_text('utf-8')


class CookieHandler:
    @staticmethod
    def has_cookie(request, *, name, value):
        raw_cookies = request.headers.get('Cookie')
        cookies = SimpleCookie(raw_cookies)
        cookie = cookies.get(name)
        return getattr(cookie, 'value', None) == value

    @staticmethod
    def generate_cookie_for_remove(request, *, name):
        cookie = SimpleCookie(request.headers.get('Cookie'))
        cookie[name] = 'deleted'
        cookie[name]['path'] = '/'
        cookie[name]['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        cookie[name]['httponly'] = True
        return cookie.output(header='', sep='')

    @classmethod
    def generate_cookie(cls, request, *, name, value):
        cookie = SimpleCookie(request.headers.get('Cookie'))
        cookie[name] = value
        cookie[name]['path'] = '/'
        cookie[name]['httponly'] = True
        return cookie.output(header='', sep='')
