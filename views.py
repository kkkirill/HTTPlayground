from cgi import FieldStorage
from jinja2 import Template
from tools.file_reader import FileReader
from tools.cookie_handler import CookieHandler


def login(request):
    request.send_response(200)
    request.send_header('Content-type', 'text/plain')
    CookieHandler.set_cookie(request, {'auth': 'True'})
    request.end_headers()
    return 'OK'


def logout(request):
    request.send_response(200)
    request.send_header('Content-type', 'text/plain')
    CookieHandler.set_cookie(request, {'auth': 'False'})
    request.end_headers()
    return 'OK'


def get_form(request):
    request.send_response(202)
    request.send_header('Content-type', 'text/html')
    request.end_headers()
    form_text = {'form_link': ('/charge', '/charge'),
                 'auth_link': ('auth/login', 'auth/logout'),
                 'auth_text': ('Login', 'Logout')}
    is_authenticated = CookieHandler.is_cookie(request, {'auth': 'True'})
    t = Template(FileReader.read('form.html'))
    rendered_html = t.render(**{k: v[is_authenticated] for k, v in form_text.items()})
    return rendered_html


def process_form(request):
    request.send_response(202)
    request.send_header('Content-type', 'text/plain')
    request.end_headers()
    if not CookieHandler.is_cookie(request, {'auth': 'True'}):
        return 'Error! No Auth info!'
    form = FieldStorage(
        fp=request.rfile,
        headers=request.headers,
        environ={'REQUEST_METHOD': 'POST'}
    )
    return f'OK. {form.getvalue("sum_value")}$ charged!'


def not_found(request):
    return 'ERROR 404\n\nPage not found'
