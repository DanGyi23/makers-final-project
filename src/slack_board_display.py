from piece import Piece
import board_render


class SlackBoardDisplay:

    def render_board(self, game, web_client, channel):
        self.post(web_client, self.__announce_whose_turn(game), channel)
        board_render.BoardRender(game).draw_board()
        web_client.files_upload(
            channels = channel,
            file = 'output.png',
            title = 'Board',
            username = 'Chessy'
        )
        if self.__list_taken_pieces_ifany(game) != '\n': self.post(web_client, self.__list_taken_pieces_ifany(game), channel)

    # output_board can be used to show a text-based board. use: self.post(web_client, self.slack_board_display.output_board(self.game))

    def output_board(self, game):
        output = self.__announce_whose_turn(game)
        output +='\n\n\n'
        output += f"<@{game.player_2.name}>\n"
        output += "| A | B | C | D | E | F | G | H |\n"
        output += '________________________\n'
        ind = 8
        for row in game.board:
            x = "|"
            for el in row:
                if isinstance(el, Piece):
                    x += f" {el.symbol} |"
                else:
                    x += f" {el}  |"
            x += f" {ind}"
            ind -= 1
            output += f"{x}\n"
            output += '------------------------------\n'
        output += f"<@{game.player_1.name}>\n"
        output += '\n'
        output += self.__list_taken_pieces_ifany(game)
        return output

    def post(self, client, text, channel):
        output = client.chat_postMessage(
            channel = channel,
            text = text,
            username = 'Chessy')
            # as_user = True)

    # private

    def __announce_whose_turn(self, game):
        if game.p1_turn == True:
            return f"<@{game.player_1.name}>" + "'s turn!"
        else:
            return f"<@{game.player_2.name}>" + "'s turn!"

    def __list_taken_pieces_ifany(self, game):
        output = '\n'
        if len(game.player_2.taken_pieces) > 0:
            output += 'Taken:'
            for el in game.player_2.taken_pieces:
                output += f" {el.symbol}"
            output += '\n'
        if len(game.player_1.taken_pieces) > 0:
            output += 'Taken:'
            for el in game.player_1.taken_pieces:
                output += f" {el.symbol}"
            output += '\n'
        return output
