
# Python TCP Client B
import socket


BUFFER_SIZE = 2000


udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
MESSAGE = "DISCOVER_LOBBY"

#while True:
udpClient.sendto(MESSAGE.encode("ASCII"), ('255.255.255.255', 54000))
data, adr = udpClient.recvfrom(BUFFER_SIZE)
data = data.decode("ASCII")
print( " Client2 received data:", data)

data = data.split()
host,port = adr
port = int(data[1])
tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClientB.connect((host, port))
tcpClientB.settimeout(1)

while True:
    MESSAGE = input("Type message (C2): ")
    try:
        if MESSAGE != "a":

            tcpClientB.send(MESSAGE.encode("ASCII"))
            data = tcpClientB.recv(BUFFER_SIZE)
            data = data.decode("ASCII")
            print( " Client2 received data:", data)

        if MESSAGE == "a":
            print("AAAA")
            udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpsocket.bind((host, 2001))

            msg = "hallo test upd fuckin worked"

            udpsocket.sendto(msg.encode("ASCII"),(host,20000))


    except socket.timeout:
        print("Timed out")

tcpClientB.close()
udpsocket.close()
