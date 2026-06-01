"""
@File        : header.py
@Author      : Min Dai, shi4712
@Date        : 2022/8/26 9:31
@Description : Define the header layout
"""
import os

from dash import html, dcc
import dash_bootstrap_components as dbc

logAndTitleCol = dbc.Col(
    dbc.Row(
            [
                dbc.Col(
                    html.Img(
                        src="../assets/logo.png",
                        className="center_block_ver",
                        style={
                            "display": "block",
                            "height": "60px",
                        },
                    ),
                ),
                dbc.Col(
                    "CellClick",
                    style={
                        "color": "#FFFFFF",
                        "font-size": "26px",
                    },
                    className="header_line_center",
                ),
            ],
    ),
    style={"margin-left": "10%"},
    width={"size": "auto"},
)

navbarButtonsCol = dbc.Col(
    dbc.Row(
        [
            dbc.Col(
                dbc.Button(
                    "Document", className="center_block width_adjust navButton",
                    id="Document",
                    style={"height": "32px"},  # default width == adjust??, the width of the button is larger than 100%
                ),
                width={"size": "2"},
            ),
            dbc.Col(
                [
                    dbc.ButtonGroup(
                        [
                            dbc.Button(
                                "Fix Selection",
                                id="fixSelection",
                                active=False, disabled=True,
                                n_clicks=0,
                                className="width_adjust navButton",
                                style={"height": "32px", "background-color": "darkgray", "border-color": "darkgray"},
                            ),
                            dbc.Button(
                                html.I(className="bi bi-union"),
                                id={"class": "fixSelection", "type": "Button", "name": "add"},
                                className="width_adjust",
                                style={"height": "32px", "visibility": "hidden"},
                            ),
                            dbc.Button(
                                html.I(className="bi bi-subtract"),
                                id={"class": "fixSelection", "type": "Button", "name": "remove"},
                                className="width_adjust",
                                style={"height": "32px", "visibility": "hidden"},
                            ),
                            dbc.Button(
                                html.I(className="bi bi-intersect"),
                                id={"class": "fixSelection", "type": "Button", "name": "inter"},
                                className="width_adjust",
                                style={"height": "32px", "visibility": "hidden"},
                            ),
                        ],
                        className="center_block width_adjust",
                        # style={"width": "100%"},
                    ),
                ],
                width={"size": "4"},
            ),
            dbc.Col(
                dbc.Button(
                    "Undo",
                    id="rollback",
                    className="center_block width_adjust navButton",
                    style={"height": "32px", "background-color": "darkgray", "border-color": "darkgray", "width": "100%"},
                    disabled=True,
                    active=False,
                ),
                width={"size": "2"},
            ),
            dbc.Col(
                dbc.Button(
                    "Reset", className="center_block width_adjust navButton",
                    id="reset",
                    style={"height": "32px", "width": "100%"},
                ),
                width={"size": "2"},
            ),
            dbc.Col(
                [
                    dcc.Download(id=dict(function="Export", type="Download")),
                    dbc.Button(
                        "Export", className="center_block width_adjust navButton",
                        id=dict(function="Export", type="Button"),
                        style={"height": "32px", "background-color": "darkgray", "border-color": "darkgray", "width": "100%"},
                    ),
                ],
                width = {"size": "2"},
            ),
        ],
        className="center_block width_adjust", justify="end",
    ),
    style={"margin-right": "5%"},
    width={"size": "auto"},
)

header = dbc.Row(
    [
        logAndTitleCol,
        navbarButtonsCol
    ],
    style={
      "background-color": "#0F0F0F"
    },
    className="center_block_hor header init_padding, init_margin",
    justify="between",
)
