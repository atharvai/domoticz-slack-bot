import json
from datetime import datetime
from slackclient import SlackClient
import argparse
import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('bot.config')

slack_client = ''

epoch = datetime.utcfromtimestamp(0)

priority_colours = {
    'normal': 'good',
    'high': 'danger'
}

def generate_attachment(title, priority, text, ts):
    attachments = [{'title':title,
                    'color':priority_colours[priority],
                    'text':text,
                    'fallback':text,
                    'ts':(datetime.utcnow()-epoch).total_seconds()  if ts is None else ts
                    }]
    return json.dumps(attachments)

def generate_table_attachment(title, priority, data, fallback):
    fields = []
    attachments = []

    for d in data:
        field = [{'title':'Sensor', 'value': str(d['Name']), 'short': 'true'},
                {'title':'Value', 'value': str(d['Data']), 'short': 'true'},
                {'title':'Last Update', 'value': str(d['LastUpdate']), 'short': 'true'},
                 ]
        attachment = {'title':title,
                    'color':priority_colours[priority],
                    'fallback':fallback,
                    'fields': field
                    }
        attachments.append(attachment)

    return json.dumps(attachments)

def post_slack_message(channel, attachment):
    slack_client.api_call("chat.postMessage", channel=channel,
                          as_user=True,
                          attachments=attachment,
                          )

def datetime_to_ts(dt):
    if isinstance(dt,datetime):
        return (dt - epoch).total_seconds()
    raise Exception('dt must be of type datetime')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--priority', default='high')
    parser.add_argument('--message')
    parser.add_argument('--channel', default='#general')

    args = parser.parse_args()

    priority=args.priority
    channel=args.channel
    message=args.message

    slack_client = SlackClient(config.get('slack','token'))

    if message is None:
        print('No message specified')
        sys.exit(1)

    post_slack_message(channel,generate_attachment('Sensor Triggered', priority, message))