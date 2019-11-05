import os
import slack
import coordinate_conversion
import game
from io import StringIO
import sys
import minimax
from slack_board_display import SlackBoardDisplay


#can run only one game concurrently
#think about how to run in another channel vs. #chess only

class Slack:

    def __init__(self):
        self.client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
        self.game = None
        self.names_of_players = []
        self.game_mode = None
        self.slack_board_display = SlackBoardDisplay()

    def post(self, client, text, channel = '#chess'):
        output = client.chat_postMessage(
            channel = channel,
            text = text,
            # icon_emoji=':dart:',
            as_user = True)

    def start_listen(self):
        self.post(self.client, self.__intro_chessy())
        @slack.RTMClient.run_on(event='message')
        def run_game(**payload):
            data = payload['data']
            web_client = payload['web_client']
            rtm_client = payload['rtm_client']
            self.__check_for_start(web_client, data)
            self.__check_for_moves(web_client, data)
            self.__check_for_stop(web_client, data)
            self.__check_for_mode(web_client, data)
            self.__check_for_mode_set(web_client, data)
            self.__check_for_join(web_client, data)
            self.__check_for_AI(web_client, data)

        slack_token = os.environ["SLACK_API_TOKEN"]
        rtm_client = slack.RTMClient(token=slack_token)
        rtm_client.start()

    # private methods

    def __check_for_start(self, web_client, data):
        if data.get('text', []) == 'start' and data.get('bot_id') == None and self.game == None:
            print(data)
            self.names_of_players = [data['user']]
            self.post(web_client, f" <@{data['user']}> wants to play! Enter join to start the game!")

    def __check_for_join(self, web_client, data):
        if data.get('text', []) == 'join' and data.get('bot_id') == None and len(self.names_of_players) == 1:
            print(data)
            self.names_of_players.append(data['user'])
            if self.game_mode not in [None, 'in_choosing']:
                self.__launch_game(web_client, self.names_of_players[0], self.names_of_players, ruleset = self.game_mode)
            else:
                self.__launch_game(web_client, self.names_of_players[0], self.names_of_players)

    def __check_for_AI(self, web_client, data):
        if data.get('text', []) == 'AI please!' and data.get('bot_id') == None and len(self.names_of_players) == 1:
            print(data)
            self.names_of_players.append('AI')
            self.__launch_game(web_client, self.names_of_players[0], self.names_of_players, ruleset = self.game_mode)

    def __check_for_mode(self, web_client, data):
        if data.get('text', []) == "let's make this more interesting!" and len(self.names_of_players) == 1 and data['user'] in self.names_of_players:
            self.game_mode = 'in_choosing'
            self.post(web_client, f" Ok <@{data['user']}>! Make your choice:")
            self.post(web_client, ' - Can I play daddy?')
            self.post(web_client, ' - Piece of cake')
            self.post(web_client, " - Damn I'm good")

    def __check_for_mode_set(self, web_client, data):
        if data.get('text', []) == "Can I play daddy?" and len(self.names_of_players) == 1 and data['user'] in self.names_of_players:
            self.game_mode = 'many_queens'
            self.post(web_client, 'Yes you can!')
        if data.get('text', []) == "Piece of cake" and len(self.names_of_players) == 1 and data['user'] in self.names_of_players:
            self.game_mode = 'random_pieces'
            self.post(web_client, 'Pieces will be random, but not the cake (0)!')

    def __check_for_moves(self, web_client, data):
        if self.game != None and data.get('text', []) not in ['start', 'stop', 'join'] and data['user'] in self.names_of_players:
            print(data)
            if self.__correct_players_turn(data):
                try:
                    self.__parse_and_execute_move(web_client, data.get('text', []))
                except:
                    self.post(web_client, 'Invalid move - try again')
                self.__check_for_checkmate()
                self.post(web_client, self.slack_board_display.output_board(self.game))
            if self.game.player_2.name == 'AI' and self.game.p1_turn == False:
                self.__AI_move()
                self.__check_for_checkmate()
                self.post(web_client, self.slack_board_display.output_board(self.game))

    def __AI_move(self):
        AI_move = minimax.Minimax(self.game).minimax()
        print(AI_move)
        self.game.execute_turn(AI_move[0][0],AI_move[0][1],AI_move[1][0],AI_move[1][1])

    def __check_for_stop(self, web_client, data):
        if self.game != None and data.get('text', [])== 'stop' and data['user'] in self.names_of_players:
            print(data)
            self.post(web_client, 'Ok, stopped the game. Enter start to start a new game!')
            self.game = None
            self.names_of_players = []
            self.game_mode = None

    def __launch_game(self, web_client, user_launched_game, names, ruleset = 'standard'):
        self.game = game.Game(names[0], names[1], ruleset)
        self.post(web_client, f" <@{user_launched_game}> launched the game! Enter moves in this format: a2-a4")
        self.post(web_client, 'Enter stop to stop the game')
        self.post(web_client, f" <@{names[0]}> vs <@{names[1]}>")
        self.post(web_client, self.slack_board_display.output_board(self.game))

    def __parse_and_execute_move(self, web_client, text):
        turn_from = text.split('-')[0].lower()
        turn_to = text.split('-')[1].lower()
        move = coordinate_conversion.Convert().coordinates(turn_from, turn_to)
        if self.game.execute_turn(move[0],move[1],move[2],move[3]) == 'invalid move':
            self.post(web_client, 'Invalid move - try again')

    def __check_for_checkmate(self):
        if self.game.is_checkmate():
            if self.game.p1_turn:
              self.post(web_client, f"Checkmate, <@{self.game.player_2.name}> wins!")
            elif self.game.p1_turn == False:
              self.post(web_client, f"Checkmate, <@{self.game.player_1.name}> wins!")
            self.game = None

    def __correct_players_turn(self, data):
        if self.game.p1_turn:
            if data['user'] == self.game.player_1.name:
                return True
        else:
            if data['user'] == self.game.player_2.name:
                return True
        return False

    def __intro_chessy(self):
        output = 'Hi I am Chessy!\n'
        output += 'Let others play their games, the game of kings is still the ♔ of games!\n'
        output += 'Enter start to start the game!\n'
        return output

slack_instance = Slack()
slack_instance.start_listen()
