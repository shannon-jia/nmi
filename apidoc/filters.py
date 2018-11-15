#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# FILTER

def get_afilter()

"""
@apiUse AFilter
@apiUse Back
@api {get} /filter/alarms/:id 1 get alarm points
@apiGroup Filter
@apiVersion 1.0.0
@apiParam {Number} id Unique alarm point.
"""

def patch_afilter()

"""
@apiUse AFilter
@apiUse Back
@api {patch} /filter/alarms 2 patch alarm points status
@apiGroup Filter
@apiVersion 1.0.0
@apiParam {Number} id Unique alarm point.
@apiParam {String} status alarm point status.
"""

def get_tfilter()

"""
@apiUse TFilter
@apiUse Back
@api {get} /filter/tampers/:id 3 get tamper points
@apiGroup Filter
@apiVersion 1.0.0
@apiParam {Number} id Unique tamper point.
"""

def patch_tfilter()

"""
@apiUse TFilter
@apiUse Back
@api {patch} /filter/tampers 4 patch tamper points status
@apiGroup Filter
@apiVersion 1.0.0
@apiParam {Number} id Unique tamper point.
@apiParam {String} status tamper point status.
"""
