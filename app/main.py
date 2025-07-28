import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(1024).decode("utf-8")
    print(f"Received request:\n{request}")

    if request.startswith("GET /user-agent"):
        # Extract User-Agent header
        lines = request.split("\r\n")
        user_agent = ""
        for line in lines:
            if line.lower().startswith("user-agent:"):
                user_agent = line.split(":", 1)[1].strip()
                break
        response_body = user_agent
        response_headers = [
            "HTTP/1.1 200 OK",
            "Content-Type: text/plain",
            f"Content-Length: {len(response_body)}",
            "",
            response_body
        ]
        response = "\r\n".join(response_headers)

    elif request.startswith("GET / HTTP/1.1"):
        response = "HTTP/1.1 200 OK\r\n\r\n"

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()

def main():
    print("Starting HTTP server on http://localhost:4221")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 4221))
    server_socket.listen(5)

    while True:
        client_socket, address = server_socket.accept()
        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
