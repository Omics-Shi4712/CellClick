"""
@File        : body.py
@Author      : Min Dai, shi4712
@Date        : 2022/8/26 10:51
@Description : define body layout
"""
import dash
from dash import dcc, html, dash_table

from apps.template import *
from apps.moduleSettings import modifyClassName, defaultLabelClass, defaultInputClass
from apps.moduleSettings import leftNavBar
from apps.dash_input import CardInput
# from apps.modal import document, qcController
from apps.modal import document

from settings import CanvasManagerInitDict


def returnTableSwitcher(show_name, label_name):
    idDict = {
        "class": "Cells Table", "group": "switcher",
        "type": "Button",
    }
    button = dbc.Button(
        show_name,
        className=modifyClassName(
            defaultInputClass, ["navButton", "inputGroup_label_inputText"],
        ),
        id=returnIDDict(label=label_name, **idDict),
        style={"margin-left": "10px", "padding": "0px"},
    )
    return button


def returnTableContainer():
    import pandas as pd
    # refer to https://github.com/plotly/dash-table/issues/436
    # Empty DataFrame to start the DataTable
    # (workaround for bug in DataTable - https://github.com/plotly/dash-table/issues/436#issuecomment-615924723)
    start_table_df = pd.DataFrame(columns=[''])
    data = start_table_df.to_dict('records'),
    columns = [{'id': c, 'name': c} for c in start_table_df.columns],

    table = dash_table.DataTable(
        id={
            "class": "Cells Table", "group": "container",
            "type": "Table",
        },

        # refer to https://github.com/plotly/dash-table/issues/436
        data=start_table_df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in start_table_df.columns],

        # column_selectable="multi",
        # row_selectable='multi',

        page_current=0, page_size=6, page_action="custom",

        sort_action='custom', sort_mode='multi', sort_by=[],

        filter_action='custom', filter_query='',

        fixed_rows={'headers': True}, fixed_columns={'headers': True, 'data': 1},
        # style_table={'height': 400, 'overflowX': 'auto', "max-width": "100%", "visibility": "hidden"},
        style_table={"display": "none", 'height': "450px", 'overflowX': 'auto', "max-width": "100%"},
        # defaults to 500, each row takes up 30px
        style_header={"height": "50px"},
        style_cell={
            'height': '40px', 'whiteSpace': 'normal',
            # all three widths are needed
            'width': '200px', 'minWidth': '200px', 'maxWidth': '200px',
        },
    )
    return table


def returnTableController(label):
    button = dbc.Button(
        label,
        id={
            "class": "Cells Table", "group": "controller",
            "type": "Button", "label": label
        },
        style={"margin": "0 5%", "border-radius": "0"}
    )
    return button


def returnColumnsController(label):
    buttonGroup = dbc.ButtonGroup(
        [
            dbc.Button(
                label,
                className=modifyClassName(defaultInputClass, ["inputGroup_label_inputText"]),
                style={"margin-left": "10px", "padding": "0px", "border-radius": "0"},
                id={
                    "class": "Cells Table", "group": "controller",
                    "type": "Button", "label": label
                },
            ),
            dcc.Dropdown(
                style={"width": "60%"},
                id={
                    "class": "Cells Table", "group": "controller",
                    "type": "Dropdown", "label": label
                },
                searchable=True,
            )
        ],
        style={"width": "60%", "margin-top": "10px"}
    )
    return buttonGroup


leftNavBar = [
    CardInput(card).component for card in leftNavBar
]

# cellsTableCollapseCard = dbc.Card(
#     [
#         dbc.Button("Cells Table", style={"width": "100%"}),
#         html.Div(
#             [
#                 dbc.Row(
#                     dbc.ButtonGroup(
#                         [
#                             returnTableSwitcher("Select by Meta", "Meta"),
#                             returnTableSwitcher("Select by Gene", "Expression"),
#                             returnTableSwitcher("Selected Cells", "Selected")
#                         ],
#                         style={"width": "80%", "margin-top": "10px"}
#                     ),
#                 ),
#                 dbc.Row(
#                     returnColumnsController("Add Column")
#                 ),
#                 dbc.Row(
#                     returnColumnsController("Remove Column")
#                 ),
#                 dbc.Row(
#                     [returnTableContainer()],
#                     style={"min-height": "400px", "margin-top": "10px"}
#                 ),
#                 dbc.Row(
#                     dbc.ButtonGroup(
#                         [
#                             returnTableController("Select All"),
#                             returnTableController("Unselect All"),
#                             # returnTableController("Reset"),
#                         ],
#                     ),
#                     style={"margin-top": "10px", "margin-bottom": "10px", "padding": "0 5%"}
#                 ),
#             ],
#             id={
#                 "class": "Cells Table", "group": "container",
#                 "type": "Div"
#             },
#             style={"visibility": "hidden"}
#         ),
#     ],
# )
# leftNavBar.append(cellsTableCollapseCard)


rowNum = CanvasManagerInitDict["rowNum"]
colNum = CanvasManagerInitDict["colNum"]
body = dash.html.Div(
    [
        document,
        # qcController,
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Label(
                            children="None data has been loaded!",
                            id="Current Data ID",
                            className="inputGroup_label_inputText center_block_hor",
                            style={
                                "width": "70%",
                                "line-height": "45px", "height": "45px",
                                "text-align": "center", "margin-bottom": "0px",
                                "font-weight": "bold",
                                # "border": "1px", "border-style": "solid",
                            }
                        ),
                    ]
                ),
                dbc.Alert(
                    "This is an alert", dismissable=True, is_open=False,
                    id="CellClickAlert", className="center_block_hor",
                    style={
                        "text-align": "center",
                        "width": "90%",
                    },
                ),
                dbc.Alert(
                    "This is an alert", dismissable=True, is_open=False,
                    id="PreprocessingAlert", className="center_block_hor",
                    style={
                        "text-align": "center",
                        "width": "90%",
                    },
                ),
                dbc.Col(leftNavBar, width={"size": 4}),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.Div(
                                    [
                                        dbc.Button(
                                            className="btn-close canvasCloseBtn",
                                            id={"type": "Button", "class": "canvas", "function": "close", "index": i}
                                        ),
                                        html.Div(
                                            id={"type": "Div", "class": "canvas", "function": "container", "index": i}
                                        )
                                    ],
                                    className="canvasDiv_default",
                                    # className="canvasDiv_total",
                                    style={"display": "none"},
                                    id={"type": "Div", "class": "canvas", "index": i}
                                ) for i in range(0, rowNum * colNum)
                            ],
                            id="canvas",
                            style={
                                "padding-left": "30px",
                            },
                        ),
                    ],
                    width={"size": 8},
                ),

                dcc.Store(id="User Session ID"),  # record the user session and data
                dcc.Store(id="refresh_UserSessionIDRecorder", data=None),
                dcc.Store(id="Removed Data ID"),
                dcc.Store(id="refresh_annotationTypeRecorder", data=0),
                dcc.Store(id="refresh_clusterHistoryRecorder", data=0),
                dcc.Store(id="refresh_selectedCellsRecorder", data=0),
                dcc.Store(id="refresh_fixedCellsRecorder", data=0),
                dcc.Store(id=dict(type="Group Cells", label_name="Group A", function="refresh"), data=0),
                dcc.Store(id=dict(type="Group Cells", label_name="Group B", function="refresh"), data=0),
            ],
            justify="between"
        ),
    ],
    className="center_block_hor body init_padding, init_margin",
)
