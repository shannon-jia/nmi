#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json, redirect


app = Sanic()

app.static('/', '../apidoc/doc')

@app.route("/")
async def index(request):
    url = app.url_for('static', filename='index.html')
    return redirect(url)

app.run(host='0.0.0.0', port=8888)
