from datetime import datetime

from slack.slack_helper import generate_attachment, datetime_to_ts


def process(domo, cmd, req_var):
    msg_type = 'attachment'
    if cmd == 'all':
        data = map(lambda v: v['Name'], domo.get_all_variables())
        attachment = generate_attachment('User Variable List', 'neutral', '\n'.join(data),
                                         datetime_to_ts(datetime.utcnow()))
        return msg_type, attachment
    elif cmd == 'get':
        is_idx = False
        data = None
        try:
            int(req_var[1])
            is_idx = True
        except:
            is_idx = False
        if is_idx:
            data = domo.get_user_variable(idx=req_var[1])
        else:
            data = domo.get_user_variable(name=req_var[1])
        if data is not None:
            attachment = generate_attachment('User Variable: {id}'.format(id=req_var[1]), 'neutral', data,
                                             datetime_to_ts(datetime.utcnow()))
        else:
            msg_type = 'plain'
            attachment = 'Variable `{}` not found'.format(req_var[1])
        return msg_type, attachment
    elif cmd == 'set':
        vtype, name, value = req_var[1].split(' ')
        var_type = domo.get_user_variable_type_id(vtype)
        if var_type is not None:
            status = domo.create_or_update_user_variable(name, value, var_type)
            if status['title'] == 'UpdateUserVariable' and status['status'] == 'OK':
                status = 'User variable update successful'
            elif status['title'] == 'CreatUserVariable' and status['status'] == 'OK':
                status = 'User variable created successful'
            else:
                status = status['status']
        else:
            status = 'Variable type {} not recognised. Valid types are: int, integer, float, str, string, date, time'.format(
                    vtype)
        msg_type = 'plain'
        return msg_type, status
    elif cmd == 'delete':
        var = req_var[1]
        is_idx = False
        try:
            idx = int(var)
            is_idx = True
        except:
            is_idx = False
        if is_idx:
            status = domo.delete_user_variable(idx=var)
        else:
            status = domo.delete_user_variable(name=var)

        msg_type = 'plain'
        if status is None:
            status = 'Variable `{}` not found'.format(var)
        return msg_type, status
