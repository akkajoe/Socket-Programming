import socket
import threading
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 10003
c.connect(('127.0.0.1', port))
'''
client_receive() saves the username and sends it to the server.
else prints the message recieved from the client/server.
triggers client_send() method.
param message: message received from other client/server.
param username: username of the client.
'''
def client_receive():
    while True:
        try:
            message = c.recv(1024).decode('utf-8')
            if message == 'Enter your Username ':
                print(message)
                username = input()
                c.send(username.encode('utf-8'))
                send_thread = threading.Thread(target=client_send)
                send_thread.start()

            else:
                print(message)
        except Exception:
            break
'''
client_send() closes the connection for the client on 'exit' input.
else client sends messages to server.
param user_message: message input from client.
'''
def client_send():
    while True:
        try:
            user_message= input()
            if user_message=='exit':
                print('exiting......')
                c.close()
            else:
                c.send(user_message.encode('utf-8'))
        except Exception:
            print('You are disconnected from the chat')
            break



receive_thread = threading.Thread(target=client_receive)
receive_thread.start()
