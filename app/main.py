import socket
import threading
import os
import sys

# Parse --directory argument
directory = "."
if "--directory" in sys.argv:
    idx = sys.argv.index("--directory")
    if idx + 1 < len(sys.argv):
        directory = sys.argv[idx + 1]

HOST = 'localhost'
PORT = 4221

def handle_client(conn):
    try:
        request = conn.recv(1024).decode()
        lines = request.splitlines()
        if not lines:
            return

        method, path, _ = lines[0].split()

        # Only GET method supported
        if method != "GET":
            conn.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            return

        if path.startswith("/files/"):
            filename = path[len("/files/"):]
            filepath = os.path.join(directory, filename)

            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    content = f.read()
                headers = [
                    "HTTP/1.1 200 OK",
                    "Content-Type: application/octet-stream",
                    f"Content-Length: {len(content)}",
                    "",
                    ""
                ]
                response = "\r\n".join(headers).encode() + content
                conn.sendall(response)
            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

        else:
            # Default root handler
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    finally:
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, _ = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn,))
            thread.start()

if __name__ == "__main__":
    start_server()
