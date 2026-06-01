#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: dash_input.py
@time: 2024/11/9 9:23
"""
import dash
from dash import html
from apps.template import *

defaultLabelClass = "inputGroup_label collapseCard_row_height collapseCard_label_width"
defaultInputClass = "collapseCard_row_height collapseCard_input_width"


class DashInput(object):
    class_name = "DashInput_Name"

    def __init__(self, dashInput, baseIDDict):
        self.name = dashInput[self.class_name]
        self.show_name = dashInput["show_name"]
        self.id = self.returnID(baseIDDict)

    def returnID(self, baseIDDict):
        assert isinstance(baseIDDict, dict), """based id should be a dict type object"""
        baseIDDict = baseIDDict.copy()
        baseIDDict[self.class_name] = self.name
        return baseIDDict


class CardInput(DashInput):
    class_name = "card_name"

    def __init__(self, card, baseIDDict={}):
        super().__init__(dashInput=card, baseIDDict=baseIDDict)
        self.forms = [FormInput(form, baseIDDict=self.id) for form in card["forms"]]

        self.component = self.returnComponent(**card.get("kwargs", {}))

    def returnComponent(self, **kwargs):
        btnList = []
        for form in self.forms:
            if form.name == "Submit":
                btnList.append(dbc.ButtonGroup(
                    [
                        dbc.Button(
                            form.show_name,
                            className="navButton", n_clicks=0,
                            id=returnIDDict(type="form_button", **form.id),
                            style={"width": "100%"}
                        ),
                        dbc.Button(
                            # html.I("?"),
                            id=returnIDDict(type="document_button", **form.id),
                            className="width_adjust navButton",
                            style={
                                "width": "0%",
                                "border": "none",
                                # "color": "white", "margin-left": "-0.5px",
                            }
                        ),
                    ],
                ))
            elif form.faker_form:
                continue
            else:
                btnList.append(
                        dbc.ButtonGroup(
                        [
                            dbc.Button(
                                form.show_name,
                                className="navButton", n_clicks=0,
                                id=returnIDDict(type="form_button", **form.id),
                                style={"width": "85%"}
                            ),
                            # dbc.ButtonGroup(
                            #     [
                            #         # dbc.Button(
                            #         #     # html.I("?"),
                            #         #     # html.I(className="bi bi-question-circle"),
                            #         #     # id=returnIDDict(type="document_button", **form.id),
                            #         #     className="width_adjust navButton",
                            #         #     style={
                            #         #         # "width": "15%",
                            #         #         "border": "none",
                            #         #         "background-color": "white",
                            #         #         "height": "10%",
                            #         #     },
                            #         #     disabled=True,
                            #         # ),
                            #         dbc.Button(
                            #             # html.I("?"),
                            #             html.I(className="bi bi-question-lg"),
                            #             id=returnIDDict(type="document_button", **form.id),
                            #             className="width_adjust navButton",
                            #             style={
                            #                 # "width": "15%",
                            #                 "margin-top": "30%",
                            #                 "border": "none",
                            #                 "background-color": "white",
                            #                 "color": "blue",
                            #                 "height": "40%",
                            #                 "margin-bottom": "30%",
                            #             }
                            #         ),
                            #         # dbc.Button(
                            #         #     # html.I("?"),
                            #         #     # html.I(className="bi bi-question-circle"),
                            #         #     # id=returnIDDict(type="document_button", **form.id),
                            #         #     className="width_adjust navButton",
                            #         #     style={
                            #         #         # "width": "15%",
                            #         #         "border": "none",
                            #         #         "background-color": "white",
                            #         #         "height": "10%",
                            #         #     },
                            #         #     disabled=True,
                            #         # ),
                            #     ],
                            #     vertical=True,
                            # ),
                            dbc.Button(
                                # html.I("?"),
                                html.I(className="bi bi-question-circle"),
                                id=returnIDDict(type="document_button", **form.id),
                                className="width_adjust navButton",
                                style={
                                    "width": "15%",
                                    # "margin-top": "30%",
                                    "border": "none",
                                    # "background-color": "white",
                                    # "color": "blue",
                                    # "height": "40%",
                                    # "margin-bottom": "30%",
                                }
                            ),
                        ],
                    )
                )

        defaultText = dash.html.Div(
            "Please load data firstly!", style={"color": "red", "display": "none"},
            id=returnIDDict(form_name="error", **self.id)
        )

        component = dbc.Row(
            [
                dbc.Col(
                    dbc.Nav(
                        btnList,
                        vertical=True,
                        pills=True,
                    ),
                    width={"size": 4},
                    style={"padding-left": 0}
                ),
                dbc.Col(
                    [defaultText] + [form.component for form in self.forms],
                    width={"size": 8}
                )
            ],
            className="collapseComponent",
        )

        collapseCard = dbc.Card(
            [
                dbc.Button(
                    self.show_name, id=returnIDDict(type="card_button", **self.id),
                    style={"width": "100%"}, n_clicks=0,

                ),
                dbc.Collapse(
                    component, id=returnIDDict(type="collapse", **self.id),
                    is_open=True, style={"width": "100%"}
                )
            ],
            className="collapseCard",
        )
        return collapseCard


class FormInput(DashInput):
    class_name = "form_name"

    def __init__(self, form, baseIDDict, **kwargs):
        super().__init__(dashInput=form, baseIDDict=baseIDDict)
        self.faker_form = form.get("faker_form", False)
        if not self.faker_form:
            self.lines = [LineInput(line, baseIDDict=self.id) for line in form["lines"]]
        self.component = self.returnComponent(**form.get("kwargs", {}))

    def returnComponent(self, **kwargs):
        if self.faker_form:
            component = dbc.Form(
                style={"display": "none"}
            )
        else:
            component = dbc.Form(
                [line.component for line in self.lines], id=self.id,
                style={"display": kwargs.get("display", "none")}
            )
        return component


class LineInput(DashInput):
    class_name = "line_name"
    """
        There is no name for line input, 
        structure of line [label_input, ...... , label_input]
    """
    def __init__(self, line, baseIDDict): ## line is list object
        # super().__init__(dashInput=line, baseIDDict=baseIDDict)
        self.name = None
        self.show_name = None
        self.id = None
        self.label_inputs = [LabelInput(label_input, baseIDDict=baseIDDict) for label_input in line]
        self.component = self.returnComponent()

    def returnID(self, baseIDDict):
        return None

    def returnComponent(self):
        assert len(self.label_inputs) % 2 == 0, """It should be 2n label input in a line"""
        colNum = int(len(self.label_inputs)/2)
        assert colNum in [1, 2, 3, 4, 6, 12], """Invalid length of col in a line: {colNum}"""
        colWidth = int(12/colNum)
        component = []
        for i in range(0, colNum):
            label, input = self.label_inputs[2*i].component, self.label_inputs[2*i+1].component
            if label is None:
                col = dbc.Col(
                    dbc.InputGroup([input]),
                    width=colWidth
                )
            else:
                col = dbc.Col(
                    dbc.InputGroup([label, input]),
                    width=colWidth
                )
            component.append(col)
        return dbc.Row(component)


class LabelInput(DashInput):
    class_name = "label_name"

    def __init__(self, label_input, baseIDDict):
        self.type = label_input["type"]
        self.component_kwargs = label_input["component_kwargs"]
        super().__init__(dashInput=label_input, baseIDDict=baseIDDict)
        self.component = self.returnComponent(**label_input.get("kwargs", {}))

    def returnID(self, baseIDDict):
        assert isinstance(baseIDDict, dict), """based id should be a dict type object"""
        baseIDDict = baseIDDict.copy()
        baseIDDict[self.class_name] = self.name
        baseIDDict["type"] = self.type
        return baseIDDict

    @staticmethod
    def __returnUpload(**kwargs):
        buttonIDDict = kwargs["id"].copy()
        buttonIDDict["type"] = "Button"
        return dbc.Button(
            dcc.Upload(**kwargs),
            className="inputGroup_label collapseCard_row_height collapseCard_label_width navButton",
            # style={"margin-top": "18px"},
            id=returnIDDict(**buttonIDDict),
            # style={"margin-bottom": "10px"}
        )

    @staticmethod
    def __returnSlider(**kwargs):
        from dash import html
        divIDDict = kwargs["id"].copy()
        divIDDict["type"] = "Div"
        return html.Div(
            dcc.Slider(**kwargs),
            id=returnIDDict(**divIDDict),
        )

    @staticmethod
    def __returnRangeSlider(**kwargs):
        from dash import html
        divIDDict = kwargs["id"].copy()
        divIDDict["type"] = "Div"
        return html.Div(
            dcc.RangeSlider(**kwargs),
            id=returnIDDict(**divIDDict),
            style={"width": "90%", "margin-top": "25px"}
        )

    def returnComponent(self, **kwargs):
        switchDict = {
            "Label": dbc.Label,
            "Input": dbc.Input,
            "RadioItems": dbc.RadioItems,
            "Button": dbc.Button,
            "Select": dbc.Select,
            "Checklist": dbc.Checklist,
            "FormText": dbc.FormText,
            "Dropdown": dcc.Dropdown,
            "Download": dcc.Download,
            "Upload": self.__returnUpload,
            "Slider": self.__returnSlider,
            "RangeSlider": self.__returnRangeSlider,
        }
        if self.type is None:
            return None
        else:
            if kwargs.get("setID", True):
                component = switchDict[self.type](id=self.id, **self.component_kwargs)
            else:
                component = switchDict[self.type](**self.component_kwargs)
        return component
