import os
import socket
import threading
import ftplib
import tkinter as tk
from tkinter import *
from tkinter import filedialog
# IP =  "192.168.1.101" #"localhost"
IP = "localhost"
PORT = 4451
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server"
### to handle the clients
def handle_client (conn,addr):

    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the server".encode(FORMAT))
    #double array for each file date time 
    
    while True:
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
       
        send_data = "OK@"
        if cmd == "LOGOUT":
            break
        elif cmd == "TASK": 
            send_data += "LOGOUT from the server.\n"
            conn.send(send_data.encode(FORMAT))
            
            
            #change to specify filename 
        elif cmd == "CREATE":
            send_data += "Creating file. \n"
            conn.send(send_data.encode(FORMAT))
            path = '/Users/jasmineparsons'
            fileName = 'Simple-text-file.txt'
            buff = "ABCD \n"
            with open(os.path.join(path,fileName), 'w') as temp_file: ##### creating the file
                temp_file.write(buff)
            print("The file does not exist")
            
            
            #abs path
            print(f"{addr} disconnected")
            conn.close()
        
        elif cmd == "UPLOAD":
            #add gui to choose 
            name, text = data[1], data[2]
            
            filepath = os.path.join(SERVER_PATH, name)
        
            with open(filepath, "w") as f:
                f.write(text)

            send_data = "OK@File uploaded successfully."
            
            conn.send(send_data.encode(FORMAT))
            os.close(f.fileno())
            
            
            
        elif cmd == "LIST":
            files = os.listdir(SERVER_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
                
            conn.send(send_data.encode(FORMAT))
            
            
            
            #change to not need absolute path 
        elif cmd == "DELETE":
            files = os.listdir(SERVER_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.system(f"rm {SERVER_PATH}/{filename}")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))
            
            
            
            
            #
        elif cmd == "DOWNLOAD":
            path1 = data[1]
           
            with open(f"{path1}", "r") as f:
                text = f.read()
            filename = path1.split("/")[-1]
            send_data = f"{filename}@{text}"
            conn.send(send_data.encode(FORMAT))
            
                
            
            
            
            
     
    print(f"{addr} disconnected")
    conn.close()
        
def main():
    print("Starting the server")
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) ## used IPV4 and TCP connection
    server.bind(ADDR) # bind the address
    server.listen() ## start listening
    print(f"server is listening on {IP}: {PORT}")
    while True:
        conn, addr = server.accept() ### accept a connection from a client
        thread = threading.Thread(target = handle_client, args = (conn, addr)) ## assigning a thread for each client
        thread.start()

if __name__ == "__main__":
    main()
