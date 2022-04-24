import os
import socket
from time import sleep
from time import time
import json
import matplotlib.pyplot as plt

IP = "localhost"
PORT = 4450
ADDR = (IP,PORT)
SIZE = 1024 ## byte .. buffer size
FORMAT = "utf-8"
CLIENT_PATH = "client_data"

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
        
        cmd, msg = data.split("@")
  
        
        
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
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            
            
        #> UPLOAD /Users/jasmineparsons/filename
        elif cmd == "UPLOAD":
            
            
            path1 = data[1]
           
            with open(f"{path1}", "r") as f:
                text = f.read()
            filename = path1.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            start = float(time() * 1000)
            
            buff = bytes(send_data.encode(FORMAT))
            num_bytes = len(buff)
            client.send(buff)
            client.recv(SIZE).decode(FORMAT)
            print("uploaded")
            data = client.recv(SIZE)
            print("recv data")
            s_ms = data.decode('utf8')
       
            stop = float(s_ms)
          
            u_time = stop-start
            print(u_time)
            rate = float(num_bytes/u_time)
            print(rate)

            name = "uploadSpeed.txt"
            filepath = os.path.join(CLIENT_PATH, name)
            
            with open(f"{filepath}", "a") as f:
                add = str(rate) + '\n'
                f.write(add)
        
              
            f.close()
            with open(f"{filepath}", "r") as f:
                content_list = [line.rstrip() for line in f]
                data = tuple(content_list)
            
            plt.plot(range(len(data)), data)
            plt.show()
        
            
            

            
        
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
            path = '/Users/jasmineparsons/Desktop/serverrun/client_data'
            text = data[1]
            
            filepath = os.path.join(path, filename)
        
            with open(filepath, "w") as f:
                f.write(text)
            f.close()
            print("Download Complete.")
            
            
           
     
      
            
            

            
            
            
                    
            
        

    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
