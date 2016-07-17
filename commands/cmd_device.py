from datetime import datetime

from slack.slack_helper import datetime_to_ts, generate_attachment


def process(domo, cmd):
    if cmd == 'list':
        data = sorted(map(lambda d: d['Name'], domo.device_list))
        attachment = generate_attachment('Device List', 'neutral', '\n'.join(data),
                                         datetime_to_ts(datetime.utcnow()))
        return attachment
