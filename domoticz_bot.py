import ConfigParser
import time

from commands import cmd_uservar, cmd_device, cmd_status
from commands.commands import commands, command_groups
from domoticz import domoticz
from slack.slack_helper import generate_attachment_custom_fields
from slack.slack_notify import SlackNotify
from slackclient import SlackClient

INTRO_MSG = 'How can I help?'
HELP_MSG = 'I didn''t quite understand that.' + '\n' + INTRO_MSG

config = ConfigParser.ConfigParser()
config.read('bot.config')

BOT_ID = config.get('slack', 'bot_id')

# constants
AT_BOT = "<@" + BOT_ID + ">:"

# instantiate Slack clients
slack_client = SlackClient(config.get('slack', 'token'))
slack_notify = SlackNotify(config.get('slack', 'token'))
domo = domoticz.Domoticz(config.get('domoticz', 'host'))
domo._cache_device_list()


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
        :param channel:
        :param command:
    """
    response = 'Not sure what you mean. Sample commands to try `status all`, `status temp`, `temp`'
    command_grp, cmd = parse_command(command)
    if command_grp in command_groups:
        if cmd == '' and (len(commands[command_grp]) == 0 or 'all' in commands[command_grp]):
            cmd = 'all'

        if command_grp == 'status':
            msg = cmd_status.process(domo, cmd, command_grp)
            slack_notify.post_slack_message(channel, msg)
        elif command_grp == 'device':
            if cmd in commands[command_grp]:
                msg = cmd_device.process(domo, cmd)
                if msg is not None:
                    slack_notify.post_slack_message(channel, msg)
            else:
                post_help_msg(channel)
        elif command_grp == 'sunriseset':
            data = domo.get_sunriseset()
            if 'title' in data:
                data.pop('title')
            if 'status' in data:
                data.pop('status')
            attachment = generate_attachment_custom_fields('SunRise & SunSet', 'neutral', data, 'SunRiseSet')
            slack_notify.post_slack_message(channel, attachment)
        elif command_grp == 'uservar':
            req_var = None
            if ' ' in cmd:
                req_var = cmd.split(' ', 1)
                cmd = req_var[0]
            if cmd in commands[command_grp]:
                msg = cmd_uservar.process(domo, cmd, req_var)
                if msg.startswith('[{'):
                    slack_notify.post_slack_message(channel, msg)
                else:
                    slack_notify.post_slack_message_plain(channel, msg)
            else:
                post_help_msg(channel)
        else:
            post_help_msg(channel)
    else:
        post_help_msg(channel)


def post_help_msg(channel):
    slack_notify.post_slack_message_plain(channel, HELP_MSG)


def parse_command(slack_output):
    parsed = slack_output.split(' ', 1)
    try:
        parsed[1] = int(parsed[1])
    finally:
        if len(parsed) == 1:
            parsed = parsed + ['']
        return parsed


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
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print('DomoticzBot connected and running!')
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            else:
                slack_notify.post_slack_message_plain(channel, INTRO_MSG)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')
