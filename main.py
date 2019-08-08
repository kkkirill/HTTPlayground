from sys import argv
from http.server import HTTPServer, BaseHTTPRequestHandler
from tools.file_reader import FileReader
from views import not_found
from urls import urls
from settings import URL, PORT


class SimpleRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/favicon.ico':
            return
        elif self.path.endswith(('.css', '.js')):
            filename = self.path.rsplit('/', 1)[-1]
            self.wfile.write(FileReader.read(filename, mode='b'))
        else:
            body_content = f'{urls.get(self.path, not_found)(self)}'
            self.wfile.write(body_content.encode('utf-8'))

    def do_POST(self):
        print(self.headers)
        body_content = f'{urls.get(self.path, not_found)(self)}'
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
    if len(argv) == 3:
        run(handler_class=SimpleRequestHandler, url=argv[1], port=int(argv[2]))
    else:
        run(handler_class=SimpleRequestHandler)
