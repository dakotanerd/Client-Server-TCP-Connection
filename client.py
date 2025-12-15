from socket import *

serverName = '127.0.0.1'
serverPort = 12001

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    sentence = input('Input lowercase sentence (type EXIT to quit): ')
    clientSocket.send(sentence.encode())

    modifiedSentence = clientSocket.recv(1024).decode('utf-8')
    print('From Server:', modifiedSentence)

    if sentence.upper() == "EXIT":
        print("Closing connection.")
        break

clientSocket.close()
