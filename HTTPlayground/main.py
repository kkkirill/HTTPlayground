from http.server import HTTPServer, BaseHTTPRequestHandler
from HTTPlayground.views import not_found
from HTTPlayground.urls import urls
from HTTPlayground.settings import URL, PORT
from HTTPlayground.base import process_static


class SimpleRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        body_content = f'{urls.get(self.path, process_static)(self) or not_found(self)}'
        self.wfile.write(body_content.encode('utf-8'))

    def do_POST(self):
        body_content = f'{urls.get(self.path, process_static)(self) or not_found(self)}'
        self.wfile.write(body_content.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, url=URL, port=PORT):
    try:
        handler = server_class((url, port), handler_class)
        handler.serve_forever()
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        handler.socket.close()


if __name__ == '__main__':
    run(handler_class=SimpleRequestHandler)