import socket


BUFFER_SIZE = 2000

udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
MESSAGE = "DISCOVER_LOBBY"
from threading import Thread

def getboard(a,udpsocket):

    while True:

        data = udpsocket.recv(2048)
        data = data.decode("ASCII")
        data = data.split(";")
        for i in range(len(data)):
            print(data[i])
        print("___________________")

udpClient.sendto(MESSAGE.encode("ASCII"), ('255.255.255.255', 54000))
data ,adr = udpClient.recvfrom(BUFFER_SIZE)
udpClient.close()
print(data,adr)
data = data.decode("ASCII")
print( " Client2 received data:", data)
data = data.split()
host,port = adr
port = int(data[1])
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpClientB.connect((host, port))
tcpClientB.settimeout(0.1)


udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpsocket.bind((host, 2000))
thread_listen = Thread(target = getboard, args = (1,udpsocket))
thread_listen.start()

while True:
    MESSAGE = input("Type message (C2): ")

    try:
        if MESSAGE == "d":
            print("AAAA")

            msg = "1 NEW_DIRECTION 1,0"

            udpsocket.sendto(msg.encode("ASCII"),(host,20000))
        if MESSAGE == "s":
            print("AAAA")

            msg = "1 NEW_DIRECTION 0,1"

            udpsocket.sendto(msg.encode("ASCII"),(host,20000))


        if MESSAGE == "a":
            print("AAAA")

            msg = "1 NEW_DIRECTION -1,0"

            udpsocket.sendto(msg.encode("ASCII"),(host,20000))

        if MESSAGE == "w":
            print("AAAA")

            msg = "1 NEW_DIRECTION 0,-1"

            udpsocket.sendto(msg.encode("ASCII"),(host,20000))
        else:

            tcpClientB.send(MESSAGE.encode("ASCII"))
            data = tcpClientB.recv(BUFFER_SIZE)
            data = data.decode("ASCII")
            print( " Client2 received data:", data)



    except socket.timeout:
        print("Socket timed out")





tcpClientB.close()
udpsocket.close()
