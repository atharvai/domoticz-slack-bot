import json
from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

colours = {
    'neutral': '#3366ff',
    'normal': 'good',
    'high': 'danger',
    'red': 'danger',
    'green': 'good'
}


def generate_attachment(title, priority, text, ts):
    attachments = [{'title': title,
                    'color': colours[priority],
                    'text': text,
                    'fallback': text,
                    'ts': (datetime.utcnow() - epoch).total_seconds() if ts is None else ts
                    }]
    return json.dumps(attachments)


def generate_table_attachment(title, priority, data, fallback):
    fields = []
    attachments = []

    for d in data:
        field = [{'title': 'Sensor', 'value': str(d['Name']), 'short': 'true'},
                 {'title': 'Value', 'value': str(d['Data']), 'short': 'true'},
                 {'title': 'Last Update', 'value': str(d['LastUpdate']), 'short': 'true'},
                 ]
        attachment = {'title': title,
                      'color': colours[priority],
                      'fallback': fallback,
                      'fields': field
                      }
        attachments.append(attachment)

    return json.dumps(attachments)


def generate_attachment_custom_fields(title, priority, data, fallback):
    fields = []
    attachments = []

    for ftitle, value in data.iteritems():
        if ftitle == 'ServerTime':
            continue
        field = {'title': str(ftitle), 'value': str(value), 'short': 'true'}
        fields.append(field)
    attachment = {'title': title,
                  'color': colours[priority],
                  'fallback': fallback,
                  'fields': fields,
                  }
    if 'ServerTime' in data:
        attachment['ts'] = datetime_to_ts(datetime.strptime(data['ServerTime'], '%Y-%m-%d %H:%M:%S'))
    attachments.append(attachment)

    return json.dumps(attachments)


def datetime_to_ts(dt):
    if isinstance(dt, datetime):
        return (dt - epoch).total_seconds()
    raise Exception('dt must be of type datetime')
