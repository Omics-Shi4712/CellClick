#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: some init
@version: 1.0.0
@file: init.py
@time: 2023/10/17 21:28
"""
import json
import os

import dash
import pandas as pd
from dash import ALL, MATCH, dcc, html
from dash.exceptions import PreventUpdate
from dash import callback, Input, Output, State
import dash_bootstrap_components as dbc

from settings import ClickCellManagerInitDict, tmpDir, marker_ref, marker_ref_validation
from manager.cellclick import CellClickManager

from scripts.utils import *
from scripts.callbacks_utils import *
from apps.template import returnIDDict
from apps.modal import cardDict

cellClickManager = CellClickManager(**ClickCellManagerInitDict)

with open(os.path.join(projectDir, "apps/document.json"), "r") as f:
    documentJson = json.load(f)

@callback(
    Output("documentModal", "is_open"),
    [
        Input("Document", "n_clicks"),
        Input("close-popup-button", "n_clicks"),
        Input({"card_name": ALL, "form_name": ALL, "type": "document_button"}, "n_clicks")
    ],
    [dash.dependencies.State("documentModal", "is_open")]
)
def toggle_modal(n1, n2, n3, is_open):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr in ["Document", "close-popup-button", ""]:
        if n1 or n2:
            return not is_open
        return is_open
    else:
        return True


@callback(
    Output(
        {"class": "Document", "type": "Button", "card_name": ALL},
        "active"
    ),
    # Output(
    #     {"class": "Document", "card_name": ALL, "form_name": ALL, "type": "Button"},
    #     "active"
    # ),
    Output("Module Nav", "children"),
    Output("Form Document", "children"),
    inputs=dict(
        documentNav=(
            State(
                {"class": "Document", "type": "Button", "card_name": ALL},
                "id"
            ),
            Input(
                {"class": "Document", "type": "Button", "card_name": ALL},
                "n_clicks"
            ),
        ),
        moduleNav=(
            # State(
            #     {"class": "Document", "card_name": ALL, "form_name": ALL, "type": "Button"},
            #     "id"
            # ),
            Input(
                {"class": "Document", "card_name": ALL, "form_name": ALL, "type": "Button"},
                "n_clicks"
            ),
        ),
        documentButton=(
            Input({"card_name": ALL, "form_name": ALL, "type": "document_button"}, "n_clicks")
        ),
    ),
)
def returnDocument(documentNav, moduleNav, documentButton):
    def returnModuleBar(card, documentJson, IDDict, active=None):
        defaultDescription = "This is a description.\t" * 5

        show_name = card["show_name"]
        card_name = card["card_name"]
        overview = documentJson[card_name]["overview"]
        if overview == "":
            overview = defaultDescription

        if active is None:
            active = card["forms"][0]["form_name"]

        buttonList = []
        for form in card["forms"]:
            if form["form_name"] == "Submit":
                continue
            buttonList.append(
                dbc.Button(
                    form["show_name"], n_clicks=0, active=True if form["form_name"] == active else False,
                    id=returnIDDict(card_name=card_name, form_name=form["form_name"], type="Button", **IDDict),
                    outline=True, color="primary", className="me-1", style={"border": "none"}
                )
            )
        moduleNav = dbc.Nav(
            buttonList,
            vertical=True, pills=True,
        )

        return [
            html.H5(
                show_name, className="display-8",
                style={"margin-left": "20px", "margin-top": "10px"},
            ),
            html.Hr(),
            html.P(returnStringComponent(overview), style={"margin-left": "20px"}),  # description
            moduleNav,
        ]

    def returnLineDocument(lines, lineDocument, IDDict):
        tableData = []
        for line in lines:
            if line[0]["label_name"] != "Submit" and line[0]["label_name"] != "Object Name":
                tableData.append(
                    [line[0]["show_name"], lineDocument[line[0]["label_name"]]]
                )
        table = pd.DataFrame(tableData, columns=["Input", "Description"])
        return dash.dash_table.DataTable(
            table.to_dict("records"), [{"name": i, "id": i} for i in table.columns],
            style_table={"margin-top": "30px", "margin-bottom": "30px"},
            style_header={"height": "50px"},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
        )

    def returnFormDocument(form, formJson, IDDict):
        defaultDescription = "This is a description.\t" * 5
        defaultOverviewImg = "./assets/overview.png"
        defaultFormImg = "./assets/image/document_datasettings_upload.png"

        overviewImg = defaultOverviewImg if formJson["overview"]["img"] == "" else formJson["overview"]["img"]
        if formJson["overview"]["description"] == "":
            overview = defaultDescription
        else:
            overview = formJson["overview"]["description"]

        if formJson["form introduction"]["img"] == "":
            formImg = defaultFormImg
        else:
            formImg = formJson["form introduction"]["img"]

        videoList = [html.Hr(), html.H5("Example")]
        for example in formJson["example"]:
            for key in ["video", "title", "description"]:
                if example[key] != "":
                    if key == "video":
                        videoList.append(html.Video(src=example[key], controls=True))
                    if key == "title":
                        videoList.append(html.H6(example[key], style={"text-align": "center", "margin-top": "8px"}))
                    if key == "description":
                        videoList.append(html.P(returnStringComponent(example[key]), style={"margin-top": "10px"}))

        document = dbc.Card(
            [
                html.H5("Overview"),
                html.Img(src=overviewImg),
                html.P(returnStringComponent(overview))
            ] + ([] if form.get("faker_form", False) else [
                html.Hr(),
                html.H5("Form Introduction"),
                html.Img(src=formImg, style={"max-width": "300px"}, className="center_block_hor"),  # image
                returnLineDocument(
                    form["lines"], lineDocument=formJson["form introduction"]["inputs"], IDDict=returnIDDict(form_name=form["form_name"], **IDDict)
                ),
            ]) + (videoList if len(videoList) > 2 else []),
            id=returnIDDict(form_name=form["form_name"], **IDDict),
            style={"padding-left": "20px", "padding-top": "15px", "padding-right": "20px"},
        )

        return document

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "":
        module = cardDict[list(cardDict.keys())[0]]
        moduleBar = returnModuleBar(module, documentJson=documentJson, IDDict={"class": "Document"})

        moduleNum = len(cardDict)
        moduleActive = [True] + [False] * (moduleNum - 1)

        # formNum = len(module["forms"])
        # formActive = [True] + [False] * (formNum - 1)

        form = module["forms"][0]
        formJson = documentJson[module["card_name"]]["forms"][form["form_name"]]
        formDocument = returnFormDocument(
            form=form, formJson=formJson,
            IDDict={"class": "Document", "card_name": module["card_name"]},
        )
    else:
        if len(returnCtxIdStr(dash.callback_context)) > 1:
            raise PreventUpdate # I don't know what happened
        else:
            ctxId = json.loads(ctxIdStr)
            if "form_name" not in ctxId:
                card_name = ctxId["card_name"]
                form_name = cardDict[card_name]["forms"][0]["form_name"]
            else:
                card_name = ctxId["card_name"]
                form_name = ctxId["form_name"]

            module = cardDict[card_name]
            moduleBar = returnModuleBar(
                module, documentJson=documentJson, IDDict={"class": "Document"}, active=form_name
            )

            moduleActive = []
            for id in documentNav[0]:
                if card_name == id["card_name"]:
                    moduleActive.append(True)
                else:
                    moduleActive.append(False)

            # return form
            for form in module["forms"]:
                if form["form_name"] == form_name:
                    break
            formJson = documentJson[module["card_name"]]["forms"][form["form_name"]]
            formDocument = returnFormDocument(
                form=form, formJson=formJson,
                IDDict={"class": "Document", "card_name": module["card_name"]},
            )

    return moduleActive, moduleBar, formDocument
