devices = {
    'all': {'type':'devices','filter':'all','used':'true','order':'Name'},
    'light': {'type':'devices','filter':'light','used':'true','order':'Name'},
    'temp': {'type':'devices','filter':'temp','used':'true','order':'Name'},
    'utility': {'type':'devices','filter':'utility','used':'true','order':'Name'},
    'weather': {'type':'devices','filter':'weather','used':'true','order':'Name'},
    'favourite': {'type':'devices','filter':'all','used':'true','order':'Name','favorite':1},
    'byIdx': {'type':'devices','rid':-1},
    'toggleLightSwitch': {'type':'command','param':'switchlight','switchcmd':'Toggle','idx':-1},
}

command = {
    'sunriseset': {'type':'command','param':'getSunRiseSet'},
}

uservariable_type = {
    'Integer': 0,
    'Float': 1,
    'String': 2,
    'Date': 3,
    'Time': 4
}

uservariables = {
    'save': {'type':'command','param':'saveuservariable','vname':'','vtype':-1,'vvalue':''},
    'update': {'type':'command','param':'updateuservariable','vname':'uservariablename','vtype':-1,'vvalue':'uservariablevalue'},
    'all': {'type':'command','param':'getuservariables'},
    'delete': {'type':'command','param':'deleteuservariable','idx': -1},
    'byIdx': {'type':'command','param':'getuservariable','idx': -1},
}
