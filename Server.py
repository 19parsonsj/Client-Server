import os
import socket
import threading
import ftplib
import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import filedialog
# IP =  "192.168.1.101" #"localhost"
IP = "localhost"
#IP = Dns.GetHostEntry(Dns.GetHostName()).AddressList[0]
#IP = "10.31.185.131"
#Automatically retrieves IPAddress.

PORT = 4451
ADDR = (IP,PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_PATH = "D:\Austin\School\CS371\Project\ServerFile"
SETTINGS_PATH = "D:\Austin\School\CS371\Project\ServerFile\Settings.txt"
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
            
            
            
        elif cmd == "CREATE":
            send_data += "Creating file. \n"
            conn.send(send_data.encode(FORMAT))
            path = '/Users/jasmineparsons'
            fileName = 'Simple-text-file.txt'
            buff = "ABCD \n"
            with open(os.path.join(path,fileName), 'w') as temp_file: ##### creating the file
                temp_file.write(buff)
            print("The file does not exist")
            
            
            
            print(f"{addr} disconnected")
            conn.close()
        
        elif cmd == "UPLOAD":
            #add gui to choose 
            name, text = data[1], data[2]
            
            filepath = os.path.join(SERVER_PATH, name)
        
            with open(filepath, "w") as f:
                f.write(text)
            
            #os.close(f.fileno())
            
            #Get file size of file (in bytes)
            file_size = os.path.getsize(filepath)
            file_size = str(file_size)
            
            #Get date and time
            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y_%H:%M:%S ")
            
            #Now edit Settings.txt and add in this new file
            with open(SETTINGS_PATH, "a") as f:
                #Each file has the following format:
                # <filename> xxxx_bytes date_time <number of downloads>
                f.write(name + " " + file_size + "_bytes " + date_time + "0\n")

            send_data = "OK@File uploaded successfully."
            
            conn.send(send_data.encode(FORMAT))
            #os.close(f.fileno())
            
            
            
        elif cmd == "LIST":
            files = os.listdir(SERVER_PATH)
            send_data = "OK@"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
                
            conn.send(send_data.encode(FORMAT))
            
            
            
            
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
            
            
            
            
            
        elif cmd == "DOWNLOAD":
            path1 = data[1]
            
            filename = path1.split("/")[-1]
            
            #Edit settings and increment number of downloads for filename
            #First search Settings.txt for a matching filename
            settings = open(SETTINGS_PATH, "r")
            
            i = 0
            foundLine = 0
            
            for line in settings:
                i += 1
                if filename in line:
                    foundLine = 1
                    break
                
            #If we found the line, edit it and increment the downloads by 1.
            if foundLine == 1:
                data = settings.readlines()
                newLine = data[i].split()
                #Number of downloads will always be the fifth "word" on every line
                numDown = newLine[4]
                numDown = int(numDown)
                numDown += 1
                numDown = str(numDown)
                newLine[4] = numDown
                
            #Close the file
            settings.close()
            
            #Write the new line back into the file
            with open(SETTINGS_PATH, "w") as f:
                f.writelines(data)
                
           
            with open(f"{path1}", "r") as f:
                text = f.read()
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