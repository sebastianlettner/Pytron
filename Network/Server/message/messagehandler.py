server_features = "BASIC"
game_names = "Tron"
game = "Tron"
command_from_client = ["HELLO","LIST_GAMES","CREATE_Match",
                       "LIST_MATCHES", "MATCH_FEATURES", "JOIN_MATCH", "LEAVING_MATCH",
                       "I_AM_READY", "NEW_DIRECTION"]


class message(object):
    """ Creates message object
    message must be decoded"""


    def __init__(self,message):

        self.message = message

    def m_split(self):

        self.message_split = self.message.split()
        self.length = len(self.message_split) #useless so far
        self.command = self.message_split[0]

    def determine_command(self):
        pass

""" All the messages of
the lobby protocol that the server can send to
the client """



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

# class HELLO(object):
#
#     def __init__(self,name,list_client_features):
#
#         self.name = name
#
#         self.list_client_features = list_client_features
