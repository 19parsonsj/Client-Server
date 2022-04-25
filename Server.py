import os
import socket
import threading
import ftplib
import tkinter as tk
import hashlib
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
    #ask client for user and password
    #collection list of username and passwords
    HashTable = {'19parsonsj': 'Potus123'}
    conn.send(str.encode('ENTER USERNAME : ')) # Request Username
    name = conn.recv(2048)
    conn.send(str.encode('ENTER PASSWORD : ')) # Request Password
    password = conn.recv(2048)
    password = password.decode()
    name = name.decode()
    
    #check if user and pass are in the collection
    if(HashTable[name] == password):
        #connect if user and pass 
        conn.send(str.encode('Connection Successful')) # Response Code for Connected Client 
        print('Connected : ',name)
    else:
        #deny connection if user and pass does not exist
        conn.send(str.encode('Login Failed')) # Response code for login failed
        print('Connection denied : ',name)
        
        
    conn.send("OK@Welcome to the server".encode(FORMAT))
    
    #while loop for command line
    while True:
        data =  conn.recv(SIZE).decode(FORMAT)
        data = data.split("@")
        cmd = data[0]
       
        send_data = "OK@"
        
        #logout command breaks while loop and closes connection
        if cmd == "LOGOUT":
            break
            
        #lists possible commands 
        elif cmd == "TASK": 
            send_data = "OK@"
            send_data += "LOGOUT from the server.\n"
            send_data += "LIST: List all the files from the server.\n"
            send_data += "UPLOAD <path>: Upload a file to the server.\n"
            send_data += "DELETE <filename>: Delete a file from the server.\n"
            send_data += "LOGOUT: Disconnect from the server.\n"
            send_data += "TASK: List all the commands."
            conn.send(send_data.encode(FORMAT))
            
        #create command handling
        elif cmd == "CREATE":
            send_data += "Creating file. \n"
            conn.send(send_data.encode(FORMAT))
            path = '/Users/jasmineparsons'
            fileName = 'Simple-text-file.txt'
            buff = "ABCD \n"
            with open(os.path.join(path,fileName), 'w') as temp_file: ##### creating the file
                temp_file.write(buff)
            print("The file does not exist")
            
            
            
        elif cmd == "UPLOAD":
            ######START OF JASMINE'S CODE######
            name, text = data[1], data[2]
            
            filepath = os.path.join(SERVER_PATH, name)
        
            with open(filepath, "w") as f:
                f.write(text)
                
            #tell client uploaded successfully
            send_data = "OK@File uploaded successfully."
            conn.send(send_data.encode(FORMAT))
            #print("sent data")
            
            #send back time for calculation
            send_data = ms
            conn.send(ms.encode(FORMAT))
            #print("sent ms")
            
            #delete previous version of uploadSpeed if available
            data =  conn.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            filename = data[0]
            text = data[1]
            #print(filename)
            #print(text)
            
            #rewrite new values to uploadSpeed
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
                
            #convert lines in uploadSpeed to read to a plot
            content_list = []
            with open(f"{filepath}", "r") as f:
                for line in f:
                    value = int(float(line.rstrip()))
                    content_list.append(value)
                
            data = np.array(content_list)
            
            #plot the uploadSpeed data
            plt.plot(range(len(data)), data)
            plt.savefig('/Users/jasmineparsons/Desktop/serverrun/server_data/UPLOADRATE.png')
            #plt.show()
            ######END OF JASMINE'S CODE######
            
            ######START OF AUSTIN'S CODE######
            
            #Get file size of file (in bytes)
            filepath = os.path.join(SERVER_PATH, name)
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
                
            #######END OF AUSTIN's CODE########

            send_data = "OK@File uploaded successfully."
            
            conn.send(send_data.encode(FORMAT))
            #os.close(f.fileno())
            
            
            
            
            ### ENTIRE LIST COMMAND IS BY AUSTIN ###
            
        elif cmd == "LIST":
            #files = os.listdir(SERVER_PATH)
            send_data = "OK@"

            with open(SETTINGS_PATH, "r") as settings:
                settingsData = settings.readlines()
                
            if len(settingsData) == 0:
                send_data += "The server directory is empty"
            else:
                for i in range(len(settingsData)):
                    send_data += settingsData[i]    
                conn.send(send_data.encode(FORMAT))
            
            ### END OF LIST COMMAND ###
            
            
        # Delete both the file and its entry into settings.txt
        elif cmd == "DELETE":
            files = os.listdir(SERVER_PATH)
            send_data = "OK@"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                # If you can find the file to delete, start the deletion process
                if filename in files:
                    #Delete the file
                    os.system(f"del {SERVER_PATH}\{filename}")
                    send_data += "File deleted successfully."
                    
                    ### START OF AUSTIN'S CODE ##
                    
                    # Delete the entry in settings
                    with open(SETTINGS_PATH, "r") as settings:
                        # Read all lines in settings.txt, and if the corresponding file to
                        # delete is found, delete that line only
                        settingsData = settings.readlines()
                        for i in range(len(settingsData)):
                            #print(settingsData[i])
                            if filename in settingsData[i]:
                                break
                        #Delete only the ith line
                        settingsData.pop(i)
                    
                    # After popping the element from the list, remake the
                    # text file.
                    try:
                        with open(SETTINGS_PATH, "r+") as f:
                            f.truncate(0)
                            # Write in each of the remaining elements of the list
                            for i in range(len(settingsData)):
                                f.write(settingsData[i])
                                #print(settingsData[i])
                        print("file opened")
                    except IOError:
                        print("File not accessible")
                    finally:
                        f.close()

                    ### END OF AUSTIN's CODE                    

                else:
                    send_data += "File not found."

            conn.send(send_data.encode(FORMAT))
            
            
            
            
            
        elif cmd == "DOWNLOAD":
            
            path1 = data[1]
            
            ### IMPORTANT: CHANGE THIS TO "/" FOR MAC ####
            filename = path1.split("\\")[-1]
            
            ### START OF AUSTIN'S CODE ###
            
            #Edit settings and increment number of downloads for filename
            #First search Settings.txt for a matching filename
            #settings = open(SETTINGS_PATH, "r")
            with open(SETTINGS_PATH, "r") as settings:
                settingsData = settings.readlines()
                
                #Find which line's download number to increment by comparing file names
                for i in range(len(settingsData)):
                    #print(settingsData[i])
                    if settingsData[i].startswith(filename):
                        #print("in if")
                        break
                #print(i)
                
                #If we found the line, edit it and increment the downloads by 1.
                newLine = settingsData[i].split(" ")
                #Number of downloads will always be the fourth "word" on every line
                # (which translates to 3 in an array)
                numDown = newLine[3]
                numDown = int(numDown)
                numDown += 1
                numDown = str(numDown)
                newLine[3] = numDown
                
                lineToWrite = ""
                
                # Concatenate all four "words" into one string to replace the
                # current line in the text file
                for j in range(4):
                    lineToWrite += str(newLine[j])
                    lineToWrite += " "
                
                #Add a newline and replace the previous line with our lineToWrite
                lineToWrite = lineToWrite + '\n'
                settingsData[i] = lineToWrite
            
            #Write the new line back into the file
            with open(SETTINGS_PATH, "w") as f:
                f.writelines(settingsData)
                
                ### END OF AUSTIN'S CODE ###
                
            ### START OF JASMINE'S CODE ###
           
            with open(f"{path1}", "r") as f:
                text = f.read()
                
            send_data = f"{filename}@{text}"
            #start timer for sending
            start = float(time() * 1000)
            buff = bytes(send_data.encode(FORMAT))
            #calculate number of bytes
            num_bytes = (os.path.getsize(filepath))
            #send data
            conn.send(buff)
           
            #receives stop time from client
            data = conn.recv(SIZE)
            #print("recv data")
            #decode
            s_ms = data.decode('utf8')
            stop = float(s_ms)
            #difference in time
            u_time = abs(stop-start)
            #print(u_time)
            
            #calculate the rate MB/s
            rate = (int(num_bytes/u_time) / 100000 * 1000)
           
            #open downloadSpeed.txt and add new rate
            name = "downloadSpeed.txt"
        
            filepath = os.path.join(SERVER_PATH, name)
            
            with open(f"{filepath}", "a") as f:
                add = str(rate) + '\n'
                f.write(add)
        
              
            f.close()
            
            #convert lines in file to read to a plot
            content_list = []
            with open(f"{filepath}", "r") as f:
                for line in f:
                    value = int(float(line.rstrip()))
                    content_list.append(value)
                
            data = np.array(content_list)
            
            #plot the data
            plt.clf()
            plt.plot(range(len(data)), data)
            plt.savefig('/Users/jasmineparsons/Desktop/serverrun/server_data/DOWNLOADRATE.png')
            
            
            #delete previous version and upload new version of downloadSpeed.txt
            filename = 'downloadSpeed.txt'
            
            with open(f"{filepath}", "r") as f:
                text = f.read()
            
            #send new downloadSpeed.txt to client
            send_data = f"{filename}@{text}"
            buff = bytes(send_data.encode(FORMAT))
            num_bytes = len(buff)
            conn.send(buff)
            #plt.show()
            #status for upload of uploadSpeed.txt
            #client.recv(SIZE).decode(FORMAT)
            send_data = "OK@RESUMING"
            
            conn.send(send_data.encode(FORMAT))
            ### END OF JASMINE'S CODE ###
            
            
            
     
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
