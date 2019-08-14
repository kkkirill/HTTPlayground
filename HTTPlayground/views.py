from cgi import FieldStorage
from HTTPlayground.base import CookieHandler, send_headers, require_http_methods
from settings import TEMPLATE_ENV


def not_found(request):
    send_headers(request, response_code=404, content_type='text/html')
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    rendered_html = file.render(title='Not found', link='/form', text='404 error. Page not found!')
    return rendered_html


@require_http_methods(['GET'], not_found)
def login(request):
    cookie_header = {'Set-Cookie': CookieHandler.generate_cookie(request, name='auth', value='True')}
    send_headers(request, content_type='text/html', **cookie_header)
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    rendered_html = file.render(title='Login', link='/form', text='Successful login.')
    return rendered_html


@require_http_methods(['GET'], not_found)
def logout(request):
    cookie_header = {'Set-Cookie': CookieHandler.generate_cookie_for_remove(request, name='auth')}
    send_headers(request, content_type='text/html', **cookie_header)
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    rendered_html = file.render(title='Logout', link='/form', text='Successful logout.')
    return rendered_html


@require_http_methods(['GET'], not_found)
def get_form(request):
    send_headers(request, content_type='text/html')
    form_text = {'title': ('form', 'form'),
                 'form_link': ('/charge', '/charge'),
                 'auth_link': ('/authh/login', '/authh/logout'),
                 'auth_text': ('Login', 'Logout')}
    is_authenticated = CookieHandler.has_cookie(request, name='auth', value='True')
    file = TEMPLATE_ENV.get_template('form.html')
    rendered_html = file.render(**{k: v[is_authenticated] for k, v in form_text.items()})
    return rendered_html


@require_http_methods(['POST'], not_found)
def process_form(request):
    send_headers(request, content_type='text/html')
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    if not CookieHandler.has_cookie(request, name='auth', value='True'):
        return file.render(title='Error', link='/form', text='Not authorized!')
    form = FieldStorage(
        fp=request.rfile,
        headers=request.headers,
        environ={'REQUEST_METHOD': 'POST'}
    )
    rendered_html = file.render(title='Charged', link='/form', text=f'OK. {form.getvalue("sum_value")}$ charged!')
    return rendered_html
