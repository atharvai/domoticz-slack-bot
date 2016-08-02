import shlex

NOT_FOUND_MSG = 'Device `{}` not found'


def process(domo, command_str):
    tokens = shlex.split(command_str)
    if len(tokens) > 0:
        if tokens[0] == 'refresh':
            try:
                domo._cache_device_list()
                return 'plain', 'System refresh completed successfully'
            except:
                return 'plain', 'System refresh failed'
    return 'plain', 'I didn''t understand what you want me to do'
