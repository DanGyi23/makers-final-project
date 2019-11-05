import os
import slack
import coordinate_conversion
import game
from io import StringIO
import sys
import minimax
from slack_board_display import SlackBoardDisplay
from slack_control import SlackControl


#can run only one game concurrently
#think about how to run in another channel vs. #chess only

class Slack:

    def __init__(self):
        self.client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
        self.slack_control = SlackControl()

    def post(self, client, text, channel = '#chess'):
        output = client.chat_postMessage(
            channel = channel,
            text = text,
            as_user = True)

    def start_listen(self):
        self.post(self.client, self.__intro_chessy())
        @slack.RTMClient.run_on(event='message')
        def run_game(**payload):
            data = payload['data']
            web_client = payload['web_client']
            rtm_client = payload['rtm_client']
            self.slack_control.check_for_start(web_client, data)
            self.slack_control.check_for_moves(web_client, data)
            self.slack_control.check_for_stop(web_client, data)
            self.slack_control.check_for_mode(web_client, data)
            self.slack_control.check_for_mode_set(web_client, data)
            self.slack_control.check_for_join(web_client, data)
            self.slack_control.check_for_AI(web_client, data)

        slack_token = os.environ["SLACK_API_TOKEN"]
        rtm_client = slack.RTMClient(token=slack_token)
        rtm_client.start()

    # private methods

    def __intro_chessy(self):
        output = 'Hi I am Chessy!\n'
        output += 'Let others play their games, the game of kings is still the ♔ of games!\n'
        output += 'Enter start to start the game!\n'
        return output


slack_instance = Slack()
slack_instance.start_listen()
