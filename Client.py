import os
import socket
from time import sleep
from time import time
IP = "localhost"
PORT = 4451
ADDR = (IP,PORT)
SIZE = 1024 ## byte .. buffer size
FORMAT = "utf-8"
SERVER_DATA_PATH = "D:\Austin\School\CS371\Project\ClientFile"
def main():
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(ADDR)
    response = client.recv(2048)
    name = input(response.decode())
    client.send(str.encode(name))
    response = client.recv(2048)
    password = input(response.decode())
    client.send(str.encode(password))
    response = client.recv(2048)
    
    while True:  ### multiple communications
        data = client.recv(SIZE).decode(FORMAT)
        #cmd, msg = data.split("@")
        
        data = data.split("@")
        if len(data) == 1:
            cmd = data[0]
        else:
            cmd = data[0]
            msg = data[1]

        
        if cmd == "OK":
            print(f"{msg}")
        elif cmd == "DISCONNECTED":
            print(f"{msg}")
            break
        
        data = input("> ") 
        data = data.split(" ")
        cmd = data[0]
        
        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "CREATE":
            client.send(cmd.encode(FORMAT))
            
            
        #> UPLOAD /Users/jasmineparsons/filename
        elif cmd == "UPLOAD":
            
            path1 = data[1]
           
            with open(f"{path1}", "r") as f:
                text = f.read()
            filename = path1.split("\\")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            client.send(send_data.encode(FORMAT))
        
        elif cmd == "LIST":
            #redo format to add size, upload date and time, number of downloads
            client.send(cmd.encode(FORMAT))
            
            
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            
            
        elif cmd == "DOWNLOAD":
            filename = data[1]
            send_data = f"{cmd}@{filename}"
            client.send(send_data.encode(FORMAT))
            data =  client.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            filename = data[0]
            text = data[1]
            
            filepath = os.path.join(SERVER_DATA_PATH, filename)
        
            with open(filepath, "w") as f:
                f.write(text)
            f.close()
            data = input("> ") 
            data = data.split(" ")
            cmd = data[0]
            
            

            
            
            
                    
            
        

    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
