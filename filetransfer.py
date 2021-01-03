import socket
import os

class Filetransfer:
    def __init__(self,host = socket.gethostbyname(socket.gethostname()),port = 5000, sok = socket.socket(), server = True):
        self.host = host
        self.port = port
        self.sok = sok
        ''' defining host, port no, and creating socket for this class'''
        if server == False:
            self.client()
        else:
            self.server()
            ''' if server is not true, then client function will run'''

    def server(self):
        ''' server program portion '''
        print("Server is on | Host ",self.host,' | Port ',self.port) #printing the server host ip and port number
        self.sok.bind((self.host,self.port))
        self.sok.listen(10)
        print("Server listening...")

        option = ['help', 'file', 'download', 'dl'] #defining options
        conn,addr = self.sok.accept()
        print('Connected to client',addr)

        while True:
            ''' Communication '''
            r = conn.recv(1024).decode() #rx, receiving buffer size is 1024
            print('Client :', r)

            if r in option:
                if r == 'help':
                    msg = str(option).encode()
                    conn.send(msg)

                elif r == 'file':
                    top = str(os.getcwd()) + '\\store' # current working directory path
                    file_name = ''
                    for root, dirs, files in os.walk(top):
                        file_name = str(files).encode()
                    conn.send(file_name)
                elif r == 'download' or 'dl':
                    ''' Download operation'''
                    buffer = 0 # buffer size variable
                    msg = str('dl_ack').encode() #download ack
                    conn.send(msg) #tx
                    r = conn.recv(1024).decode() #rx file name
                    path_variable = str(os.getcwd()) + '\\store' + '\\' + r
                    print(path_variable)
                    if os.path.exists(path_variable):
                        msg = str('OK').encode()
                        conn.send(msg) # tx 'OK'
                        r = conn.recv(1024).decode() #rx 'OK'
                        size = os.path.getsize(path_variable)
                        msg = str(size).encode()
                        conn.send(msg) # tx size of the file
                        r = conn.recv(1024).decode() # rx 'OK'
                        #file sending .....
                        file = open(path_variable, 'rb')
                        file_data = file.read(size)
                        conn.send(file_data) #tx

                    else:
                        msg = "File does not exist.".encode()
                        conn.send(msg) #tx error msg
                elif r == 'close':
                    conn.close()
                else:
                    print("Service currently unavailabe.")

            else:
                conn.send(str('Invalid command.').encode())

    def client(self):
        ''' Client program'''
        self.sok.connect((self.host,self.port))
        print("Client mode on. Client connected.")
        print("Please type 'help' to see available options.")
        print("Type 'file' to display the available files, 'dl' or 'download' to download a file.")
        while True:
            msg = input(str('Client : ')).encode()
            self.sok.send(msg) #tx option to server
            r = self.sok.recv(1024).decode() #rx

            if r == 'dl_ack':
                ''' Download operation'''
                print('Server : Please type the file name to download.')
                msg_file = input(str('Client : ')).encode() #taking file name as input
                self.sok.send(msg_file) # tx file name
                r = self.sok.recv(1024).decode() # rx 'OK'
                if r == 'OK':
                    msg = str('OK').encode()
                    self.sok.send(msg)  # tx 'OK'
                    r_size = int(self.sok.recv(1024).decode())  # rx
                    self.sok.send(msg)  # tx ok
                    # file receive
                    path_var = str(os.getcwd()) + '\\download' + '\\' + msg_file.decode()
                    file = open(path_var, 'wb')
                    file_data = self.sok.recv(r_size + 100)  # rx file , buffer size r_size+100
                    file.write(file_data)
                    file.close()
                    print('Server : File has been sent!')
                else:
                    pass
            else:
                print('Server : ',r)










