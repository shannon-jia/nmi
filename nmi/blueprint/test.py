device_types = [
    {
        "PLC_430": {
            "diags": 0,
            "alarms": 8,
            "controls": 8
        }

    },
    {
        "PLC_410": {
            "diags": 0,
            "alarms": 64,
            "controls": 128
        }
    }
]

k = "PLC_430"
for i in device_types:
    if k in i:
        print(i.get(k)["alarms"])
    else:
        print('False')
