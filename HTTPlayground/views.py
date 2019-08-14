from cgi import FieldStorage
from jinja2 import Template
from HTTPlayground.base import FileReader, CookieHandler, TokensDB, send_headers
from HTTPlayground.settings import ACCESSORY_URL_PREFIX, SALT


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
    secret_token = hash(f'{hash(CookieHandler.generate_cookie(request, {"auth": "True"}))}{hash(SALT)}')
    TokensDB.add_token(secret_token)
    form_text = {'form_link': (f'{ACCESSORY_URL_PREFIX}/charge', f'{ACCESSORY_URL_PREFIX}/charge'),
                 'auth_link': (f'{ACCESSORY_URL_PREFIX}/auth/login', f'{ACCESSORY_URL_PREFIX}/auth/logout'),
                 'auth_text': ('Login', 'Logout'),
                 'secret_token': (secret_token, secret_token)}
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
    form_text = '{msg}. {sum_msg} charged!'
    if not TokensDB.is_token_valid(form.getvalue('secret_token')):
        form_text = form_text.format(msg='OK', sum_msg=form.getvalue("sum_value"))
    else:
        form_text = form_text.format(msg='ERROR', sum_msg='Nothing')
    t = Template(FileReader.read('charged.html'))
    rendered_html = t.render(link=f'{ACCESSORY_URL_PREFIX}/form', text=form_text)
    return rendered_html


def not_found(request):
    send_headers(request, content_type='text/html')
    return Template(FileReader.read('not_found.html')).render(link=f'{ACCESSORY_URL_PREFIX}/form')
