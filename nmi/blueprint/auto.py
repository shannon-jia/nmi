#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sanic import Blueprint
from sanic.response import json


bp = Blueprint(__name__)


@bp.route('/', methods=['GET'])
async def auto(request):
    if not bp.site.auto:
        bp.site.auto = True
    else:
        bp.site.auto = False
    return json({"auto": bp.site.auto})
