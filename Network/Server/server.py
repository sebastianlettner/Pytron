import socket
import sys
import os
from threading import Thread
from message import messagehandler
import pygame
import numpy as np
import itertools
import time

command_from_client = {"HELLO" : 3,"LIST_GAMES" : 1,"CREATE_MATCH" : 4,
                       "LIST_MATCHES" : 2, "MATCH_FEATURES" : 2, "JOIN_MATCH" : 3,
                       "LEAVING_MATCH" : 2,"I_AM_READY" : 1}

server_features = "BASIC"
list_game_names = "Tron"
supported_game = "Tron"
list_of_active_matches = []
list_of_active_matches_names = []
list_of_current_games = []
available_upd_game_port = [20000]




# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread):
    """ This class exists for every connected Client
        and contains its TCP connection, ip nad port"""
    name = ""

    def __init__(self,ip,port,conn,id_in_list):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.id_in_list = id_in_list
        self.active = True

        print( "[+] New server socket thread started for " + ip + ":" + str(port))

    def run(self):
        while self.active:
            data = self.conn.recv(4096)
            data = data.decode("ASCII")

            if data != "":
                data_list = data.split("\x00")
                print( "Server received data in Client Thread " + str(self.id_in_list) + ":", data)
                for messages in data_list:
                    message_for_client = received_message(data, self.ip , self.port, self.id_in_list)
                    if not (message_for_client == "Nothing to send"):
                        self.send(message_for_client)

    def send(self, message):
        self.conn.send(message.encode("ASCII"))


class match(object):
    """contains the creator and the game specs"""
    def __init__(self,creator,game,name,list_of_features):
        self.creator = creator
        self.game = game
        self.name = name
        self.features_list = list_of_features


class Logic(object):
    """ Implements the logic of TRON. This would be your server.

        This game is hard coded for two players, but easily extensible to
        multiple ones.
    """

    def __init__(self, num_x_tiles, num_y_tiles):
        """ Initializes object.

            Args:
                num_x_tiles (int): Width of the game board.
                num_y_tiles (int): Height of game board.
        """
        self.num_player = 2
        # Game board is represented as a matrix of zeros. A zero indicates a
        # free cell. A value different from zero indicates an barrier. Other
        # values are the other players ids.
        self.game_board = np.zeros((num_x_tiles, num_y_tiles), dtype = np.int)
        self.num_x_tiles = num_x_tiles
        self.num_y_tiles = num_y_tiles
        move_vectors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Set initial position of players
        x1 = np.random.randint(0, num_x_tiles)
        y1 = np.random.randint(0, num_y_tiles)

        # Get a starting position that is different from existing one
        x2 = x1
        y2 = y1
        while (x1 == x2) and (y1 == y2):
            x2 = np.random.randint(0, num_x_tiles)
            y2 = np.random.randint(0, num_y_tiles)

        # Set initial positions of players in board
        self.game_board[y1, x1] = 1
        self.game_board[y2, x2] = 2

        # Randomly select direction to move
        init_direction1 = move_vectors[np.random.randint(0, len(move_vectors))]
        init_direction2 = move_vectors[np.random.randint(0, len(move_vectors))]
        print(init_direction1)
        # Initialize player dictionaries. Better style (especially if you add
        # more sophisticated features) would be to create own classes.
        #colors = ["#1b9e77", "#7570b3"]
        self.players = {
                1: {
                        "posx": x1,
                        "posy": y1,
                        "vx": init_direction1[0],
                        "vy": init_direction1[1],
                        "color": (pygame.Color("red")),
                        "alive": True
                   },
                2: {
                        "posx": x2,
                        "posy": y2,
                        "vx": init_direction2[0],
                        "vy": init_direction2[1],
                        "color": (pygame.Color("green")),
                        "alive": True
                }
        }

    def set_direction(self, player_id, vx, vy):
        """
        Update directional vector of a player.

        Args:
            player_id (int): ID of player.
            vx (int): Speed in x direction.
            vy (int): Speed in y direction.

        Returns:
            None
        """
        # Perform updates only if new direction is orthogonal to previous one.
        # Protects player from running straight into his own tail, i.e., if
        # moving to the left and then pressing the move right key
        if (vx * self.players[player_id]["vx"] + vy * self.players[player_id]["vy"]) == 0:
            self.players[player_id]["vx"] = vx
            self.players[player_id]["vy"] = vy


    def update_player(self, player_id):
        """
        Perform one time step, i.e., calculate new position of a player based
        on his old position and current directional vector.
        It is only performed if the player is still alive. Else the player is
        ignored.

        Args:
            player_id (int): ID of Player.

        Returns:
            alive (boolean): Whether player is still alive or not
        """
        if self.players[player_id]["alive"]:
            x_new = int(self.players[player_id]["posx"]) + int(self.players[player_id]["vx"])
            y_new = int(self.players[player_id]["posy"]) + int(self.players[player_id]["vy"])


            if (x_new < 0) or (y_new < 0) or (x_new >= self.num_x_tiles) or (y_new >= self.num_y_tiles):
                self.players[player_id]["alive"] = False
            elif (self.game_board[y_new, x_new] != 0):
                self.players[player_id]["alive"] = False
            else:
                self.game_board[y_new, x_new] = player_id
                self.players[player_id]["posx"] = x_new
                self.players[player_id]["posy"] = y_new

        return self.players[player_id]["alive"]

    def get_board(self):

        board = self.game_board
        return(board)


def listen():
    """ This function listens for
    new connections the hole time
    and saves the connections in threads[] """
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_IP = "192.168.0.12"
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_PORT = 54001
    id_in_list = 0
    tcpServer.bind((TCP_IP, TCP_PORT))
    tcpServer.listen(4)

    while True:
        print( "Multithreaded Python server : Waiting for connections from TCP clients...")
        (conn, (ip,port)) = tcpServer.accept()
        newthread = ClientThread(ip,port,conn,id_in_list)
        newthread.start()
        threads.append(newthread)
        id_in_list +=1


def listen_broadcast():
    #UPD Socket initial for Broadcast
    UDP_PORT = 54000
    udpServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpServer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udpServer.bind(('',UDP_PORT))
    TCP_PORT = str(54001)
    while True:
        MESSAGE = "LOBBY " + TCP_PORT
        data , adr = udpServer.recvfrom(1024)
        data = data.decode("ASCII")
        if data == "DISCOVER_LOBBY":
            udpServer.sendto(MESSAGE.encode("ASCII"), adr)
        else:
            MESSAGE = messagehandler.ERR_CMD_NOT_UNDERSTOOD()
            MESSAGE = MESSAGE.complete_message
            udpServer.sendto(MESSAGE.encode("ASCII"), adr)


def check_feature_support(list_of_features):

    features_list = list_of_features.split(",")
    for features in features_list:
        if (features not in server_features):
            return False
        else: return True


def check_color(color):
    color_list = color.split(",")
    if len(color_list) != 3:
        return False

    for color in color_list:
        if not color.isdigit():
            return False

    for color in color_list:
        color = int(color)
        if color < 0 or color > 255:
            return False
    return True


class game(Thread):

    """
        Class Game representing the a match with two players
        client1_p1 : The creator of the game (we Initialize with the thread object
                                             so we have the TCP connection, port, ip, id and name)
        client2_p2 : The person who joined (we also Initialize with the thread object)
        udp_game_port : the port for the upd socket which the game will use
        list_of_features : the feature the shall be activaded for this game

    """


    def __init__(self,
                client1_p1,
                client2_p2,
                list_of_features,
                color_p1,
                color_p2,
                game_name,
                match_name,
                id_in_list_of_current_game,
                udp_port):

        Thread.__init__(self)
        self.client1_p1 = client1_p1
        self.client2_p2 = client2_p2
        self.player1_id = 1 #creator
        self.player2_id = 2 #the one who joined
        self.list_of_features = list_of_features
        self.color_p1 = color_p1 #(0,0,128) cant be changed so far
        self.color_p2 = color_p1
        self.game_name = game_name #Tron
        self.match_name = match_name #e.g Test match
        self.id = id_in_list_of_current_game
        self.udp_port = udp_port
        self.ready_p1 = False
        self.ready_p2 = False
        self.logic = Logic(18,18) #the game logic (field is 15x15 as default)
        self.udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udpsocket.bind(("192.168.0.12", self.udp_port))
        self.playing = True

    def run(self):
        """
        Advance the game one click at a time. At every klick handle the events
        that occurred. If key down events occurred, this method checks whether
        they correspond to movement keys of a player and sets the corresponding
        directional vector accordingly.
        As soon as one player dies the game is over.

        Returns:
            None
        """
        clock = pygame.time.Clock()
        #GameLoop
        while self.ready_p1 and self.ready_p2 and self.playing:

            #Regelt das empfangen über das udpgamesocket
            direction_handler = CLient_UDP_INGAME(self.udpsocket, self.id, self.client1_p1.ip, self.client2_p2.ip)
            direction_handler.start()

            #Updated das Spielfeld und überprüft "alive"
            alive1 = self.logic.update_player(1)
            alive2 = self.logic.update_player(2)

            #überprüfe ob spiel weiterlaufen soll
            if (not alive1):
                message1 = messagehandler.GAME_ENDED("You lost!")
                message2 = messagehandler.GAME_ENDED("You won!")
                message1 = message1.complete_message
                message2 = message2.complete_message
                self.client1_p1.send(message1)
                self.client2_p2.send(message2)
                self.playing = False


            if (not alive2):
                message1 = messagehandler.GAME_ENDED("You won!")
                message2 = messagehandler.GAME_ENDED("You lost!")
                message1 = message1.complete_message
                message2 = message2.complete_message
                self.client1_p1.send(message1)
                self.client2_p2.send(message2)
                self.playing = False


            board = self.logic.get_board()
            message = GET_GAMEBOARD_FORMAT(board)
            direction_handler.send(message)

            #controls speed of "snake"
            clock.tick(0.5)

class CLient_UDP_INGAME(Thread):

    def __init__(self, udp_socket, game_id, ip_p1, ip_p2):
        Thread.__init__(self)
        self.udp_socket = udp_socket
        self.id = game_id
        self.ip_p1 = ip_p1
        self.ip_p2 = ip_p2



    def run(self):

        while True:

            data, adr = self.udp_socket.recvfrom(32)
            ip,port = adr
            data = data.decode("ASCII")
            data = data.split()

            '''QUESTION: How can i detect which port belongs to which player??'''
            if port == 2000:
                player_id = 1
            else:
                player_id = 2

            if data[1] == "NEW_DIRECTION":

                # not empty direction
                if (len(data) == 3):
                    direction = data[2]
                    direction = direction.split(",")

                    list_of_current_games[self.id].logic.set_direction(player_id,int(direction[0]),int(direction[1]))

    def send(self, message):

        message = message.encode("ASCII")
        self.udp_socket.sendto(message, (self.ip_p1, 2000))
        self.udp_socket.sendto(message, (self.ip_p2, 2001))

def GET_GAMEBOARD_FORMAT(board):
    row = []
    #get matrix to list
    liste = board.tolist()
    #for loops format to sendable message
    for i in range(len(liste)):
        string = ''.join(str(liste[i]))
        string = string.replace(" ", "")
        row.append(string)

    for i in range(len(row)):
        msg = ';'.join(row)
    msg = str(msg)
    msg = msg.replace("[", "")
    msg = msg.replace("]", "")
    #board is now in protocol format
    #code takes under 1msec for 50x50 board
    return(msg)






def HELLO(message_c,id_of_client):

    returnMessage = messagehandler.WELCOME(server_features)
    returnMessage = returnMessage.complete_message
    threads[id_of_client].name = message_c.message_split[1]
    return returnMessage

def CREATE_Match(message_c,port_of_client,id_of_client):

    #check if game is valid (we only support tron)
    if message_c.message_split[1] != supported_game:
        returnMessage = messagehandler.ERR_FAILED_TO_CREATE("Game not supported")
        returnMessage = returnMessage.complete_message
        return returnMessage

    """create a match object in which we put or
    creator the game name (tron) and the name of the match +
    list of features """
    check = check_feature_support(message_c.message_split[3])
    if not check:
        returnMessage = messagehandler.ERR_FAILED_TO_CREATE("feature not supported")
        returnMessage = returnMessage.complete_message
        return returnMessage
    else:
        created_match = match(threads[id_of_client], supported_game, message_c.message_split[2], message_c.message_split[3])
        list_of_active_matches.append(created_match)
        list_of_active_matches_names.append(created_match.name)

    """return the answer with id 1 as the player id
        the creator always gets id 1"""

    returnMessage = messagehandler.GAME_CREATED(1)
    returnMessage = returnMessage.complete_message
    return returnMessage

def LIST_MATCHES(message_c):
    # check if game is Tron
    if message_c.message_split[1] != supported_game:
        print(message_c.message_split[1])
        returnMessage = messagehandler.ERR_CMD_NOT_UNDERSTOOD()
        returnMessage = returnMessage.complete_message
        return returnMessage
    #returns the list
    else:
        list_of_active_matches_str = ','.join(list_of_active_matches_names)
        returnMessage = messagehandler.GAMES(supported_game, list_of_active_matches_str)
        returnMessage = returnMessage.complete_message
        return returnMessage



def MATCH_FEATURES(message_c):

    game_name = message_c.message_split[1]

    #check if name of the match is available if True return list of feature of this game
    if game_name in list_of_active_matches_names:
        index = list_of_active_matches_names.index(game_name)
        returnMessage = messagehandler.MATCH(supported_game, game_name, list_of_active_matches[index].features_list)
        returnMessage = returnMessage.complete_message
        return returnMessage
    #else send error
    else:
        returnMessage = messagehandler.ERR_GAME_NOT_EXIST(game_name)
        returnMessage = returnMessage.complete_message
        return returnMessage

def JOIN_MATCH(message_c,port_of_client, id_of_client, game_id, udp_port):
    game_name = message_c.message_split[1]
    color_p2 = message_c.message_split[2]
    valid_color = check_color(color_p2)

    if game_name not in list_of_active_matches_names:
        returnMessage = messagehandler.ERR_FAILED_TO_JOIN("Match name not found!")
        returnMessage = returnMessage.complete_message
        return returnMessage
    elif not valid_color:
        returnMessage = messagehandler.ERR_FAILED_TO_JOIN("Invalid color!")
        returnMessage = returnMessage.complete_message
        return returnMessage
    else:
        index = list_of_active_matches_names.index(game_name)
        game1 = game(
            list_of_active_matches[index].creator,
            threads[id_of_client],
            list_of_active_matches[index].features_list,
            (0,0,128),
            color_p2,
            supported_game,
            list_of_active_matches_names[index],
            game_id,
            udp_port
            )
        game1.start()
        list_of_current_games.append(game1)

        #The player who joined always has ID two
        returnMessage = messagehandler.GAME_JOINED(2)
        returnMessage = returnMessage.complete_message


        '''sending the match started message to both players
        at this point its safe that the game will start because the game object is already
        initialized'''

        MATCH_STARTED(list_of_active_matches[index],threads[id_of_client], udp_port, (0,0,128), color_p2)
        list_of_active_matches.pop(index)
        list_of_active_matches_names.pop(index)
        return returnMessage

def MATCH_STARTED(tcpSocket_p1,tcpSocket_p2,udp_port,color_p1,color_p2):

    string_color1 = ','.join(map(str,color_p1))
    #string_color2 = ','.join(map(str,color_p2))
    list_players_colors = "1," + string_color1 + ",2," + str(color_p2)
    print(list_players_colors)
    message = messagehandler.MATCH_STARTED(udp_port, list_players_colors )
    message = message.complete_message
    tcpSocket_p1.creator.send(message)
    tcpSocket_p2.send(message)
    return

def I_AM_READY(message_c,port_of_client):

    for game_object in list_of_current_games:

        if game_object.client1_p1.port == port_of_client:
            game_object.ready_p1 = True
            if game_object.ready_p2 == True:
                game_object.run()
            return
        if game_object.client2_p2.port == port_of_client:
            game_object.ready_p2 = True
            if game_object.ready_p1 == True:
                game_object.run()
            return
        else:
            #If client is not in a game??
            return




def received_message(message, ip_of_client, port_of_client, id_of_client):
    message_from_ip = ip_of_client
    message_from_port = port_of_client
    message_c = messagehandler.message(message)
    message_c.m_split()
    command = message_c.message_split[0]    #where the cmd should be
    check_if_valid = (command in command_from_client)
    game_id = 0
    udp_port = 20000
    #if command is supported (the specific message parts arent checked yet)
    if check_if_valid:


        #check if length of message is ok (for example if a message only contains
        #the command is has length 1)
        if command_from_client[message_c.command] != message_c.length:
            returnMessage = messagehandler.ERR_CMD_NOT_UNDERSTOOD()
            returnMessage = returnMessage.complete_message
            return returnMessage



        #check which command we received
        elif message_c.command == "HELLO":

            """saves the name of the client in the object of the client
                returnMessage : the welcome command + list of our features"""

            returnMessage = HELLO(message_c, id_of_client)
            return returnMessage


        elif message_c.command == "LIST_GAMES":

            """ returns the list of available games
                in our case its just tron"""

            returnMessage = messagehandler.AVAILABLE_GAMES(list_game_names)
            returnMessage = returnMessage.complete_message
            return returnMessage


        elif message_c.command == "CREATE_MATCH":

            returnMessage = CREATE_Match(message_c, port_of_client, id_of_client)
            return returnMessage


        elif message_c.command == "LIST_MATCHES":

            returnMessage = LIST_MATCHES(message_c)
            return returnMessage



        elif message_c.command == "MATCH_FEATURES":

            returnMessage = MATCH_FEATURES(message_c)
            return returnMessage



        elif message_c.command == "JOIN_MATCH":

            game_name = message_c.message_split[1]

            '''Der Name des Spiels, dem beigetreten werden soll (game_name)
            game_id entsprich der position des objekts in der list_of_current_games
            Der Port wird für jedes neue Spiel um 1 erhöht
            '''
            game_id = len(list_of_current_games)

            returnMessage = JOIN_MATCH(
                            message_c,
                            port_of_client,
                            id_of_client,
                            game_id,
                            available_upd_game_port[0])
            '''the udport hast to be different for each game '''
            available_upd_game_port[0] = available_upd_game_port[0] + 1


            return returnMessage


        elif message_c.command == "I_AM_READY":
            I_AM_READY(message_c,port_of_client)


            return ("Nothing to send")




    else:
        returnMessage = messagehandler.ERR_CMD_NOT_UNDERSTOOD()
        returnMessage = returnMessage.complete_message
        return returnMessage




"""----------------------------------------------------------------------------
----------------------------------------------------------------------------"""
# Multithreaded Python server
#Start listening for Client connection + boradcast
threads = []
thread_listen = Thread(target = listen, args = ())
thread_listen.start()
thrad_listen_broadcast = Thread(target = listen_broadcast, args = ())
thrad_listen_broadcast.start()

###############################################################################
