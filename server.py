import socket
import threading
from time import sleep

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

HOST = ip_address
PORT = int(input('Enter port: '))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            #print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat\n".encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")

        client.send('NICK'.encode('utf-8'))
        try:
            nickname = client.recv(1024)
            if nickname not in nicknames:
                nicknames.append(nickname)
                clients.append(client)

                print(f"Nickname of the client is {nickname}")
                sleep(0.1)
                broadcast(f"{nickname} joined the chat\n".encode('utf-8'))
                #client.send("Connected to the server".encode('utf-8'))

                thread = threading.Thread(target=handle, args=(client,))
                thread.start()
            
            else:
                print("Nickname error(Nickname is already in use)")

        except:
            print("Nickname error(Incorrect nickname)")

print("Server running...")
print(f"Ip address - {ip_address}\nPort - {PORT}\nHostname - {hostname}")

receive()
