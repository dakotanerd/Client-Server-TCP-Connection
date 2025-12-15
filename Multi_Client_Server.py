from socket import *
import threading

SERVER_PORT = 12001

def handle_client(connectionSocket, addr):
    print(f"[+] Connected from {addr}")

    try:
        while True:
            data = connectionSocket.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            response = message.upper()
            connectionSocket.send(response.encode())

            if response == "EXIT":
                break

    except ConnectionResetError:
        print(f"[-] Connection reset by {addr}")

    finally:
        connectionSocket.close()
        print(f"[-] Disconnected from {addr}")


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', SERVER_PORT))
    serverSocket.listen(5)

    print(f"[+] Multi-client server listening on port {SERVER_PORT}")

    while True:
        connectionSocket, addr = serverSocket.accept()

        client_thread = threading.Thread(
            target=handle_client,
            args=(connectionSocket, addr),
            daemon=True
        )
        client_thread.start()


if __name__ == "__main__":
    main()
