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
    
     #authentication request from server
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
        
         #command for task
        if cmd == "TASK":
            client.send(cmd.encode(FORMAT))
            
        #command for logout    
        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break
        #command for create
        elif cmd == "CREATE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            
            
        #> UPLOAD using filepath in command lines
        elif cmd == "UPLOAD":
            #path = given filepath
            path1 = data[1]
            
           #open and read text 
            with open(f"{path1}", "r") as f:
                text = f.read()
            
            #cmd, filename to upload, and all of its text
            filename = path1.split("/")[-1]
            send_data = f"{cmd}@{filename}@{text}"
            
            #start timer for speed calculation
            start = float(time()*1000)
            
            #turn send_data into bytes
            buff = bytes(send_data.encode(FORMAT))
            num_bytes = (os.path.getsize(path1))
            
            #send info to server to upload file
            client.send(buff)
            
            #recieve response about status
            client.recv(SIZE).decode(FORMAT)
            #print("uploaded")
            
            #recieve time value when upload was called 
            data = client.recv(SIZE)
           # print("recv data")
           
            #decode from byte
            s_ms = data.decode('utf8')
            stop = float(s_ms)
            
            #calculation for time passed
            u_time = (stop-start)
            #print(u_time)
            
            #upload speed rate
            rate = (int(num_bytes/u_time) / 100000 * 1000)
            #print(rate)
            #add new rate to uploadSpeed.txt
            name = "uploadSpeed.txt"
        
            filepath = os.path.join(CLIENT_PATH, name)
            #open file and add new value
            with open(f"{filepath}", "a") as f:
                add = str(rate) + '\n'
                f.write(add)
        
            
            f.close()
            
            #making the plot
            content_list = []
            #open uploadSpeed and turn each line into an int and append to list
            with open(f"{filepath}", "r") as f:
                for line in f:
                    value = int(float(line.rstrip()))
                    content_list.append(value)
                    
            #convert list into readble for plot 
            data = np.array(content_list)
            f.close()
            
           #plot data
            plt.plot(range(len(data)), data)
            plt.savefig('/Users/jasmineparsons/Desktop/serverrun/client_data/UPLOADRATE.png')
            
            #delete previous version and upload new version of uploadSpeed.txt
            filename = 'uploadSpeed.txt'
            with open(f"{filepath}", "r") as f:
                text = f.read()
            
            #upload new version of uploadSpeed.txt
            send_data = f"{filename}@{text}"
            buff = bytes(send_data.encode(FORMAT))
            num_bytes = len(buff)
            client.send(buff)
        
        #command for list
        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))
            
            
        #command for delete
        elif cmd == "DELETE":
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))
            
            
        #command for download 
        elif cmd == "DOWNLOAD":
            #start timer
            ms = str(time() * 1000)
            filename = data[1]
            
            #send file info to download
            send_data = f"{cmd}@{filename}"
            client.send(send_data.encode(FORMAT))
            
            #recieve file info
            data =  client.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            filename = data[0]
            path = '/Users/jasmineparsons/Desktop/serverrun/client_data'
            text = data[1]
            
            filepath = os.path.join(path, filename)
        
        #write info to file 
            with open(filepath, "w") as f:
                f.write(text)
            f.close()
            #print("Download Complete.")
            
            #send time
            send_data = ms
            client.send(ms.encode(FORMAT))
            
            #receive new downloadSpeed.txt from server 
            data =  client.recv(SIZE).decode(FORMAT)
            data = data.split("@")
            filename = data[0]
            text = data[1]
            #print(filename)
            #print(text)
            
            
            filepath = os.path.join(CLIENT_PATH, filename)
          
            #rewrite new values for downloadSpeed
            try:
                with open(filepath, "r+") as f:
                    f.truncate(0)
                    f.write(text)
                #print("file opened")
            except IOError:
                #print("File not accessible")
            finally:
                f.close()
            
            #convert lines in file to read to a plot
            content_list = []
            with open(f"{filepath}", "r") as f:
                for line in f:
                    value = int(float(line.rstrip()))
                    content_list.append(value)
                
            data = np.array(content_list)
            f.close()
    
            #plot data
            plt.clf()
            plt.plot(range(len(data)), data)
            plt.savefig('/Users/jasmineparsons/Desktop/serverrun/client_data/DOWNLOADRATE.png')
  
            #plt.show()
            
            

            
            
            
                    
            
        

    print("Disconnected from the server.")
    client.close() ## close the connection

if __name__ == "__main__":
    main()
