import os
import socket
import threading
import ftplib
import tkinter as tk
import hashlib
from time import time 
from tkinter import *
from tkinter import filedialog
# IP =  "192.168.1.101" #"localhost"
IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "server_data"
### to handle the clients
def handle_client (conn,addr):

    print(f"[NEW CONNECTION] {addr} connected.")
    
    #double array for each file date time 
    #fileTable = {'Filename'}
    uploadTable ={}
   
    HashTable = {'19parsonsj': 'Potus123'}
    conn.send(str.encode('ENTER USERNAME : ')) # Request Username
    name = conn.recv(2048)
    conn.send(str.encode('ENTER PASSWORD : ')) # Request Password
    password = conn.recv(2048)
    password = password.decode()
    name = name.decode()
    if(HashTable[name] == password):
        conn.send(str.encode('Connection Successful')) # Response Code for Connected Client 
        print('Connected : ',name)
    else:
        conn.send(str.encode('Login Failed')) # Response code for login failed
        print('Connection denied : ',name)
    conn.send('OK@Welcome to the server\n'.encode(FORMAT))
    
    
    while True:
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        #if len(data) == 1:
        cmd = data[0]
       # else:
           # cmd = data[0]
           # msg = data[1]
        

        
        if cmd == "LOGOUT":
            break
        
        elif cmd == "TASK": 
            send_data = "OK@"
            send_data += "LOGOUT from the server.\n"
            send_data += "LIST: List all the files from the server.\n"
            send_data += "UPLOAD <path>: Upload a file to the server.\n"
            send_data += "DELETE <filename>: Delete a file from the server.\n"
            send_data += "LOGOUT: Disconnect from the server.\n"
            send_data += "TASK: List all the commands."
            conn.send(send_data.encode(FORMAT))
            
            
            #change to specify filename 
        elif cmd == "CREATE":
            send_data += "Creating file. \n"
            conn.send(send_data.encode(FORMAT))
        
            buff = ""
            with open(os.path.join(SERVER_PATH,fileName), 'w') as temp_file: ##### creating the file
                temp_file.write(buff)
            print("The file does not exist")
            
        
            #abs path
            print(f"{addr} disconnected")
            conn.close()
        
        elif cmd == "UPLOAD":
            #timer for stop time of sending files
            ms = str(time() * 1000)
            #open path and write in file send
            name, text = data[1], data[2]
            
            filepath = os.path.join(SERVER_PATH, name)
        
            with open(filepath, "w") as f:
                f.write(text)
            
            #tell client uploaded successfully
            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))
            print("sent data")
            #send back time for calculation
            send_data = ms
            conn.send(ms.encode(FORMAT))
            print("sent ms")
            
            #delete previous version of uploadSpeed if available
            data =  conn.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            filename = data[0]
            text = data[1]
            print(filename)
            print(text)
            
            send_data = "OK@"
            filepath = os.path.join(SERVER_PATH, filename)
          

            try:
                with open(filepath, "r+") as f:
                    f.truncate(0)
                    f.write(text)
                print("file opened")
            except IOError:
                print("File not accessible")
            finally:
                f.close()
                
            
                    

            #conn.send(send_data.encode(FORMAT))
            
            content_list = []
            with open(f"{filepath}", "r") as f:
                for line in f:
                    value = int(float(line.rstrip()))
                    content_list.append(value)
                
            data = np.array(content_list)
            
            #y_ticks = np.arange(0, 1500, 50)
            #plt.yticks(y_ticks)
            plt.plot(range(len(data)), data)
            plt.savefig('/Users/jasmineparsons/Desktop/serverrun/server_data/UPLOADRATE.png')
  
            #plt.show()
            send_data = "OK@RESUMING"
            
            conn.send(send_data.encode(FORMAT))
            
            
            
        elif cmd == "LIST":
            print("in list")
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
            name = data[1]
            filepath = os.path.join(SERVER_PATH, name)
           
            with open(f"{filepath}", "r") as f:
                text = f.read()
            
            send_data = f"{name}@{text}"
            conn.send(send_data.encode(FORMAT))
           
            send_data = "Download Complete"
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
