from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import argparse

class CustomHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith("/files/"):
            filename = self.path[len("/files/"):]
            content_length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(content_length)

            try:
                filepath = os.path.join(self.server.directory, filename)
                with open(filepath, "wb") as f:
                    f.write(data)

                self.send_response(201)
                self.end_headers()
            except Exception as e:
                print("Error:", e)
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return  # Disable default logging

def run(directory, port=4221):
    handler = CustomHandler
    server = HTTPServer(("", port), handler)
    server.directory = directory
    print(f"Server running at http://localhost:{port}/")
    server.serve_forever()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    args = parser.parse_args()

    run(directory=args.directory)
