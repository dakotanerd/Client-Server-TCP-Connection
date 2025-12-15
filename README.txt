TCP Multi-Client Chat Application

Overview
This project implements a multi-client TCP chat application in Python.

- Clients can connect to the server with a unique username.
- Messages can be sent to all users (broadcast) or to specific users (private messages using @username message).
- Commands are supported:
  - /list – show online users
  - /help – show available commands
- The connection remains open until the client types EXIT.
- When a new client joins or leaves, all users are notified.

This project demonstrates multi-threaded TCP socket programming, username management, message broadcasting, and private messaging.

__________________________________________________________________________________________________

Files
chat_room.py - TCP server that listens for clients, handles usernames, broadcasts messages, and manages private messaging
client_chat.py - TCP client that connects to the server, sends messages, and receives broadcasts

__________________________________________________________________________________________________

How It Works

Server (chat_room.py)
- Listens on port 12001
- Accepts multiple client connections
- Prompts each client for a unique username
- Broadcasts join/leave notifications to all clients
- Receives messages in a loop:
  - Broadcasts normal messages to all clients
  - Sends private messages when @username message is used
  - Processes commands (/list and /help)
- Closes a connection when a client sends EXIT

Client (client_chat.py)
- Connects to the server at 127.0.0.1:12001
- Prompts the user to enter a unique username
- Receives broadcasts and private messages from the server in real time
- Sends messages typed by the user:
  - Normal messages → broadcast to all users
  - @username message → private message to a specific user
- Displays commands and messages clearly:
  - You: "message" for your broadcasts
  - You (private to Bob): "message" for private messages

__________________________________________________________________________________________________

How to Run

Step 1 – Start the Server
1. Open a terminal.
2. Run the server:

python chat_room.py

You should see:
[+] Chat server running on port 12001

Step 2 – Start the First Client
1. Open a second terminal.
2. Run the client:

python client_chat.py

3. Enter a unique username:

> Alice
Alice has joined the chat.
Welcome Alice! Type EXIT to quit.
Private messages: @username message
Commands: /list (online users), /help (show commands)
>

Step 3 – Start the Second Client
1. Open a third terminal.
2. Run the client again:

python client_chat.py

3. Enter a different username:

> Bob
Bob has joined the chat.
Welcome Bob! Type EXIT to quit.
Private messages: @username message
Commands: /list (online users), /help (show commands)

Alice sees the join notification:
Bob has joined the chat.

Step 4 – Chatting
- Broadcast message: type normally and press Enter

> Hello everyone
You: "Hello everyone"

- Private message: use @username message

> @Alice Hi Alice!
You (private to Alice): "Hi Alice!"

- Commands:

> /list
Online users: Alice, Bob

> /help
Available commands:
 /list - show online users
 /help - show this help
 @username message - send private message
 EXIT - leave chat

- Exit chat: type EXIT

> EXIT
You leave the chat and connection is closed.

Other clients will see:
Bob has left the chat.

__________________________________________________________________________________________________

Protocol Details
- Transport: TCP
- Message format: Raw UTF-8 text
- Persistent connections: connection remains open until EXIT is sent
- Message types: broadcast, private, command

__________________________________________________________________________________________________

Key Lessons Learned
- Multi-threaded server handles multiple clients simultaneously.
- Ensuring unique usernames prevents conflicts.
- Clean separation of broadcast vs private messages improves user experience.
- Real-time message handling requires careful input/output handling to avoid freezing.

__________________________________________________________________________________________________

Requirements
- Python 3.x
- Works on Windows, macOS, and Linux
- No external dependencies

__________________________________________________________________________________________________

Author
Dakota Wellerbrady
Advanced Networking – HW0
Python TCP Socket Programming Assignment
