from datetime import datetime

from slack.slack_helper import datetime_to_ts, generate_attachment


def process(domo, cmd):
    if cmd == 'list':
        data = sorted(map(lambda d: d['Name'], domo.device_list))
        attachment = generate_attachment('Device List', 'neutral', '\n'.join(data),
                                         datetime_to_ts(datetime.utcnow()))
        return attachment
    elif cmd.startswith('toggle'):
        dev_name = cmd.split(' ', 1)[1]
        result = domo.toggle_light_switch(dev_name)
        return result
    elif 'on' in cmd.lower() or 'off' in cmd.lower():
        dev_name, swt_cmd = cmd.split(' ', 1)
        result = domo.toggle_light_switch(name=dev_name, swt_cmd=swt_cmd.title())
        return result
    elif cmd.startswith('dim'):
        _, dev_name, level = cmd.split(' ', 2)
        return 'I don''t yet know how to dim a light.'

