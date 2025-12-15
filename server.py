from socket import *

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Connected:", addr)

    while True:
        sentence = connectionSocket.recv(1024)
        if not sentence:
            break

        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence)

        if capitalizedSentence == b"EXIT":
            break

    connectionSocket.close()
    print("Connection closed:", addr)
    
    