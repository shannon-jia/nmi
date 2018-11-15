#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Blueprint
from sanic.response import json
from sanic.exceptions import InvalidUsage
from .parse import Parse


bp = Blueprint(__name__)
parse = Parse()

@bp.route('/', methods=['GET'])
async def get_device(request):
    return json({
        "device": bp.site.device,
        "diags": bp.site.diags,
        "alarms": bp.site.alarms,
        "controls": bp.site.controls
    })


@bp.route('/', methods=['PATCH'])
async def set_device(request):
    try:
        params = request.json
        if not params:
            return json({"Error": "Please enter parameters"}, status=404)
        x_dict = patch(params)
        if not x_dict:
            return json({'error': 'Parameter is wrong.'}, status=404)
        return json(x_dict)
    except InvalidUsage as e:
        params = request.form
        x_dict = parse.convert(params)
        res = patch(x_dict)
        if not res:
            return json({'error': 'Parameter is wrong.'}, status=404)
        return json(res)
    except Exception as e:
        return json({'error': e})

def patch(params):
    x_dict = {}
    name = params.get("name", "")
    if isinstance(name, int):
        return
    if not name:
        return
    if len(params) > 1:
        return
    for i in bp.site.device_types:
        if name.upper() == i.get("name"):
            bp.site.device = x_dict["name"] = i.get("name")
            bp.site.diags = x_dict["diags"] = i.get("diags")
            bp.site.alarms = x_dict["alarms"] = i.get("alarms")
            bp.site.controls = x_dict["controls"] = i.get("controls")
            bp.site.sensor_alarm = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.sensor_tamper = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.filter_alarm = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.filter_tamper = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.shunt_alarm = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.shunt_tamper = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.pre_alarm = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.trbl_alarm = ['NORMAL' for i in range(bp.site.alarms)]
            bp.site.control_list = ['NORMAL' for i in range(bp.site.controls)]
    return x_dict
