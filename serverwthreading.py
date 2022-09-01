import socket
import threading
clients=[]
usernames=[]
host=''
port=10003
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)
user_conn_dict={}
print('Listening for connections....')

'''
Broadcast() registers the client's message and displays it on the chat interface
param announcement: message to be broadcasted
'''
def broadcast(announcement,conn):
    for client in clients:
        while client!=conn:
            client.send(announcement.encode('utf-8'))
            break

'''
Identifies the usernames involved in private messaging and triggers private_chat().
else receives a message and broadcasts it.
param message_received: message received from client
list username_message_list: splits the message to identify the username of the recipient and private message.
param user_message: private message
param user_id: username of the recipient
param username_sender: username of the sender
'''
def received_from_client(conn,username):
    while True:
        username_sender = [k for k, v in user_conn_dict.items() if v == conn]
        try:
            message_received = conn.recv(1024).decode('utf-8')
            if ':' in message_received:
                username_message_list = message_received.split(':')
                user_message = username_message_list[1]
                user_id = username_message_list[0]
                private_chat(user_id, user_message, username_sender)
            else:
                broadcast(f'{username}:{message_received}', conn)
        except Exception:
            print(f'{username_sender} has left the chat')
            broadcast(f'{username_sender} has left the chat',conn)
            clients.remove(conn)
            break
''' 
private_chat() sends the private message to the desired client
param:client_conn: obtains the client details of the recipient.
'''
def private_chat(user_id,user_message,username_sender):
    client_conn=user_conn_dict.get(user_id)
    client_conn.send(f'[Private Message from {username_sender}]:{user_message}'.encode('utf-8'))

''' 
client_usernames() receives the username from the client and confirms connectivity.
param username: username of the client.
list usernames: contains all usernames of clients joining the chat.
dict user_conn_dict: holds the usernames as keys and client details as values.
'''
def client_usernames(conn,addr):
    conn.send('Enter your Username '.encode('utf-8'))
    username = conn.recv(1024).decode('utf-8')
    print(f'{username} has joined the chat')
    usernames.append(username)
    user_conn_dict[username]=conn
    broadcast(f'{username} has entered the chat!', conn)
    conn.send('You are now connected'.encode('utf-8'))

    received_from_client(conn, username)

''' 
client_connects() accepts connection from the client.
triggers client_usernames() after starting a thread for each new client.
param conn: client details
param addr: client host and port
'''
def client_connects():
    while True:
        try:
            conn,addr=server.accept()
            print(f'connection has been established with {str(addr[0])}')
            clients.append(conn)
            client_connection_thread = threading.Thread(target=client_usernames, args=(conn,addr), daemon=True)
            client_connection_thread.start()
            print(f'Active Connections: {threading.activeCount() - 1}')
        except Exception as ex:
            print(ex)
            break


client_connects()

