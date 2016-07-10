import json
import time
from slackclient import SlackClient
from datetime import datetime
import ConfigParser
from domoticz import domoticz
from slack_notify import SlackNotify
from commands import commands, command_groups

config = ConfigParser.ConfigParser()
config.read('bot.config')

BOT_ID = config.get('slack', 'bot_id')

# constants
AT_BOT = "<@" + BOT_ID + ">:"

# instantiate Slack & Twilio clients
slack_client = SlackClient(config.get('slack', 'token'))
slack_notify = SlackNotify(config.get('slack', 'token'))
domo = domoticz.Domoticz(config.get('domoticz', 'host'))


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
            if cmd in commands[command_grp]:
                data = domo.get_device_status_many(cmd)
                get_domoticz_status(channel, data)
        elif command_grp == 'device':
            if cmd in commands[command_grp]:
                data = sorted(domo.device_id_map.keys())
                attachment = slack_notify.generate_attachment('Device List','neutral', '\n'.join(data), slack_notify.datetime_to_ts(datetime.utcnow()))
                slack_notify.post_slack_message(channel, attachment)
        elif command_grp == 'temp':
            get_domoticz_temp(channel, cmd)
    else:
        slack_notify.post_slack_message_plain(channel, '')


def parse_command(slack_output):
    parsed = slack_output.split(' ',1)
    try:
        parsed[1] = int(parsed[1])
    finally:
        if len(parsed) == 1:
            parsed = parsed + ['']
        return parsed

def get_domoticz_temp(channel, name):
    if name == '' or name == 'all':
        data = domo.get_device_status_many('temp')
        get_domoticz_status(channel, data)
    else:
        devices = filter(lambda k: name.lower() in k['Name'].lower(), domo.device_list_by_type['Temp'])
        if len(devices) == 0:
            slack_notify.post_slack_message_plain(channel, 'Device _{dev}_ not found'.format(dev=name))
            return

        idx = devices[0]['idx']
        data = domo.get_device_data(idx=idx)
        data = data[0]
        ts = slack_notify.datetime_to_ts(datetime.strptime(data['LastUpdate'], '%Y-%m-%d %H:%M:%S'))
        attachment = slack_notify.generate_attachment(data['Name'], 'normal', data['Data'], ts)
        slack_notify.post_slack_message(channel, attachment)


def get_domoticz_status(channel, data):
    attachments = slack_notify.generate_table_attachment('Device Status', 'normal', data, 'Device Status Update')
    slack_notify.post_slack_message(channel, attachments)


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
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print('Connection failed. Invalid Slack token or bot ID?')
