#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Blueprint
from sanic.response import json
from sanic.response import text
from sanic.exceptions import InvalidUsage
from .parse import Parse


bp = Blueprint(__name__)
parse = Parse()


@bp.route('/', methods=['GET'])
async def get_types(request):
    args = request.raw_args
    try:
        if not args:
            return json(bp.site.device_types)
        x_dict = deal_args(args)
        if not x_dict:
            return json({'error': 'Parameter is wrong.'}, status=404)
        return json(x_dict)
    except Exception as e:
        return json({
            "Error": e
        })

def deal_args(args):
    x_dict = {}
    id = args.get("id", 0)
    if not id:
        return
    if len(args) > 1:
        return
    if not id.isdigit():
        return
    for i in bp.site.device_types:
        if int(id) ==  i.get("id"):
            x_dict = i
    return [x_dict]


# @bp.route('/', methods=['DELETE'])
# async def delete_type(request):
#     args = request.raw_args
#     try:
#         if not args:
#             bp.site.device_types.clear()
#             return json({"device_types": bp.site.device_types})
#         x_dict = deal_args(args)
#         if not x_dict:
#             return json({'error': 'ID does not exist.'}, status=404)
#         bp.site.device_types.remove(x_dict)
#         return json(x_dict)
#     except Exception as e:
#         return json({
#             "error": e.args or e
#         })


# @bp.route('/', methods=['POST'])
# async def post_type(request):
#     try:
#         params = request.json
#         x_list = deal_params(params)
#         if not x_list:
#             return json({'error': 'ID and NAME cannot be duplicated or NAME cannot be empty'},
#                         status=404)
#         return json(x_list)
#     except InvalidUsage:
#         params = request.form
#         x_dict = parse.convert(params)
#         x_list = deal_params(x_dict)
#         if not x_list:
#             return json({'error': 'ID and NAME cannot be duplicated or NAME cannot be empty'},
#                         status=404)
#         return json(x_list)
#     except Exception as e:
#         return json({
#             "error": e.args or e
#         })


# @bp.route('/', methods=['PATCH'])
# async def patch_type(request):
#     try:
#         params = request.json
#         x_list = patch(params, bp.site.device_types)
#         if not x_list:
#             return json({'error': 'ID does not exist or NAME duplication'},
#                         status=404)
#         return json(x_list)
#     except InvalidUsage:
#         params = request.form
#         x_dict = parse.convert(params)
#         x_list = patch(x_dict, bp.site.device_types)
#         if not x_list:
#             return json({'error': 'ID does not exist or NAME duplication'},
#                         status=404)
#         return json(x_list)
#     except Exception as e:
#         return json({
#             "error": e
#         })


# def deal_params(params):
#     x_list = []
#     if isinstance(params, dict):
#         params = [params]
#     id_list = []
#     name_list = []
#     for i in bp.site.device_types:
#         id_list.append(i.get("id"))
#         name_list.append(i.get("name"))
#     for i in params:
#         x_dict = {}
#         id = i.get('id', 0)
#         name = i.get('name', '').upper()
#         diags = i.get('diags', 0)
#         alarms = i.get('alarms', 0)
#         controls = i.get('controls', 0)
#         if not isinstance(id, int) or not isinstance(diags, int) or not isinstance(alarms, int) or not isinstance(controls, int):
#             continue
#         if id in id_list or name in name_list or id < 1 or not name:
#             continue
#         x_dict["id"] = id
#         x_dict["name"] = name
#         x_dict["diags"] = diags
#         x_dict["alarms"] = alarms
#         x_dict["controls"] = controls
#         x_list.append(x_dict)
#         bp.site.device_types.append(x_dict)
#     return x_list

# def patch(params, types):
#     x_list = []
#     if isinstance(params, dict):
#         params = [params]
#     name_list = [i.get("name") for i in types]
#     for i in range(len(types)):
#         for j in params:
#             x_dict = {}
#             id = int(j.get("id", 0))
#             name = j.get("name", "").upper()
#             if id != types[i].get("id"):
#                 continue
#             name_list.remove(types[i].get("name"))
#             if name in name_list:
#                 continue
#             x_dict["id"] = id
#             x_dict["name"] = j.get("name", types[i].get("name")).upper()
#             x_dict["diags"] = j.get("diags", types[i].get("diags"))
#             x_dict["alarms"] = j.get("alarms", types[i].get("alarms"))
#             x_dict["controls"] = j.get("controls", types[i].get("controls"))
#             types[i] = x_dict
#             x_list.append(x_dict)
#     return x_list
