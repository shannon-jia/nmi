#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.response import json, redirect
from sanic_cors import CORS

from .blueprint.device import bp as device
from .blueprint.device_types import bp as device_types
from .blueprint.sensors import bp as sensors
from .blueprint.tampers import bp as tampers
from .blueprint.filters import bp as filters
from .blueprint.shunts import bp as shunts
from .blueprint.trbls import bp as trbls
from .blueprint.pres import bp as pres
from .blueprint.controls import bp as controls
from .blueprint.auto import bp as auto

app = Sanic(__name__)
app.blueprint(device_types, url_prefix='/device_types')
app.blueprint(device, url_prefix='/device')
app.blueprint(sensors, url_prefix='/sensors')
app.blueprint(tampers, url_prefix='/tampers')
app.blueprint(filters, url_prefix='/filter')
app.blueprint(shunts, url_prefix='/shunt')
app.blueprint(trbls, url_prefix='/trbls')
app.blueprint(pres, url_prefix='/pre_alarms')
app.blueprint(controls, url_prefix='/controls')
app.blueprint(auto, url_prefix='/auto')
app.static('/', './docs/doc', name='index')

CORS(app)

@app.route("/")
async def index(request):
    url = app.url_for('static', filename='index.html', name='index')
    return redirect(url)

def start(port, site=None):
    app.site = site
    device_types.site = app.site
    device.site = app.site
    sensors.site = app.site
    tampers.site = app.site
    filters.site = app.site
    shunts.site = app.site
    trbls.site = app.site
    pres.site = app.site
    controls.site = app.site
    auto.site = app.site
    return app.create_server('0.0.0.0', port)


if __name__ == "__main__":
    start(8888)
