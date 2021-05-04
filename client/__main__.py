import socket
import threading
import queue
import sys
import random
import os
import time
#дописать recvfrom
try:
    def ReceiveData(sock, encoding, BufferSize):
        while True:
            try:
                data, addr = sock.recvfrom(BufferSize)
                data = data.decode(encoding)
                itsatime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
                print(
                    '[' + str(addr[0]) + ']' + '=' + '[' + str(addr[1]) + ']' + '=' + '[' + itsatime + ']' + '/' + data)
                # data,addr = sock.recvfrom(1024)
                # print(data.decode('utf-8'))
            except:
                pass


    def connect(serverIP, port):

        serverIP = input('Enter new serverIP: ')
        port = int(input('Enter new port: '))

        RunClient(serverIP, port)


    def rename(name):
        print('*' * 53)
        name = input("Enter new name: ")
        print('*' * 53)
        return name


    def RunClient(serverIP, port):
        BufferSize = 1024
        encoding = 'utf-8'
        host = socket.gethostbyname(socket.gethostname())
        # if not port:
        #     port = random.randint(6000,10000)
        # logger.info('Client IP->'+str(host)+' Port->'+str(port))

        print('Client Running')

        print('Client IP -> [' + str(host) + '] Port -> [' + str(port) + ']')

        server = (str(serverIP), 8000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        s.bind(server)
        s.setblocking(0)

        join = False

        name = input('Please write your name here: ')
        if name == '':
            name = 'Guest' + str(random.randint(1000, 9999))
            # logger.info('Your name is:'+name)
            print('Your name is:' + name)
        s.sendto(name.encode(encoding), server)

        recvPackets = queue.Queue()
        threading.Thread(target=ReceiveData, args=(s, encoding, BufferSize)).start()

        while True:
            if join == False:
                data = '[' + name + '] -> join chat'
                s.sendto(data.encode(encoding), server)
                join = True
            data = input()
            if data == 'exit':
                # data='['+name+']' + ' <- ' + 'left the chat'
                # s.sendto(data.encode(encoding),server)
                break
            elif data == '':
                continue
            elif data == '/rename':
                old_name = name
                name = rename(name)
                data = '[' + old_name + ']' + ': change name' + ' on ' + '[' + name + ']'
                s.sendto(data.encode(encoding), server)
            elif data == '/connect':
                data = '[' + name + ']' + ' <- ' + 'left the chat'
                s.sendto(data.encode(encoding), server)
                connect(serverIP, port)
            elif data[0] == '/':
                pass
            else:
                data = '[' + name + ']' + ' -> ' + data
                s.sendto(data.encode(encoding), server)
        data = '[' + name + ']' + ' <- ' + 'left the chat'
        s.sendto(data.encode(encoding), server)
        s.close()
        os._exit(1)
except:
    # logger.info('Client closed')
    print('Client closed')

# if len(sys.argv)==2:
RunClient('localhost', 25505)
# else:
#   RunClient(sys.argv[1])
