from socket import *
import threading

SERVER_PORT = 12001
clients = {}  # username -> socket
clients_lock = threading.Lock()

def broadcast(message):
    """Send a message to all clients."""
    with clients_lock:
        for client in clients.values():
            try:
                client.send(message.encode())
            except:
                pass  # ignore failures

def send_private(message, recipient_username, sender_username):
    """Send a private message to a specific client."""
    with clients_lock:
        recipient_socket = clients.get(recipient_username)
        if recipient_socket:
            try:
                recipient_socket.send(f"[Private] {sender_username}: {message}".encode())
            except:
                clients.pop(recipient_username, None)
        else:
            sender_socket = clients.get(sender_username)
            if sender_socket:
                sender_socket.send(f"User '{recipient_username}' not found.".encode())

def list_users(sender_socket):
    """Send the list of online users to the requesting client."""
    with clients_lock:
        if clients:
            user_list = ", ".join(clients.keys())
            sender_socket.send(f"Online users: {user_list}".encode())
        else:
            sender_socket.send("No other users online.".encode())

def handle_client(connectionSocket, addr):
    username = None
    try:
        connectionSocket.send("Enter a username: ".encode())
        while True:
            username_candidate = connectionSocket.recv(1024).decode().strip()
            if not username_candidate:
                connectionSocket.send("Username cannot be empty. Try again: ".encode())
                continue
            with clients_lock:
                if username_candidate in clients:
                    connectionSocket.send("Username already taken. Try another: ".encode())
                else:
                    username = username_candidate
                    clients[username] = connectionSocket
                    break

        # Broadcast join message to all, including new user
        broadcast(f"{username} has joined the chat.")

        # Send welcome message to new user
        connectionSocket.send(
            f"Welcome {username}! Type EXIT to quit.\n"
            f"Private messages: @username message\n"
            f"Commands: /list (online users), /help (show commands)"
            .encode()
        )

        while True:
            data = connectionSocket.recv(1024)
            if not data:
                break
            message = data.decode().strip()
            if not message:
                continue

            # Exit
            if message.upper() == "EXIT":
                connectionSocket.send("EXIT".encode())
                broadcast(f"{username} has left the chat.")
                break

            # Commands
            if message.startswith("/"):
                if message.lower() == "/list":
                    list_users(connectionSocket)
                elif message.lower() == "/help":
                    connectionSocket.send(
                        "Available commands:\n"
                        "/list - show online users\n"
                        "/help - show this help\n"
                        "@username message - send private message\n"
                        "EXIT - leave chat".encode()
                    )
                else:
                    connectionSocket.send("Unknown command. Type /help for commands.".encode())
                continue

            # Private message
            if message.startswith("@"):
                if " " in message:
                    target_username, private_msg = message[1:].split(" ", 1)
                    send_private(private_msg, target_username, username)
                else:
                    connectionSocket.send("Invalid private message. Use: @username message".encode())
            else:
                # Broadcast
                broadcast(f"{username}: {message}")

    except ConnectionResetError:
        print(f"[-] Connection reset by {addr}")
        if username:
            broadcast(f"{username} has left unexpectedly.")
    finally:
        with clients_lock:
            if username in clients:
                clients.pop(username)
        connectionSocket.close()
        print(f"[-] Disconnected {username if username else addr}")

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', SERVER_PORT))
    serverSocket.listen(5)
    print(f"[+] Chat server running on port {SERVER_PORT}")

    while True:
        connectionSocket, addr = serverSocket.accept()
        threading.Thread(target=handle_client, args=(connectionSocket, addr), daemon=True).start()

if __name__ == "__main__":
    main()
