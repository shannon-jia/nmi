#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic.response import json

class Parse:
    def __init__(self):
        pass

    def get_all(self, alarm_list):
        x_list = []
        j = 0
        for i in alarm_list:
            x_dict = {}
            j += 1
            x_dict['id'] = j
            x_dict['status'] = i
            x_dict['desc'] = f'The state of {j} point is {i}.'
            x_list.append(x_dict)
        return x_list

    def get_one(self, args, alarm_list):
        id = args.get('id', 0)
        if not id:
            return
        if len(args) > 1:
            return
        if not id.isdigit():
            return
        j = 0
        x_dict = {}
        for i in alarm_list:
            j += 1
            if int(id) == j:
                x_dict["id"] = j
                x_dict["status"] = i
                x_dict["desc"] = f'The state of {j} point is {i}.'
        return x_dict

    def patch(self, param, alarms, alarm_list):
        if isinstance(param, dict):
            param = [param]
        x_list = []
        for i in param:
            x_dict = {}
            id = i.get("id", 0)
            status = i.get("status", "").upper()
            if not id or id < 1 or id > alarms or not status:
                continue
            if status not in ("ALARM", "NORMAL"):
                continue
            x_dict['id'] = id
            x_dict['status'] = status
            x_dict['desc'] = f'The state of {id} point is {status}.'
            x_list.append(x_dict)
            alarm_list[id-1] = status
        return x_list

    def convert(self, params):
        x_dict = {}
        for k, v in params.items():
            if k in ('name', 'status'):
                x_dict[k] = v[0]
            if not v[0].isdigit():
                continue
            x_dict[k] = int(v[0])
        return x_dict



if __name__ == "__main__":
    pass
