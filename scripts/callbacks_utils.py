#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_utils.py
@time: 2024/11/9 9:07
"""
import json


def returnCtxIdStr(ctx, index=None):
    """return the idstr of ctx based on index, where ctx is a dash.callback_context object"""
    ctxTriggered = ctx.triggered
    if index is None:
        return [ctx.triggered[i]['prop_id'].split('.')[0] for i in range(0, len(ctxTriggered))]
    if isinstance(index, list):
        return [ctx.triggered[i]['prop_id'].split('.')[0] for i in index]
    if isinstance(index, int):
        return ctx.triggered[index]['prop_id'].split('.')[0]
    raise ValueError("Unexpected index received: {}({})".format(index, type(index)))


def returnDropdownOptions(options, first=[], last=[], sort=True):
    """return dropdown component options"""
    if (len(options) + len(first) + len(last)) == 0:
        return []

    if sort:
        options = sorted(list(options))

    baseOption = [{"label": option, "value": option} for option in options]
    if len(first) > 0:
        baseOption = returnDropdownOptions(first, sort=sort) + baseOption
    if len(last) > 0:
        baseOption = baseOption + returnDropdownOptions(last, sort=sort)
    return baseOption


def returnDropdown(options, first=[], last=[], value=None, sort=True):
    baseOption = returnDropdownOptions(options, first, last, sort=sort)
    if len(baseOption) == 0:
        defaultValue = None
    elif (value is None) or (value not in (options + first + last)):
        defaultValue = baseOption[0]["value"]
    else:
        defaultValue = value
    return defaultValue, baseOption


def checkExport(ctx, index):
    ctxIdStr = returnCtxIdStr(ctx, index)
    try:
        ctxId = json.loads(ctxIdStr)
        if ctxId.get("type", False) == "Button" and ctxId.get("function", False) == "Submit":
            export = True
        else:
            export = False
    except json.JSONDecodeError:
        export = False
    return export


def returnComponentID(baseDict, allKey=None, matchKey=None, **kwargs):
    from dash import ALL, MATCH

    if allKey is None:
        allKey = []
    elif isinstance(allKey, str):
        allKey = [allKey]

    if matchKey is None:
        matchKey = []
    elif isinstance(matchKey, str):
        matchKey = [matchKey]

    for key in allKey:
        baseDict[key] = ALL

    for key in matchKey:
        baseDict[key] = MATCH

    for key in kwargs:
        baseDict[key] = kwargs[key]
    return baseDict
