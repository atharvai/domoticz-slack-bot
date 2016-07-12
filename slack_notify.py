import json
from datetime import datetime
from slackclient import SlackClient
import argparse
import sys
import ConfigParser


class SlackNotify:
    slack_client = ''

    epoch = datetime.utcfromtimestamp(0)

    colours = {
        'neutral': '#3366ff',
        'normal': 'good',
        'high': 'danger',
        'red': 'danger',
        'green': 'good'
    }

    def __init__(self, token):
        self.slack_client = SlackClient(token)

    def generate_attachment(self, title, priority, text, ts):
        attachments = [{'title': title,
                        'color': self.colours[priority],
                        'text': text,
                        'fallback': text,
                        'ts': (datetime.utcnow() - self.epoch).total_seconds() if ts is None else ts
                        }]
        return json.dumps(attachments)

    def generate_table_attachment(self, title, priority, data, fallback):
        fields = []
        attachments = []

        for d in data:
            field = [{'title': 'Sensor', 'value': str(d['Name']), 'short': 'true'},
                     {'title': 'Value', 'value': str(d['Data']), 'short': 'true'},
                     {'title': 'Last Update', 'value': str(d['LastUpdate']), 'short': 'true'},
                     ]
            attachment = {'title': title,
                          'color': self.colours[priority],
                          'fallback': fallback,
                          'fields': field
                          }
            attachments.append(attachment)

        return json.dumps(attachments)

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

    def datetime_to_ts(self, dt):
        if isinstance(dt, datetime):
            return (dt - self.epoch).total_seconds()
        raise Exception('dt must be of type datetime')


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
    ts = slack_notify.datetime_to_ts(datetime.utcnow())
    attachment = slack_notify.generate_attachment('Sensor Triggered', priority, message, ts)
    slack_notify.post_slack_message(channel, attachment)
