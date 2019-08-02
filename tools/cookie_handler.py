from http.cookies import SimpleCookie


class CookieHandler:
    @staticmethod
    def is_cookie(request, cookie_pair: dict):
        raw_cookies = request.headers.get('Cookie')
        cookies = SimpleCookie(raw_cookies)
        k, v = tuple(cookie_pair.items())[0]
        cookie = cookies.get(f'{k}')
        return getattr(cookie, 'value', None) == v

    @classmethod
    def set_cookie(cls, request, cookie_pair: dict):
        """Should use before end_headers!"""
        if cls.is_cookie(request, cookie_pair):
            return
        cookie = SimpleCookie(request.headers.get('Cookie'))
        k, v = tuple(cookie_pair.items())[0]
        cookie[f"{k}"] = v
        cookie[f"{k}"]['path'] = '/'
        cookie[f"{k}"]['httponly'] = True
        request.send_header('Set-Cookie', cookie.output(header='', sep=''))
