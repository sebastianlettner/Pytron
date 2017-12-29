import socket
from threading import Thread
import sys
import pygame
import numpy as np
import itertools
import time
import random
from message import messagehandler
import lobbygui
import time

"""
This is the executable of the clientside of this game.
In the following code we used some global lists (probably bad style)
The first two list following contain general information.

The udp_port_list saves the port for the UDP Socket created for the match.

The my_player_id_l list contains the ID a player gets from the server.

The game_list is filled with the game object when a match is started.

The game_end_list is filled with the *reason* of the GAME_ENDED
message when a match is over.

"""


game = "Tron"
supported_features = "BASIC"
udp_port_list = []
my_player_id_l = []
my_player1_color = []
my_player2_color = []
game_list = []
game_end_list = []

def broadcast():
    """
    Performs the sending of the broadcast message.
    If there is no answer within 5 sec a timeout
    exception is thrown.

    Retruns:
        host (string): The ip of the server
        port (int): The port the server listens for TCP connections
    """

    BUFFER_SIZE = 2000

    udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udpClient.settimeout(5)
    MESSAGE = "DISCOVER_LOBBY\x00"
    udpClient.sendto(MESSAGE.encode("ASCII"), ('255.255.255.255', 54000))
    try:
        data ,adr = udpClient.recvfrom(BUFFER_SIZE)

    except socket.timeout:
        udpClient.close()
        return 0,0
    data = data.decode("ASCII")
    data = data.split()
    if str(data[0]) == "LOBBY":
        host,port = adr
        port = int(data[1])
        print("Found Server with IP: " + str(host) + " on Port: " + str(port))

    else:
        udpClient.close()
        return 0,0
    udpClient.close()
    return host,port


class ClientTcp(Thread):

    """
    Implements the TCP connection to the Server.
    Threads are used for parallel working.
    """

    def __init__(self, host, port):
        """
        Initializes Object.

        Args:
            host (string): ip of Server
            port (int): the prot we received throug the broadcast for the TCP
            active_lobby (bool): Flag that tells us if we are still in the lobby
                                 If i.e. a game/match starts we close the lobby
                                 and display the gamefield using pygame.

        """
        Thread.__init__(self)

        self.host = host
        self.port = port
        self.tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsocket.connect((self.host,self.port))
        self.tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.active_lobby = True

    def send(self, message):
        """
        Can send a message via TCP to the server.

            Args:
                message (string): The message that is sended
        """
        message = message.encode("ASCII")
        try:
            self.tcpsocket.send(message)
        except BrokenPipeError:
            lobbygui.error_gui("Connection Lost",None)


    def run(self):
        """
        The run function of the Thread receives the messages from the Server.
        Calls the answer_handler function to process the message
        """
        while True:
            try:
                data = self.tcpsocket.recv(1024)
                data = data.decode("ASCII")
                if data != "":
                    print("In TCP:",data)

                    data = data.split("\x00")
                    for i in range(len(data)-1):
                        msg = str(data[i])
                        self.active_lobby = answer_handler(msg)
            except ConnectionResetError:
                lobbygui.error_gui("Connection Lost",None)
    """
    The following functions can be used to transmit the protocoll-messages
    to the server.
    """

    def LIST_GAMES(self):
        msg = messagehandler.LIST_GAMES()
        msg = msg.complete_message
        self.send(msg)


    def LIST_MATCHES(self,game):

        msg = messagehandler.LIST_MATCHES(game)
        msg = msg.complete_message
        self.send(msg)

    def MATCH_FEATURES(self,name):

        msg = messagehandler.MATCH_FEATURES(name)
        msg = msg.complete_message
        self.send(msg)

    def JOIN_MATCH(self,name,color):

        msg = messagehandler.JOIN_MATCH(name,color)
        msg = msg.complete_message
        self.send(msg)

    def CREATE_MATCH(self,game,name,features):

        msg = messagehandler.CREATE_MATCH(game,name,features)
        msg = msg.complete_message
        self.send(msg)

    def I_AM_READY(self):

        msg = messagehandler.I_AM_READY()
        msg = msg.complete_message
        self.send(msg)




class Game(object):
    """
    Implements the Game for to players.
    """
    def __init__(self,tcpconnection,udp_port,server_ip, player_id):

        """
        Initializes Object

            Args:
                tcp (object): The TCP connection to the server
                The Tcp object is initialized before a match is started.
                server_ip (string): IP of server we communicate with.
                udp_port (int): Port for the udp_socket we send to.
                udp_socket (socket): The actual socket for the match.
                random_port (int): A random port the client listens on the udp_socket.
                gui (object): The pygame gui for the match (not the lobby).
                player_id (int): ID of the player
                playing (bool): Just a flag.

        """
        self.tcp = tcpconnection
        self.server_ip = server_ip
        self.udp_port = udp_port
        self.udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.random_port = random.randint(1000,10000)
        self.udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpsocket.bind((socket.gethostbyname(socket.gethostname()), self.random_port))
        #self.udpsocket.bind(("", self.random_port))
        self.gui = GUI(25,25,30,30)
        self.udp_port = int(udp_port)
        self.player_id = player_id
        self.playing = True

    def event_loop(self):
        #start listening on udp
        listen_udp_object = listen_udp(self.udpsocket,self.gui)
        listen_udp_object.daemon = True
        listen_udp_object.start()
        seq = 1
        not_ready = True
        while not_ready:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        """Sending an empty direction to tell
                        the server our port as early as possible"""

                        msg = "0" + " NEW_DIRECTION " + str(self.player_id)
                        self.tcp.I_AM_READY()
                        not_ready = False
                        self.udpsocket.sendto(msg.encode("ASCII"),(self.server_ip,self.udp_port))


        m = np.zeros((30, 30), dtype = np.int)
        self.gui.draw(m)

        while self.playing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        # Player moving to upper edge of screen
                        msg = str(seq) + " NEW_DIRECTION " + str(self.player_id) + " 0,-1"
                        self.udpsocket.sendto(msg.encode("ASCII"),(self.server_ip,self.udp_port))
                        seq += 1

                    elif event.key == pygame.K_DOWN:
                        # Player moving to lower edge of screen
                        msg = str(seq) + " NEW_DIRECTION " + str(self.player_id) + " 0,1"
                        self.udpsocket.sendto(msg.encode("ASCII"),(self.server_ip,self.udp_port))
                        seq += 1

                    elif event.key == pygame.K_LEFT:
                        # Player moving to the left
                        msg = str(seq) + " NEW_DIRECTION " + str(self.player_id) +  " -1,0"
                        self.udpsocket.sendto(msg.encode("ASCII"),(self.server_ip,self.udp_port))
                        seq += 1

                    elif event.key == pygame.K_RIGHT:
                        # Player moving to the right
                        msg = str(seq) + " NEW_DIRECTION " + str(self.player_id) + " 1,0"
                        self.udpsocket.sendto(msg.encode("ASCII"),(self.server_ip,self.udp_port))
                        seq += 1

                    #------------------
        #Quits the loop in the udpsocket run funtion
        listen_udp_object.keeprunning = False



class listen_udp(Thread):
    """
    Takes care of the udp connection of the match
    """

    def __init__(self, udp_socket, gui):
        """
        Initializes Object

            Args:
                udp_socket (socket): The udp_socket wich is created when a match
                                     is initialized

                gui (obbject): The initialization of GUI for the match

                keeprunning (bool): Flag for the run loop
        """
        Thread.__init__(self)
        self.udp_socket = udp_socket
        self.gui = gui
        self.keeprunning = True

    def run(self):
        """
        Takes care of receiving messages from the server via the udp_socket
        of the match
        We interpret the messages here and dra the game board.
        """
        while self.keeprunning:
            try:
                data, adr = self.udp_socket.recvfrom(8192)
                ip,port = adr
                data = data.decode("ASCII")
                data = data.split(" ") #0:seq 1:cmd 2:row_col 3:board
                if data[1] == "UPDATE_FIELD":
                    board = data[3].split("\x00")
                    board = board[0]
                    self.gui.draw(board)
                else:
                    print("Cmd not undestood")
            except ConnectionResetError:
                print("Connction lost")

class GUI(object):
    """
    Object handling drawing of the field.
    """

    def __init__(self, width, height, num_x_tiles, num_y_tiles):
        """
        Initializes object.

        Args:
            width (int): Width in pixel of one game cell.
            height (int): Height in pixel of one game cell.
            num_x_tiles (int): Width of game board, i.e., number of cells the
                board has in horizontal direction.
            num_y_tiles (int): Height of game board, i.e., number of cells the
                board has in vertical direction.
        """
        self.width = width
        self.height = height
        self.num_x_tiles = num_x_tiles
        self.num_y_tiles = num_y_tiles

        pygame.init()
        #Sick name of our game
        pygame.display.set_caption("Pytron")

        self.screen = pygame.display.set_mode((
                self.width * self.num_x_tiles,
                self.height * self.num_y_tiles
                ))
        self.screen.fill(pygame.Color(120,120,120))

    def draw(self,gameboard):
        """
        Draw the current state of the board.

        Returns:
            None
        """
        #gameboard = gameboard.split(";")
        m = np.asmatrix(gameboard)
        #Fill screen with black color
        self.screen.fill(pygame.Color("black"))
        for i in range(self.num_x_tiles):
            for j in range(self.num_y_tiles):
                y = 0 if i == 0 else i * self.height
                x = 0 if j == 0 else j * self.width

                w = self.width - 2
                h = self.height - 2

                try:
                    if m[i, j] == 0:
                       color = (120, 120, 120)
                    else:
                       if m[i, j] == 1:
                           color = (my_player1_color[0], my_player1_color[1],my_player1_color[2])
                       if m[i, j] == 2:
                           color = (my_player2_color[0],my_player2_color[1],my_player2_color[2])
                except IndexError:
                    print("Sth wrong with board")
                pygame.draw.rect(self.screen, color, (x, y, w, h))
        pygame.display.update()



class LOBBY(object):

    """
    Implements the Lobby (the state of the programm before the gameboard is
                          displayed)
    """

    def __init__(self,tcp_connection,name,color,ipstring):
        """
        Initializes Object

        Args:
            tcp_connection (object): The initialization of the ClientTcp class.
            name (string): Name the of the player.
            color (RGB): Color of the player.
            ipstring (string): A string conatining host ip and port.
        """
        self.tcp = tcp_connection
        self.name = name
        self.color = color
        self.ipstring = ipstring


    def event_loop(self):

        """
        #######################
        """

        clock = pygame.time.Clock()
        clock.tick(5)

        print("Welcome to the Game Lobby!\n")

        '''
        Initialization of second gui screen where the player can create or join a game
        '''
        while True:
            
            #get list of available games and save it in a txt file
            self.tcp.LIST_MATCHES(game)
            time.sleep(1)
            gameslist=open('pythron_gameslist.txt','r')
            gameslist=str(gameslist.read())
            gameslist=gameslist.split(',')
            #starts second gui and stays in mainloop
            lobbygui.start_gui2(gameslist,ipstring)
            #get information out of txt file
            cache = open("pythron_savecache.txt",'r')
            string = str(cache.read())
            cache = string.split('\n')
            state = int(cache[0])
            print(state)
            '''
            state:
            0 : cancel button was pressed
            1 : refresh button was pressed
            2 : join game was pressed and game was selected
            3 : create game was pressed
            '''
            if state == 0:
                sys.exit()

            if state ==2:
                #join game
                namegame=cache[1]
                self.tcp.JOIN_MATCH(namegame, color)
                self.tcp.active_lobby = False
                break

            if state ==3:
                #create game
                namegame=cache[1]
                featureslow = cache[2]
                featurewalls = cache[3]
                featurefast = cache[4]
                 #create correct feature string 
                features = None
                #if fast and slow are selected the speed stays normal
                if featurefast == 'ON' and featureslow == 'OFF':
                    features = 'FAST'
                if featurefast == 'OFF' and featureslow == 'ON':
                    features = 'SLOW'


                if featurewalls == 'ON' and features==None:
                    features='WALLS'
                if featurewalls == 'ON' and features!=None:
                    features=features+',WALLS'
                feature4 = cache[5]
                if features == None:
                    features = 'BASIC'
                self.tcp.CREATE_MATCH(game,namegame,features)
                print("Waiting for Opponent...")
                print_header_flag = False
                self.tcp.active_lobby = False
                break



def answer_handler(message):

    """
    Performs the handling of incoming Protocoll messages.
    Is called in the ClientTcp class (run function).
    Basically compares the messages to what we expect and if its valid
    performs the necessary steps.
    The prints are only for help. Everything can also be seen on our official
    GUI.

    This is also the the place were the GUI interacts with the client.
    The GUI saves the informations of the server from here.

    Return:
        True: if we want to stay in the lobby after this call
        False: if we dont want to stay in the lobby afeter this call
    """

    message_s = message.split()
    if len(message_s) != 0:
        command = str(message_s[0])

        if(command == "WELCOME") and (len(message_s) == 2):

            server_features = str(message_s[1])
            print("-------------------------------------------")
            print("The Server supports the following features: " + server_features)
            print("-------------------------------------------")

            return True

        elif(command == "AVAILABLE_GAMES") and (len(message_s) == 2):

            supported_games = str(message_s[1])
            print("-------------------------------------------")
            print("The Server supports the following games: " + supported_games)
            print("-------------------------------------------")

            return True

        elif(command == "GAME_CREATED") and (len(message_s) == 2):

            my_player_id = int(message_s[1])
            my_player_id_l.append(my_player_id)
            print("-------------------------------------------")
            print("Created match! Your ID is " + str(my_player_id))
            print("-------------------------------------------")


            return True

        elif(command == "GAMES") and ((len(message_s) == 3) or (len(message_s) == 2)):

            game = str(message_s[1])
            cache = open("pythron_gameslist.txt",'w')
            if len(message_s) == 3:
                list_open_matches = str(message_s[2])

                cache.write(list_open_matches)

            else:
                cache.write('No open matches')
                #print("-------------------------------------------")
                #print("No open games")
                #print("-------------------------------------------")'''

            return True

        elif(command == "MATCH") and (len(message_s) == 4):

            game = str(message_s[1])
            match_name = str(message_s[2])
            list_of_match_features = str(message_s[3])
            print("-------------------------------------------")
            print("In game " + game + " the match " + match_name + " supports the folloing features: " + list_of_match_features)
            print("-------------------------------------------")
            return True

        elif(command == "GAME_JOINED") and (len(message_s) == 2):

            my_player_id = int(message_s[1])
            my_player_id_l.append(my_player_id)
            print("-------------------------------------------")
            print("Joined match! Your ID is" + str(my_player_id))
            print("-------------------------------------------")
            return True

        elif (command == "MATCH_STARTED") and len(message_s) == 3:

            udp_port = message_s[1]
            playercolors = message_s[2].split(",")

            my_player1_color.append(int(playercolors[1]))
            my_player1_color.append(int(playercolors[2]))
            my_player1_color.append(int(playercolors[3]))

            my_player2_color.append(int(playercolors[5]))
            my_player2_color.append(int(playercolors[6]))
            my_player2_color.append(int(playercolors[7]))


            print("Match started!")
            udp_port_list.append(udp_port)
            #We want to leave the lobby after this one
            return False

        elif (command == "GAME_ENDED"):
            reason = ""
            if len(game_list) == 1:
                game_list[0].playing = False
            try:
                reason = str(message_s[1])+ " " + str(message_s[2])
            except IndexError:
                print("IndexError")
            game_end_list.append(reason)

            return False

        #If the message could not be interpeted
        else:
            return True
    #If the message could not be interpeted
    else:
        return True

def HELLO(tcp,name):
    """
    Send the HELLO cmd to the server

    Args:
        tcp (object): The TCP connection
        name (string): Teh players name
    """
    msg = messagehandler.HELLO(name,supported_features)
    msg = msg.complete_message
    tcp.send(msg)





"""-----------------------------------------------------------------------"""
if __name__ == "__main__":


    print('Welcome to Pytron')

    print('Looking for Servers...' )


    flag = 1
    while flag:
        """
        We stay here until we found a server with the server via broadcast
        """
        lobbygui.start_gui1()#open first gui element
        #get information from the gui input via txt file
        cache = open("pythron_savecache.txt",'r')
        string = str(cache.read())
        cache = string.split('\n')
        state = cache[0]
        if state == '0':
            sys.exit()
        name =  cache[1]
        color = cache[2]

        host,port = broadcast()
        if host:
            flag = 0
        if not host:
            lobbygui.error_gui('No servers found',None)

    """
    Initializing the TCP object as a Thread.
    """

    TCP_connection = ClientTcp(host,port)
    TCP_connection.daemon = True
    TCP_connection.start()
    
    if color == 'Red':
        color = '243,0,0'
    if color == 'Green':
        color = '0,243,0'
    if color == 'Blue':
        color = '0,0,243'
    if color == 'Yellow':
        color = '243,243,0'

    ipstring = str(host)+':'+str(port)
    #starting the Lobby
    l = LOBBY(TCP_connection,name,color,ipstring)
    l.event_loop()
    """
    We leave this loop when a match has started
    """

    #if we have an udp_port a match has started
    clock = pygame.time.Clock()
    i = 0

    while not(len(udp_port_list) == 1 and i<30 and len(my_player_id_l) == 1):
        """
        We stay in this loop until someone joins
        If there is a problem or nobody joins within 30 sec we leave the loop
        """
        print("Please wait...")
        clock.tick(0.5)
        i = i+1


    if len(udp_port_list) == 1:
        game = Game(TCP_connection,udp_port_list[0],host, my_player_id_l[0])
        game_list.append(game)
        game.event_loop()
    else:
        #go back to the lobby
        l.event_loop()
    #we get here when the game loop ends
    if len(game_end_list) != 0:
        lobbygui.message_gui(game_end_list[0] , 'Pythron')
