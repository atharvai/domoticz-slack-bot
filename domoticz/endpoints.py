devices = {
        'all': {'type':'devices','filter':'all','used':'true','order':'Name'},
        'light': {'type':'devices','filter':'light','used':'true','order':'Name'},
        'temp': {'type':'devices','filter':'temp','used':'true','order':'Name'},
        'utility': {'type':'devices','filter':'utility','used':'true','order':'Name'},
        'weather': {'type':'devices','filter':'weather','used':'true','order':'Name'},
        'favourite': {'type':'devices','filter':'all','used':'true','order':'Name','favorite':1},
        'byIdx': {'type':'devices','rid':-1},
}

command = {
        'sunriseset': {'type':'command','param':'getSunRiseSet'},
}
