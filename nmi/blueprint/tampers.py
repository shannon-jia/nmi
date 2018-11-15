#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Blueprint
from sanic.response import json
from .parse import Parse
from sanic.exceptions import InvalidUsage


bp = Blueprint(__name__)
parse = Parse()


@bp.route('/', methods=['GET'])
async def get_tampers(request):
    args = request.raw_args
    try:
        if not args:
            x_list = parse.get_all(bp.site.sensor_tamper)
            return json(x_list)
        x_dict = parse.get_one(args, bp.site.sensor_tamper)
        if not x_dict:
            return json({'error': 'Parameter is wrong.'}, status=404)
        return json(x_dict)
    except Exception as e:
        return json({
            "error": e.args or e
        })


@bp.route('/', methods=['PATCH'])
async def set_tamper(request):
    try:
        params = request.json
        if not params:
            return json({
                "Error": "Please enter parameters"
            })
        x_list = parse.patch(params, bp.site.alarms, bp.site.sensor_tamper)
        if not x_list:
            return json({'error': 'Parameter is wrong'}, status=404)
        return json(x_list)
    except InvalidUsage:
        params = request.form
        x_dict = parse.convert(params)
        x_list = parse.patch(x_dict, bp.site.alarms, bp.site.sensor_alarm)
        if not x_list:
            return json({'error': 'Parameter is wrong'}, status=404)
        return json(x_list)
    except Exception as e:
        return json({
            'error': e.args or e
        })
