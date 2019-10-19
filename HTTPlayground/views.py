from cgi import FieldStorage
from HTTPlayground.base import CookieHandler, send_headers, require_http_methods, TokensDB
from HTTPlayground.settings import ACCESSORY_URL_PREFIX, TEMPLATE_ENV, SALT



def not_found(request):
    send_headers(request, response_code=404, content_type='text/html')
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    rendered_html = file.render(title='Not found', link=f'{ACCESSORY_URL_PREFIX}/form',
                                text='404 error. Page not found!')
    return rendered_html


@require_http_methods(['GET'], not_found)
def login(request):
    cookie_header = {'Set-Cookie': CookieHandler.generate_cookie(request, name='auth', value='True')}
    send_headers(request, content_type='text/html', **cookie_header)
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    rendered_html = file.render(title='Login', link=f'{ACCESSORY_URL_PREFIX}/form', text='Successful login.')
    return rendered_html


@require_http_methods(['GET'], not_found)
def logout(request):
    cookie_header = {'Set-Cookie': CookieHandler.generate_cookie_for_remove(request, name='auth')}
    send_headers(request, content_type='text/html', **cookie_header)
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    rendered_html = file.render(title='Logout', link=f'{ACCESSORY_URL_PREFIX}/form', text='Successful logout.')
    return rendered_html


@require_http_methods(['GET'], not_found)
def get_form(request):
    send_headers(request, content_type='text/html')
    secret_token = hash(f'{hash(CookieHandler.generate_cookie(request, name="auth", value="True"))}{hash(SALT)}')
    TokensDB.add_token(secret_token)
    form_text = {'title': ('form', 'form'),
                 'form_link': (f'{ACCESSORY_URL_PREFIX}/charge', f'{ACCESSORY_URL_PREFIX}/charge'),
                 'auth_link': (f'{ACCESSORY_URL_PREFIX}/authh/login', f'{ACCESSORY_URL_PREFIX}/authh/logout'),
                 'auth_text': ('Login', 'Logout'),
                 'secret_token': (secret_token, secret_token)}
    is_authenticated = CookieHandler.has_cookie(request, name='auth', value='True')
    file = TEMPLATE_ENV.get_template('form.html')
    rendered_html = file.render(**{k: v[is_authenticated] for k, v in form_text.items()})
    return rendered_html


@require_http_methods(['POST'], not_found)
def process_form(request):
    send_headers(request, content_type='text/html')
    file = TEMPLATE_ENV.get_template('base_response_form.html')
    if not CookieHandler.has_cookie(request, name='auth', value='True'):
        return file.render(title='Error', link=f'{ACCESSORY_URL_PREFIX}/form', text='Not authorized!')
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
    rendered_html = file.render(title='Charged', link=f'{ACCESSORY_URL_PREFIX}/form', text=form_text)
    return rendered_html
