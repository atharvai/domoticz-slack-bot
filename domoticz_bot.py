import json
import time
from slackclient import SlackClient
from datetime import datetime
import ConfigParser
from domoticz import domoticz
from slack_notify import generate_attachment, post_slack_message, datetime_to_ts, generate_table_attachment
from commands import commands

config = ConfigParser.ConfigParser()
config.read('bot.config')
# starterbot's ID as an environment variable
BOT_ID = config.get('slack','bot_id')

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient(config.get('slack','token'))

domo = domoticz.Domoticz(config.get('domoticz','host'))

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = 'Not sure what you mean. Use the *' + EXAMPLE_COMMAND + \
               '* command with numbers, delimited by spaces.'
    if command in commands:
        if command.startswith(EXAMPLE_COMMAND):
            response = "Sure...write some more code then I can do that!"
            post_slack_message(channel, response)
        elif command.startswith('temp'):
            get_domoticz_temp(channel)
        elif command == 'status':
            data = domo.get_device_status_many('temp')
            get_domoticz_status(channel, data)

def get_domoticz_temp(channel):
    data = domo.get_device_data(idx=5)
    post_slack_message(channel, generate_attachment(data['Name'], 'normal', data['Data'],
                                                    datetime_to_ts(datetime.strptime(data['LastUpdate'],'%Y-%m-%d %H:%M:%S'))))
def get_domoticz_status(channel, data):
    attachments = generate_table_attachment('Device Status','normal',data,'Device Status Update')
    post_slack_message(channel,attachments)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']

    return None, None

if __name__ == '__main__':
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('StarterBot connected and running!')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')
