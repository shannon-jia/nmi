#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Blueprint
from sanic.response import json
from .parse import Parse
from sanic.exceptions import InvalidUsage


bp = Blueprint(__name__)
parse = Parse()


@bp.route('/', methods=['GET'])
async def get_controls(request):
    args = request.raw_args
    try:
        if not args:
            x_list = parse.get_all(bp.site.control_list)
            return json(x_list)
        x_dict = parse.get_one(args, bp.site.control_list)
        if not x_dict:
            return json({'error': 'Parameter is wrong.'}, status=404)
        return json(x_dict)
    except Exception as e:
        return json({
            "error": e.args or e
        })
