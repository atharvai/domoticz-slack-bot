import ConfigParser
import argparse
import sys
from datetime import datetime

from slack.slack_helper import datetime_to_ts, generate_attachment
from slackclient import SlackClient


class SlackNotify:
    slack_client = ''

    def __init__(self, token):
        self.slack_client = SlackClient(token)

    def post_slack_message(self, channel, attachment):
        self.slack_client.api_call('chat.postMessage', channel=channel,
                                   as_user=True,
                                   attachments=attachment,
                                   )

    def post_slack_message_plain(self, channel, text):
        self.slack_client.api_call('chat.postMessage', channel=channel,
                                   as_user=True,
                                   text=text,
                                   )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--priority', default='high')
    parser.add_argument('--message')
    parser.add_argument('--channel', default='#general')

    args = parser.parse_args()

    priority = args.priority
    channel = args.channel
    message = args.message

    config = ConfigParser.ConfigParser()
    config.read('bot.config')

    slack_client = SlackClient(config.get('slack', 'token'))

    if message is None:
        print('No message specified')
        sys.exit(1)

    slack_notify = SlackNotify(config.get('slack', 'token'))
    ts = datetime_to_ts(datetime.utcnow())
    attachment = generate_attachment('Sensor Triggered', priority, message, ts)
    slack_notify.post_slack_message(channel, attachment)
