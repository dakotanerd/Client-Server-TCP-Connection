from socket import *
import threading
import sys

SERVER_NAME = '127.0.0.1'
SERVER_PORT = 12001

def receive_messages(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode()
            if not message:
                break
            if message == "EXIT":
                print("\n[Server closed the connection]")
                clientSocket.close()
                sys.exit()
            # Print incoming messages above input prompt
            print(f"\r{message}\n> ", end="", flush=True)
        except:
            break

def main():
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((SERVER_NAME, SERVER_PORT))

    threading.Thread(target=receive_messages, args=(clientSocket,), daemon=True).start()

    # Enter username first
    while True:
        username = input("> ").strip()
        if not username:
            continue
        clientSocket.send(username.encode())
        # Wait briefly for server to print welcome message via thread
        break

    # Main message loop
    try:
        while True:
            message = input("> ").strip()
            if not message:
                continue
            clientSocket.send(message.encode())
            # Show You: formatting
            if not message.startswith("/"):
                if message.startswith("@"):
                    target = message.split(" ", 1)[0][1:]
                    content = message.split(" ", 1)[1] if " " in message else ""
                    print(f'You (private to {target}): "{content}"')
                
            if message.upper() == "EXIT":
                break
    finally:
        clientSocket.close()

if __name__ == "__main__":
    main()
