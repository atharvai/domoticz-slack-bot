import shlex
from datetime import datetime

import cmd_status
from slack.slack_helper import datetime_to_ts, generate_attachment

NOT_FOUND_MSG = 'Device `{}` not found'


def process(domo, command_str):
    tokens = shlex.split(command_str)
    cmd = tokens[0]
    if len(tokens) == 2:
        if tokens[1].lower() == 'on' or tokens[1].lower() == 'off':
            cmd = tokens[1].lower()

    msg_type = 'plain'
    attachment = ''
    if cmd == 'list':
        data = sorted(domo.device_names)
        attachment = generate_attachment('Device List', 'neutral', '\n'.join(data),
                                         datetime_to_ts(datetime.utcnow()))
        msg_type = 'attachment'
    elif cmd == 'toggle':
        dev_name = tokens[1]
        result = domo.toggle_light_switch(dev_name)
        if result is not None:
            attachment = result
        else:
            attachment = NOT_FOUND_MSG.format(dev_name)
    elif 'on' == cmd or 'off' == cmd:
        dev_name, swt_cmd = tokens[0], cmd
        result = domo.toggle_light_switch(name=dev_name, swt_cmd=swt_cmd.title())
        if result is not None:
            attachment = result
        else:
            attachment = NOT_FOUND_MSG.format(dev_name)
    elif cmd == 'dim':
        dev_name, level = tokens[1], tokens[2]
        msg_type = 'plain'
        attachment = 'I don''t yet know how to dim a light.'
        result = domo.dim_light_switch(name=dev_name, level=level)
        if result is not None:
            attachment = result
        else:
            attachment = NOT_FOUND_MSG.format(dev_name)
    elif cmd == 'status':
        dev_name = tokens[1]
        result = cmd_status.process(domo, dev_name, 'status')
        if result is not None:
            msg_type = 'attachment'
            attachment = result
        else:
            attachment = NOT_FOUND_MSG.format(dev_name)

    return msg_type, attachment
