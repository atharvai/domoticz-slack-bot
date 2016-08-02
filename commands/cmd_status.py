import shlex
from datetime import datetime

from commands import commands
from slack.slack_helper import generate_table_attachment, generate_attachment, datetime_to_ts

NOT_FOUND_MSG = 'Device `{}` not found'


def get_domoticz_status(data):
    attachments = generate_table_attachment('Device Status', 'neutral', data, 'Device Status Update')
    return attachments


def get_device_status(domo, name):
    devices = filter(lambda k: name.lower() in k.lower(), domo.device_names)
    if len(devices) == 0:
        return None

    idx = domo.device_id_map[devices[0].lower()]
    data = domo.get_device_data(idx=idx)
    data = data[0]
    ts = datetime_to_ts(datetime.strptime(data['LastUpdate'], '%Y-%m-%d %H:%M:%S'))
    attachment = generate_attachment(data['Name'], 'neutral', data['Data'], ts)
    return attachment


def process(domo, cmd, command_grp):
    if cmd.startswith("'"):
        tokens = shlex.split(cmd)
        cmd = tokens[0]
    result = None
    if cmd in commands[command_grp]:
        data = domo.get_device_status_many(cmd)
        if data is not None:
            result = get_domoticz_status(data)
    else:
        result = get_device_status(domo, cmd)

    if result is None:
        return 'plain', NOT_FOUND_MSG.format(cmd)
    return 'attachment', result
