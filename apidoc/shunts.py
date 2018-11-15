#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SHUNT

def get_ashunt()

"""
@apiUse AShunt
@apiUse Back
@api {get} /shunt/alarms/:id 1 get alarm points
@apiGroup Shunt
@apiVersion 1.0.0
@apiParam {Number} id Unique alarm point.
"""

def patch_ashunt()

"""
@apiUse AShunt
@apiUse Back
@api {patch} /shunt/alarms 2 patch alarm points status
@apiGroup Shunt
@apiVersion 1.0.0
@apiParam {Number} id Unique alarm point.
@apiParam {String} status alarm point status.
"""

def get_shunt()

"""
@apiUse TShunt
@apiUse Back
@api {get} /shunt/tampers/:id 3 get tamper points
@apiGroup Shunt
@apiVersion 1.0.0
@apiParam {Number} id Unique tamper point.
"""

def patch_shunt()

"""
@apiUse TShunt
@apiUse Back
@api {patch} /shunt/tampers 4 patch tamper points status
@apiGroup Shunt
@apiVersion 1.0.0
@apiParam {Number} id Unique tamper point.
@apiParam {String} status tamper point status.
"""
