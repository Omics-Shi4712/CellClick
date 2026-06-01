#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description:
@version: 1.0.0
@file: modal.py
@time: 2024/11/29 14:40
"""

import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

# from apps.moduleSettings import dataSettingCard, preprocessingCard, dataVisualizationCard, clusterAnalysisCard, geneAnalysisCard, cellReannotationCard
from apps.moduleSettings import dataSettingCard, preprocessingCard, dataVisualizationCard, geneAnalysisCard, evaluationValidationCard, cellReannotationCard
from apps.template import returnIDDict

cardDict = {
    "CellClick Overview": {
        "card_name": "CellClick Overview", "show_name": "Overview",
        "forms": [
            {
                "form_name": "Introduction", "show_name": "Introduction",
                "faker_form": True,
            }
        ]
    }
}
for card in [
    # dataSettingCard, preprocessingCard, dataVisualizationCard, clusterAnalysisCard, geneAnalysisCard,
    dataSettingCard, preprocessingCard, dataVisualizationCard, geneAnalysisCard, evaluationValidationCard,
    cellReannotationCard
]:
    cardDict[card["card_name"]] = card

# cardDict["Cell Selection"] = {
#     "Cell Selection": {
#         "card_name": "Cell Selection", "show_name": "Cell Selection",
#         "forms": [
#             {
#                 "form_name": "Cells Table", "show_name": "Cells Table",
#                 "faker_form": True,
#             },
#             {
#                 "form_name": "Visualization Selection", "show_name": "Visualization Selection",
#                 "faker_form": True,
#             }
#         ]
#     }
# }


def returnCellClickDocument():
    # navList = ["Overview"] + list(cardDict.keys())
    navList = list(cardDict.keys())
    documentNav = dbc.Nav(
        [
            dbc.Button(
                cardDict[buttonLabel]["show_name"] if buttonLabel in cardDict else buttonLabel,
                className="navButton", n_clicks=0, active=False,
                style={'flex': 1, 'textAlign': 'center'},
                id={
                    "class": "Document", "type": "Button",
                    "card_name": cardDict[buttonLabel]["card_name"] if buttonLabel in cardDict else buttonLabel
                }
            ) for buttonLabel in navList
        ],
        vertical=False, pills=True,
    )  # maybe dbc.Tab component is a good choice
    return html.Div(
        [
            dbc.Row(documentNav),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            id="Module Nav",
                            style={
                                # "position": "fixed",
                                # "width": "100%",
                                # "padding": "2rem 1rem",
                                "height": "800px",
                                "background-color": "#f8f9fa",

                            }
                        ),
                        width={"size": 3}
                    ),
                    dbc.Col(
                        html.Div(
                            style={
                                "overflow": "scroll", "height": "800px",
                                # "margin-left": "18rem",
                                # "margin-right": "2rem",
                                "margin-top": "1rem",
                                # "padding": "2rem 1rem",
                            },
                            id="Form Document",
                        ),
                        width={"size": 9}
                    ),
                ]
            ),
        ],
    )


document = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Document for CellClick")),
        dbc.ModalBody(returnCellClickDocument()),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-popup-button", className="ms-auto", n_clicks=0)
        )
    ],
    id="documentModal", is_open=False, size="xl",
    style={'position': 'fixed'}
)


# def returnQCLayout(baseIDDict):
#     def returnQCPlot(IDDict, x_slider=True, y_slider=True):
#         del IDDict["type"]
#         return dbc.Col(
#             [
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             dcc.Graph(
#                                 id=returnIDDict(type="Graph", **IDDict),
#                                 style={
#                                     "padding": "25px 25px 0px 0px",
#                                     "height": "500px"
#                                 },
#                                 config=dict(
#                                     toImageButtonOptions=dict(
#                                         format="svg",
#                                         height=500,
#                                         width=500,
#                                     ),
#                                     displaylogo=False,
#                                     modeBarButtonsToRemove=[
#                                         "zoom", "pan", "select", "lasso2d",
#                                         "zoomIn", "zoomOut", "autoScale",
#                                     ],
#                                 ),
#                             ),
#                             width={"size": 11},  # the style of default range slider
#
#                         ),
#                         dbc.Col(
#                             dcc.RangeSlider(
#                                 id=returnIDDict(axis="y", type="RangeSlider", **IDDict),
#                                 min=0, max=0, value=[0, 0],
#                                 vertical=True, verticalHeight=500,
#                             ) if y_slider else None,
#                             width={"size": 1},
#                             style={"margin-left": "-25px"}
#                         ),
#                     ]
#                 ),
#                 dbc.Row(
#                     [
#                         dbc.Col(
#                             dcc.RangeSlider(
#                                 id=returnIDDict(axis="x", type="RangeSlider", **IDDict),
#                                 min=0, max=0, value=[0, 0],
#                                 vertical=False,
#                             ) if x_slider else None,
#                         ),
#                         dbc.Col(width={"size": 1})
#                     ]
#                 )
#             ],
#             width={"size": 6}
#         )
#
#     # actually, QC Table is a dash_table component
#     # for index, fig in enumerate(["gene_counts", "mt", "doublet", "QC table"]):
#     gene_counts = returnQCPlot(
#         returnIDDict(graphIndex=0, type="Graph", name="Gene Counts", **baseIDDict),
#         x_slider=True, y_slider=True
#     )
#     MT_PCT = returnQCPlot(
#         returnIDDict(graphIndex=1, type="Graph", name="MT PCT", **baseIDDict),
#         x_slider=False, y_slider=True
#     )
#     doublet_Score = returnQCPlot(
#         returnIDDict(graphIndex=2, type="Graph", name="Doublet Score", **baseIDDict),  # actually, it filters gene
#         x_slider=True, y_slider=True,
#     )
#     QC_table = dbc.Col(
#         [
#             dbc.Row(
#                 dash_table.DataTable(
#                     id=returnIDDict(graphIndex=3, type="Table", name="Cell QC Table", **baseIDDict),
#                     editable=False, style_table={"width": "80%"}
#                 ),
#             ),
#             dbc.Row(
#                 dash_table.DataTable(
#                     id=returnIDDict(graphIndex=4, type="Table", name="Gene QC Table", **baseIDDict),
#                     editable=False, style_table={"width": "80%"}
#                 ),
#             ),
#             dbc.Row(
#                 dbc.Button(
#                     "Filter Cell", id=returnIDDict(type="Button", name="Filter Cell", **baseIDDict),
#                     className="ms-auto", n_clicks=0,
#                     style={"width": "30%", "margin-right": "20px", "margin-top": "20px"},
#                 ),
#             ),
#         ]
#     )
#     return dbc.CardBody(
#         [
#             dbc.Row(
#                 [gene_counts, MT_PCT]
#             ),
#             dbc.Row(
#                 [doublet_Score, QC_table]
#             ),
#         ]
#     )


# qcController = dbc.Modal(
#     [
#         dbc.ModalHeader(dbc.ModalTitle("QC Controller")),
#         dbc.ModalBody(returnQCLayout(baseIDDict={"class": "QC", "group": "graph", "index": 0})),
#         dbc.ModalFooter(
#             dbc.Button("Close", id="close-popup-button_QC", className="ms-auto", n_clicks=0)
#         )
#     ],
#     id="QCModal", is_open=False, size="xl",
#     style={'position': 'fixed', "height": "800px"}
# )

