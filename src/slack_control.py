import os
import slack
import coordinate_conversion
import game
import minimax
from slack_board_display import SlackBoardDisplay

class SlackControl:

    def __init__(self, channel):
        self.game = None
        self.names_of_players = []
        self.game_mode = None
        self.slack_board_display = SlackBoardDisplay()
        self.channel = channel

    def intro_chessy(self, web_client):
        self.post(web_client, self.__intro_chessy_text())

    def check_for_start(self, web_client, data):
        if data.get('text', []) == 'start' and data.get('bot_id') == None and self.game == None:
            self.names_of_players = [data['user']]
            self.post(web_client, f" <@{data['user']}> wants to play! Enter join to start the game!")

    def check_for_join(self, web_client, data):
        if data.get('text', []) == 'join' and data.get('bot_id') == None and len(self.names_of_players) == 1:
            self.names_of_players.append(data['user'])
            if self.game_mode not in [None, 'in_choosing']:
                self.__launch_game(web_client, self.names_of_players[0], self.names_of_players, ruleset = self.game_mode)
            else:
                self.__launch_game(web_client, self.names_of_players[0], self.names_of_players)

    def check_for_AI(self, web_client, data):
        if data.get('text', []) == 'AI please!' and data.get('bot_id') == None and len(self.names_of_players) == 1:
            print(data)
            self.names_of_players.append('AI')
            self.__launch_game(web_client, self.names_of_players[0], self.names_of_players, ruleset = self.game_mode)

    def check_for_mode(self, web_client, data):
        if data.get('text', []) == "let's make this more interesting!" and len(self.names_of_players) == 1 and data.get('user',[]) in self.names_of_players:
            self.game_mode = 'in_choosing'
            self.__announce_game_modes(web_client, data['user'])

    def check_for_mode_set(self, web_client, data):
        self.__mode_set(web_client, data, "Can I play daddy?", 'many_queens', 'Yes you can!')
        self.__mode_set(web_client, data, "Piece of cake", 'random_pieces', 'Pieces will be random, but not the cake (0)!')
        self.__mode_set(web_client, data, "Damn I'm good", 'ex_bishops', 'Anarchy in the UK!')

    def check_for_moves(self, web_client, data):
        if self.game != None and data.get('text', []) not in ['start', 'stop', 'join'] and data.get('user',[]) in self.names_of_players:
            if self.__correct_players_turn(data):
                try:
                    self.__parse_and_execute_move(web_client, data.get('text', []))
                except:
                    self.post(web_client, 'Invalid move - try again')
                self.__check_for_checkmate()
                self.slack_board_display.render_board(self.game, web_client, self.channel)
            if self.game.player_2.name == 'AI' and self.game.p1_turn == False:
                self.__AI_move()
                self.__check_for_checkmate()
                self.slack_board_display.render_board(self.game, web_client, self.channel)

    def check_for_stop(self, web_client, data):
        if self.game != None and data.get('text', [])== 'stop' and data['user'] in self.names_of_players:
            self.post(web_client, 'Ok, stopped the game. Enter start to start a new game!')
            self.game = None
            self.names_of_players = []
            self.game_mode = None

    def post(self, client, text):
        output = client.chat_postMessage(
            channel = self.channel,
            text = text,
            username = 'Chessy')

    # private methods

    def __mode_set(self, web_client, data, text_to_look_for, mode_text, response_text):
        if data.get('text', []) == text_to_look_for and len(self.names_of_players) == 1 and data.get('user',[]) in self.names_of_players:
            self.game_mode = mode_text
            self.post(web_client, response_text)

    def __launch_game(self, web_client, user_launched_game, names, ruleset = 'standard'):
        self.game = game.Game(names[0], names[1], ruleset)
        self.__announce_start(web_client, user_launched_game, names)
        self.slack_board_display.render_board(self.game, web_client, self.channel)

    def __parse_and_execute_move(self, web_client, text):
        turn_from = text.split('-')[0].lower()
        turn_to = text.split('-')[1].lower()
        move = coordinate_conversion.Convert().coordinates(turn_from, turn_to)
        response = self.game.execute_turn(move[0],move[1],move[2],move[3])
        print(f"response {response}")
        self.__post_response(web_client, response)

    def __post_response(self, web_client, response):
        response_mapping = {
            'invalid move': 'Invalid move - try again',
            'excommunication': 'Oh no! bishops were excommunicated!',
            'rooksale': "Oh no! rooks were sold off! They can't move for 5 turns, while the transaction completes.",
            'rooksign': 'Sale complete! All Rooks can move again.',
            'knight_honour': 'Knights receive the hightest honour! They can now move in any direction, for 2 turns.',
            'knight_normal': 'The fun has worn off! Knights can no longer move in any direction'
            }
        if response != 'valid move':
            self.post(web_client, response_mapping.get(response, ''))

    def __AI_move(self):
        AI_move = minimax.Minimax(self.game).minimaxRoot(2, self.game.board, True)
        print(AI_move)
        self.game.execute_turn(AI_move[0][0],AI_move[0][1],AI_move[1][0],AI_move[1][1])

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

    def __announce_start(self, web_client, user_launched_game, names):
        self.post(web_client, f" <@{user_launched_game}> launched the game! Enter moves in this format: a2-a4")
        self.post(web_client, 'Enter stop to stop the game')
        self.post(web_client, f" <@{names[0]}> vs <@{names[1]}>")

    def __announce_game_modes(self, web_client, user):
        self.post(web_client, f" Ok <@{user}>! Make your choice:")
        self.post(web_client, ' - Can I play daddy?')
        self.post(web_client, ' - Piece of cake')
        self.post(web_client, " - Damn I'm good")

    def __intro_chessy_text(self):
        output = 'Hi I am Chessy!\n'
        output += 'Let others play their games, the game of kings is still the ♔ of games!\n'
        output += 'Enter start to start the game!\n'
        return output
