
server_features = "BASIC,SLOW,FAST,WALLS"
game_names = "Tron"
game = "Tron"
command_from_client = ["HELLO","LIST_GAMES","CREATE_Match",
                       "LIST_MATCHES", "MATCH_FEATURES", "JOIN_MATCH", "LEAVING_MATCH",
                       "I_AM_READY", "NEW_DIRECTION"]




class message(object):
    """
    Implement a Message
    """


    def __init__(self,message):

        """
        Initializes Object

        Args:
            message (string): The message you want to initialize as an object
        """

        self.message = message

    def m_split(self):

        """
        Splits the message by spaces

        Variables:
            message_split (list): Contains the parts of the
                                  message which were seperated by spaces.

            length (int): amount of words seperated by spaces in the message.

            command (string): The first word of the message.
                              If its a protocoll message this should be the command.

        """

        self.message_split = self.message.split()
        self.length = len(self.message_split) #useless so far
        self.command = self.message_split[0]


"""
The following classes each implement one protocoll message.
They always contain the command as the first word and if necessary
one can initialize the object with the intended arguments.
This way we can easily change the protocoll messages

The complete_message (string) variable represents the full command
ready to be sended.
"""



class WELCOME(object):

    def __init__(self,list_server_features):

        self.command = "WELCOME "

        self.list_server_features = server_features

        self.complete_message = self.command + self.list_server_features + "\x00"

class LOBBY(object):

    def __init__(self,port):

        self.port = port

        self.command = "LOBBY "

        self.complete_message = self.command + str(self.port) + "\x00"

class AVAILABLE_GAMES(object):

    def __init__(self,list_game_names):

        self.command = "AVAILABLE_GAMES "

        self.list_game_names = list_game_names

        self.complete_message = self.command + self.list_game_names + "\x00"

class GAME_CREATED(object):

    def __init__(self,player_id):

        self.command = "GAME_CREATED "

        self.player_id = player_id

        self.complete_message = self.command + str(self.player_id) + "\x00"

class GAMES(object):

    def __init__(self,game,list_matches):

        self.command = "GAMES "

        self.game = game + " "

        self.list_matches = list_matches

        self.complete_message = self.command + self.game + self.list_matches + "\x00"

class MATCH(object):

    def __init__(self,game,name_of_match,list_match_features):

        self.command = "MATCH "

        self.game = game + " "

        self.name_of_match = name_of_match + " "

        self.list_match_features = list_match_features

        self.complete_message = self.command + self.game + self.name_of_match + self.list_match_features + "\x00"

class GAME_JOINED(object):

    def __init__(self,player_id):

        self.command = "GAME_JOINED "

        self.player_id = player_id

        self.complete_message = self.command + str(self.player_id) + "\x00"

class MATCH_STARTED(object):

    def __init__(self,udp_port,list_player_id_color):

        self.command = "MATCH_STARTED "

        self.udp_port = str(udp_port) + " "

        self.list_players_colors = list_player_id_color

        self.complete_message = self.command + str(self.udp_port) + self.list_players_colors + "\x00"

class GAME_ENDED(object):

    def __init__(self,reason):

        self.command = "GAME_ENDED "

        self.reason = reason

        self.complete_message = self.command + self.reason + "\x00"

class UPDATE_FIELD(object):
    pass

""" All Error Messages
    the server can send """

class ERR_CMD_NOT_UNDERSTOOD(object):

    def __init__(self):

        self.command = "ERR_CMD_NOT_UNDERSTOOD "


        self.complete_message = self.command  + "\x00"

class ERR_FAILED_TO_CREATE(object):

    def __init__(self,reason):

        self.command = "ERR_FAILED_TO_CREATE "

        self.reason = reason

        self.complete_message = self.command + self.reason + "\x00"

class ERR_FAILED_TO_JOIN(object):

    def __init__(self,reason):

        self.command = "ERR_FAILED_TO_JOIN "

        self.reason = reason

        self.complete_message = self.command + self.reason + "\x00"

class ERR_GAME_NOT_EXIST(object):

    def __init__(self,name_of_match):

        self.command = "ERR_GAME_NOT_EXIST "

        self.name_of_match = name_of_match

        self.complete_message = self.command + self.name_of_match + "\x00"

class DISCONNECTED_YOU(object):

    def __init__(self,reason):

        self.command = "DISCONNECTED_YOU "

        self.reason = reason

        self.complete_message = self.command + self.reason + "\x00"

"""----------------------------------------------------------------------------
----------------------------------------------------------------------------"""
"""All messages the Client can send"""

class HELLO(object):

    def __init__(self,name,features):

        self.command = "HELLO "

        self.name = name + " "

        self.features = features

        self.complete_message = self.command + self.name + self.features + "\x00"

class LIST_GAMES(object):

    def __init__(self):

        self.command = "LIST_GAMES"

        self.complete_message = self.command + "\x00"

class CREATE_MATCH(object):

    def __init__(self,game,name,features):

        self.command = "CREATE_MATCH "

        self.game =  game + " "

        self.name = name + " "

        self.features = features

        self.complete_message = self.command + self.game + self.name + self.features + "\x00"

class LIST_MATCHES(object):

    def __init__(self,game):

        self.command = "LIST_MATCHES "

        self.game = game

        self.complete_message = self.command + self.game + "\x00"

class MATCH_FEATURES(object):

    def __init__(self,name):

        self.command = "MATCH_FEATURES "

        self.name = name


        self.complete_message = self.command + self.name + "\x00"

class JOIN_MATCH(object):

    def __init__(self,name,color):

        self.command = "JOIN_MATCH "

        self.name = name + " "

        self.color = str(color)

        self.complete_message = self.command + self.name + self.color + "\x00"

class I_AM_READY(object):

    def __init__(self):

        self.command = "I_AM_READY "

        self.complete_message = self.command + "\x00"

class LEAVING_MATCH(object):

    def __init__(self,reason):

        self.command = "LEAVING_MATCH "

        self.reason = reason

        self.complete_message = self.command + self.reason + "\x00"
