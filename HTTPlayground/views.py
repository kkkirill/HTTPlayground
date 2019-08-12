from cgi import FieldStorage
from jinja2 import Template
from HTTPlayground.base import FileReader, CookieHandler, send_headers
from HTTPlayground.settings import ACCESSORY_URL_PREFIX


def login(request):
    cookie_header = {'Set-Cookie': CookieHandler.generate_cookie(request, {'auth': 'True'})}
    send_headers(request, content_type='text/html', **cookie_header)
    t = Template(FileReader.read('login.html'))
    rendered_html = t.render(link=f'{ACCESSORY_URL_PREFIX}/form')
    return rendered_html


def logout(request):
    cookie_header = {'Set-Cookie': CookieHandler.generate_cookie(request, {'auth': 'False'})}
    send_headers(request, content_type='text/html', **cookie_header)
    t = Template(FileReader.read('logout.html'))
    rendered_html = t.render(link=f'{ACCESSORY_URL_PREFIX}/form')
    return rendered_html


def get_form(request):
    send_headers(request, content_type='text/html')
    form_text = {'form_link': (f'{ACCESSORY_URL_PREFIX}/charge', f'{ACCESSORY_URL_PREFIX}/charge'),
                 'auth_link': (f'{ACCESSORY_URL_PREFIX}/authh/login', f'{ACCESSORY_URL_PREFIX}/authh/logout'),
                 'auth_text': ('Login', 'Logout')}
    is_authenticated = CookieHandler.is_cookie(request, {'auth': 'True'})
    t = Template(FileReader.read('form.html'))
    rendered_html = t.render(**{k: v[is_authenticated] for k, v in form_text.items()})
    return rendered_html


def process_form(request):
    send_headers(request, content_type='text/html')
    if not CookieHandler.is_cookie(request, {'auth': 'True'}):
        return
    form = FieldStorage(
        fp=request.rfile,
        headers=request.headers,
        environ={'REQUEST_METHOD': 'POST'}
    )
    t = Template(FileReader.read('charged.html'))
    rendered_html = t.render(link=f'{ACCESSORY_URL_PREFIX}/form', text=f'OK. {form.getvalue("sum_value")}$ charged!')
    return rendered_html


def not_found(request):
    send_headers(request, content_type='text/html')
    return Template(FileReader.read('not_found.html')).render(link=f'{ACCESSORY_URL_PREFIX}/form')
