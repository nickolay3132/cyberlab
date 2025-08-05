from http.server import BaseHTTPRequestHandler, HTTPServer
import mistune

HOSTNAME = 'localhost'
PORT = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        real_path = self.path.split('?')[0]
        if real_path == '/' or real_path == '/index.html':
            real_path = '/index.md'

        real_path = '.' + real_path

        if real_path.endswith('.md'):
            markdown = None
            with open(real_path) as markdown_file:
                markdown = markdown_file.read()

            html_text = mistune.html(markdown)
            self.wfile.write(bytes(html_text, 'utf-8'))
        else:
            content = None
            with open(real_path) as file:
                content = file.read()
            self.wfile.write(bytes(content, 'utf-8'))


if __name__ == '__main__':
    web_server = HTTPServer((HOSTNAME, PORT), MyHandler)
    print("Server started on http://%s:%5s" % (HOSTNAME, PORT))

    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        print("Stopping server", end='... ')
        
    web_server.server_close()
    print("OK")

