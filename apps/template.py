"""
@File        : template.py
@Author      : Min Dai, shi4712
@Date        : 2022/8/26 10:51
@Description : define some basic/common component
"""
from dash import dcc
import dash_bootstrap_components as dbc

def returnIDDict(**kwargs):
    defaultDict = {}
    for key in kwargs:
        defaultDict[key] = kwargs[key]
    return defaultDict


def returnFigCard(figType, index, **kwargs):
    """
    return fig card based on figType
    in fig card, the default id is {"class": figType, "group": "graph", "index": index}
    :param index: the index of fig in the same figType figs
    :param figType: the type of the figure
    :return: abc.Card component
    """

    idDict = {
        "class": figType,
        "group": "graph",
        "index": index,
    }
    if figType == "QC":
        cardBody = returnQCCardBody(attributes=kwargs.get("attributes", None), **idDict)
    elif figType == "geneEmbedding":
        cardBody = returnGeneExpressionCardBody(**idDict)
    elif figType == "geneDot":
        cardBody = returnGeneDotCardBody(**idDict)
    elif figType == "cellEmbedding":
        cardBody = returnCellEmbeddingCardBody(**idDict)
    elif figType == "cellStat":
        cardBody = returnCellStatCardBody(**idDict)
    elif figType == "markerGeneIdentification":
        cardBody = returnMarkerGeneIdentificationCardBody(**idDict)
    elif figType == "markerGeneEvaluation":
        cardBody = returnMarkerGeneEvaluationCardBody(**idDict)
    elif figType == "expressionSimilaritySearch":
        cardBody = returnExpressionSimilaritySearchCardBody(**idDict)
    elif figType == "annotationEvaluation":
        cardBody = returnAnnotationEvaluationCardBody(**idDict)
    elif figType == "markerGeneScoring":
        cardBody = returnMarkerGeneScoringCardBody(**idDict)
    elif figType == "cellSelection":
        cardBody = returnCellSelectionCardBody(**idDict)
    elif figType == "visualization":
        cardBody = returnVisualizationCardBody(**idDict)
    else:
        raise ValueError("Unexpected figType received: {}".format(figType))

    switchDict = {
        "QC": "QC",
        "cellEmbedding": "Cell Embedding",
        "geneEmbedding": "Gene Embedding",
        "geneDot": "Gene Dot",
        "markerGeneIdentification": "Marker Gene Identification",
        "markerGeneEvaluation": "Cell Identification",
        "annotationEvaluation": "Annotation Evaluation",
        "markerGeneScoring": "Reference Comparison",
        "cellSelection": "Cell Selection",
    }

    dataIDRow = dbc.Row(
        dbc.InputGroup(
            [
                dbc.InputGroupText(
                    children="{}".format(kwargs["dataID"]),
                    id=returnIDDict(type="Label", function="Data ID", **idDict),
                    style={
                        "line-height": "36px", "height": "36px",
                        "text-align": "center", "margin-bottom": "0px",
                        "font-weight": "bold",
                        # "border": "1px", "border-style": "solid",
                    }
                ),
                dbc.InputGroupText(
                    children=switchDict[figType],
                    # id=returnIDDict(type="Label", function="Data ID", **idDict),
                    style={
                        "line-height": "36px", "height": "36px",
                        "text-align": "center", "margin-bottom": "0px",
                        "font-weight": "bold",
                        # "border": "1px", "border-style": "solid",
                    }
                ),
            ],
            # className="center_block_hor",
            style={"display": "flex", "justify-content": "center"}
        ),
    )
    cardBody.children = [dataIDRow] + cardBody.children

    if figType != "QC":
        exportRow = dbc.Row(
            [
                dcc.Download(id=returnIDDict(type="Download", function="Download", **idDict)),
                dbc.Col(
                    dbc.Button(
                        "Export Data",
                        id=returnIDDict(type="Button", function="Submit", **idDict),
                        n_clicks=0, style={"border-radius": "0.25rem"}
                    ),
                    style={"display": "flex", "justify-content": "flex-end"},
                    # width={"size": 6}
                )
            ],
            # justify="flex-end",
            style={"margin-top": "5px"}
        )
        cardBody.children.append(exportRow)
    else:
        exportRow = dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Filter Cells",
                        id=returnIDDict(type="Button", function="Submit", **idDict),
                        n_clicks=0, style={"border-radius": "0.25rem"},
                    ),
                    style={"display": "flex", "justify-content": "flex-end"},
                    # width={"size": 6}
                )
            ],
            # justify="flex-end",
            style={"margin-top": "5px"}
        )
        cardBody.children.append(exportRow)

    figCard = dbc.Card([cardBody], style={"border": "none"})
    return figCard


def returnQCCardBody(attributes, **idDict):
    def returnQCPlot(IDDict, x_slider=True, y_slider=True, size=4):
        return dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id=returnIDDict(**IDDict),
                                style={
                                    "padding": "25px 25px 0px 0px",
                                    "height": "500px"
                                },
                                config=dict(
                                    toImageButtonOptions=dict(
                                        format="svg",
                                        height=500,
                                        width=500,
                                    ),
                                    displaylogo=False,
                                    modeBarButtonsToRemove=[
                                        "zoom", "pan", "select", "lasso2d",
                                        "zoomIn", "zoomOut", "autoScale",
                                    ],
                                ),
                            ),
                            width={"size": 11},  # the style of default range slider

                        ),
                        dbc.Col(
                            dcc.RangeSlider(
                                id=returnIDDict(type='RangeSlider', axis="y", **IDDict),
                                min=None, max=None, value=[None, None],
                                vertical=True, verticalHeight=500,
                                # tooltip={"placement": "bottom", "always_visible": True},
                            ) if y_slider else None,
                            width={"size": 1},
                            style={"margin-left": "-25px"}
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.RangeSlider(
                                id=returnIDDict(type='RangeSlider', axis="x", **IDDict),
                                min=None, max=None, value=[None, None],
                                vertical=False,
                                # tooltip={"placement": "bottom", "always_visible": True},
                            ) if x_slider else None,
                        ),
                        dbc.Col(width={"size": 1})
                    ]
                )
            ],
            width={"size": size}
        )

    def returnController(label, inputIndex, size=3):
        return dbc.Col(
            dbc.InputGroup(
                children=[
                    dbc.InputGroupText(
                        label,
                        id=returnIDDict(type="Button", inputIndex=inputIndex, **idDict),
                        class_name="navButton inputGroup_label_inputText",
                        style={
                            "height": "36px", "line-height": "36px",
                            "width": "60%", "padding": "0 3px",
                            "justify-content": "center",
                        }
                    ),
                    dbc.Input(
                        id=returnIDDict(type="Input", inputIndex=inputIndex, **idDict),
                        style={
                            "height": "36px", "line-height": "36px",
                            "width": "30%", "padding": "0 3px",
                            "justify-content": "center",
                        },
                        disabled=True,
                    ),
                ],
                id=returnIDDict(type="InputGroup", inputIndex=inputIndex, **idDict),
            ),
            width={"size": size},
        )

    cardBody = []
    size = int(12/len(attributes))
    graphs = []
    if "UMI Counts" in attributes:
        graphs.append(returnQCPlot(
            returnIDDict(graphIndex=0, name="UMI Counts", **idDict), x_slider=False, y_slider=True, size=size,
        ))
    if "Gene Counts" in attributes:
        graphs.append(returnQCPlot(
            returnIDDict(graphIndex=1, name="Gene Counts", **idDict), x_slider=False, y_slider=True, size=size,
        ))
    if "MT PCT" in attributes:
        graphs.append(returnQCPlot(
            returnIDDict(graphIndex=2, name="MT PCT", **idDict), x_slider=False, y_slider=True, size=size,
        ))
    cardBody.append(dbc.Row(graphs))

    size = int(12/(len(attributes)+1))
    row = []
    inputIndex = 0
    if "UMI Counts" in attributes:
        row.append(returnController("UMI Counts", inputIndex, size))
        inputIndex += 1
    if "Gene Counts" in attributes:
        row.append(returnController("Gene Counts", inputIndex, size))
        inputIndex += 1
    if "MT PCT" in attributes:
        row.append(returnController("MT PCT", inputIndex, size))
        inputIndex += 1
    row.append(returnController("Total", inputIndex, size))
    cardBody.append(dbc.Row(row, style={"margin-top": "10px"}))

    return dbc.CardBody(cardBody)


def returnGeneExpressionCardBody(**idDict):
    """
    return a gene expression figure with dropdown controller based on inputMulti,
    :param inputMulti: whether to allow show multiply gene expression
    :param idDict: id dict
    :return: abc.Card body component
    """
    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=500,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=["zoom", "pan", "select", "lasso2d", "zoomIn", "zoomOut", "autoScale"],
        )
    ))
    cardBody.append(graph)

    dropdownLabels = ["Gene name", "Embedding"]
    cardBody.append(returnDropdownRow(dropdownLabels, **idDict))

    return dbc.CardBody(cardBody)


def returnGeneDotCardBody(**idDict):
    """
    return a gene expression figure with dropdown controller based on inputMulti,
    :param inputMulti: whether to allow show multiply gene expression
    :param idDict: id dict
    :return: abc.Card body component
    """
    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=500,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=["zoom", "pan", "select", "lasso2d", "zoomIn", "zoomOut", "autoScale"],
        )
    ))
    cardBody.append(graph)

    inputGroup = dbc.Row(
        [
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(
                            "Gene Name", className="inputGroup_label_inputText",
                            style={
                                "height": "41px", "line-height": "41px",
                                "width": "15%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                        dcc.Dropdown(
                            options=[],
                            style={"width": "85%"},  # class name was set to select-controller
                            id=returnIDDict(type="Dropdown", dropDownIndex=0, **idDict),
                            **{"clearable": False, "multi": True},
                        ),
                    ],
                ),
                width=9
            ),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(
                            "Annotation", className="inputGroup_label_inputText",
                            style={
                                "height": "41px", "line-height": "41px",
                                # "height": "36px", "line-height": "36px",
                                "width": "40%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                        dcc.Dropdown(
                            options=[],
                            style={"width": "60%", "height": "41px"},
                            id=returnIDDict(type="Dropdown", dropDownIndex=1, **idDict),
                            **{"clearable": False, "multi": False},
                        ),
                    ],
                ),
                width=3
            ),
        ],

    )
    cardBody.append(inputGroup)

    inputGroup = dbc.Row(

        style={"margin-top": "10px"}
    )
    cardBody.append(inputGroup)

    return dbc.CardBody(cardBody)


def returnCellEmbeddingCardBody(**idDict):
    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=500,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=["zoom", "autoScale"],
        ),
    ))
    cardBody.append(graph)
    dropdownLabels = ["Embedding", "Annotation"]
    cardBody.append(returnDropdownRow(dropdownLabels, **idDict))
    return dbc.CardBody(cardBody)


def returnCellStatCardBody(**idDict):
    """
    return a hist figure with a slider/multi-box controller based on dataType
    :param dataType: the data type shown in this figure
    :param idDict: id dict
    :return: abc.Card body component
    """
    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=500,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=["zoom", "pan", "select", "lasso2d", "zoomIn", "zoomOut", "autoScale"],
        ),
    ))
    cardBody.append(graph)

    dropdownLabels = ["Annotation", "Feature"]
    cardBody.append(returnDropdownRow(dropdownLabels, **idDict))
    return dbc.CardBody(cardBody)


def returnMarkerGeneIdentificationCardBody(**idDict):
    def returnInputGroupForGroups(label):
        labelDict = dict(
            className="navButton inputGroup_label_inputText",
            style={
                "height": "36px", "line-height": "36px",
                "width": "45%", "padding": "0 3px",
                "justify-content": "center",
            }
        )
        inputDict = dict(clearable=False, style={"width": "55%"})
        colWidth = 4

        inputGroupCol = dbc.Col(
            dbc.InputGroup(
                [
                    dbc.Button(label, id=returnIDDict(type="Button", label=label, **idDict), **labelDict),
                    dcc.Dropdown(id=returnIDDict(type="Dropdown", label=label, **idDict), **inputDict),
                ]
            ),
            width=colWidth
        )
        return inputGroupCol

    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=1000,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=["zoom", "pan", "select", "lasso2d", "zoomIn", "zoomOut", "autoScale"],
        ),
    ))
    cardBody.append(graph)

    controllerRow = dbc.Row(
        [
            dcc.Store(id=returnIDDict(type="Store", label="Group A", **idDict)),
            dcc.Store(id=returnIDDict(type="Store", label="Group B", **idDict)),
            dbc.Col(
                [
                    returnInputGroup("Annotation", **returnIDDict(label="Annotation", **idDict)),
                ],
                width=4
            ),
            returnInputGroupForGroups("Group A"),
            returnInputGroupForGroups("Group B")
        ]
    )
    cardBody.append(controllerRow)

    controllerRow = dbc.Row(
        [
            dbc.Col(
                dbc.InputGroup(
                    children=returnInputGroup(
                        "Raw Annotation", dropdownDict={"clearable": False},
                        dropdownIndex=0, **idDict  # these parameters will be treated as a new idDict
                    ),
                    id=returnIDDict(type="InputGroup", dropdownIndex=0, **idDict)
                ),
                width={"size": 4},
            ),
            dbc.Col(
                dbc.InputGroup(
                    children=[
                        dbc.Button(
                            "New Annotation",
                            id=returnIDDict(type="Button", inputIndex=1, **idDict),
                            class_name="navButton inputGroup_label_inputText",
                            style={
                                "height": "36px", "line-height": "36px",
                                "width": "60%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                        dbc.Input(
                            id=returnIDDict(type="Input", inputIndex=1, **idDict),
                            style={
                                "height": "36px", "line-height": "36px",
                                "width": "30%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                    ],
                    id=returnIDDict(type="InputGroup", inputIndex=1, **idDict),
                ),
                width={"size": 4},
            ),
        ],
        style={"margin-top": "10px"}
        # style={"display": "none"}
    )
    cardBody.append(controllerRow)

    cardBody.append(dcc.Store(id=returnIDDict(type="Store", function="Marker Gene", **idDict)))

    return dbc.CardBody(cardBody)


def returnMarkerGeneEvaluationCardBody(**idDict):
    cardBody = []

    controllerRow = dbc.Row(
        [
            dbc.Col(
                [
                    returnInputGroup("Marker Source", **returnIDDict(label="Marker Source", **idDict)),
                ],
                width=6
            ),
            dbc.Col(
                [
                    returnInputGroup("Species", **returnIDDict(label="Species", **idDict)),
                ],
                width=6
            ),
        ]
    )
    cardBody.append(controllerRow)

    graph = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", graphIndex=0, **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=[
                            "zoom", "pan", "select", "lasso2d",
                            "zoomIn", "zoomOut", "autoScale",
                        ],
                    ),
                ),
                width={"size": 6},
            ),
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", graphIndex=1, **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=[
                            "zoom", "pan", "select", "lasso2d",
                            "zoomIn", "zoomOut", "autoScale",
                        ],
                    ),
                ),
                width={"size": 6},
            ),
        ]
    )
    cardBody.append(graph)

    controllerRow = dbc.Row(
        [
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(
                            "Cell Type", className="inputGroup_label_inputText",
                            style={
                                "height": "36px", "line-height": "36px",
                                "width": "14%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                        dcc.Dropdown(
                            options=[],
                            style={"width": "86%"},  # class name was set to select-controller
                            id=returnIDDict(type="Dropdown", label="Cell Type", **idDict),
                        ),
                    ]
                ),
                width=12
            ),

        ],
    )
    cardBody.append(controllerRow)

    controllerRow = dbc.Row(
        [
            dbc.Col(
                [
                    returnInputGroup("Cluster Name", **returnIDDict(label="Cluster Name", **idDict)),
                ],
                width=4
            ),
            dbc.Col(
                [
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(
                                "Gene Number", className="inputGroup_label_inputText",
                                style={
                                    "height": "36px", "line-height": "36px",
                                    "width": "45%", "padding": "0 3px",
                                    "justify-content": "center",
                                }
                            ),
                            dcc.Input(
                                style={"width": "55%"},  # class name was set to select-controller
                                id=returnIDDict(type="Input", label="Gene Number", **idDict),
                            ),
                        ]
                    )
                ],
                width=4
            ),
            dbc.Col(
                dbc.InputGroup(
                    children=[
                        dbc.Button(
                            "Annotation",
                            id=returnIDDict(type="Button", inputIndex=0, **idDict),
                            class_name="navButton inputGroup_label_inputText",
                            style={
                                "height": "36px", "line-height": "36px",
                                "width": "45%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                        dbc.Input(
                            id=returnIDDict(type="Input", inputIndex=0, **idDict),
                            style={
                                "height": "36px", "line-height": "36px",
                                "width": "55%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                    ],
                    id=returnIDDict(type="InputGroup", inputIndex=0, **idDict),
                ),
                width={"size": 4},
            ),
        ],
        style={"margin-top": "10px"}
    )
    cardBody.append(controllerRow)

    return dbc.CardBody(cardBody)


def returnExpressionSimilaritySearchCardBody(**idDict):
    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=500,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=[
                "zoom", "pan", "select", "lasso2d",
                "zoomIn", "zoomOut", "autoScale"
            ],
        ),
    ))
    cardBody.append(graph)

    dropdownLabels = ["Annotation", "Gene Name"]
    cardBody.append(returnDropdownRow(dropdownLabels, **idDict))
    return dbc.CardBody(cardBody)


def returnAnnotationEvaluationCardBody(**idDict):
    cardBody = []
    graph = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", graphIndex=0, **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=[
                            "zoom", "pan", "select", "lasso2d",
                            "zoomIn", "zoomOut", "autoScale",
                        ],
                    ),
                ),
                width={"size": 6},
            ),
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", graphIndex=1, **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=[
                            "zoom", "pan", "select", "lasso2d",
                            "zoomIn", "zoomOut", "autoScale",
                        ],
                    ),
                ),
                width={"size": 6},
            ),
        ]
    )
    cardBody.append(graph)

    controllerRow = dbc.Row(
        [
            dbc.Col(
                [
                    returnInputGroup("Cell Cluster", **returnIDDict(label="Cell Cluster", **idDict)),
                ],
                width=3
            ),
            dbc.Col(
                dbc.InputGroup(
                    [
                        dbc.InputGroupText(
                            "Gene Number", className="inputGroup_label_inputText",
                            style={
                                "height": "36px", "line-height": "36px",
                                "width": "45%", "padding": "0 3px",
                                "justify-content": "center",
                            }
                        ),
                        dcc.Input(
                            style={"width": "55%"},  # class name was set to select-controller
                            id=returnIDDict(type="Input", label="Gene Number", **idDict),
                        )
                    ],
                ),
                width=3
            ),
            dbc.Col(
                [
                    returnInputGroup("Gene Name", **returnIDDict(label="Gene Name", **idDict)),
                ],
                width=3
            ),
            dbc.Col(
                [
                    returnInputGroup("Embedding", **returnIDDict(label="Embedding", **idDict)),
                ],
                width=3
            ),
        ]
    )
    cardBody.append(controllerRow)
    return dbc.CardBody(cardBody)


def returnMarkerGeneScoringCardBody(**idDict):
    def returnInputGroupForGroups(label, colWidth=6, **idKwargs, ):
        labelDict = dict(
            className="navButton inputGroup_label_inputText",
            style={
                "height": "36px", "line-height": "36px",
                "width": "55%", "padding": "0 3px",
                "justify-content": "center",
            }
        )
        inputDict = dict(clearable=False, style={"width": "45%"})


        inputGroupCol = dbc.Col(
            dbc.InputGroup(
                [
                    dbc.Button(label, id=returnIDDict(type="Button", label=label, **idKwargs), **labelDict),
                    dcc.Dropdown(id=returnIDDict(type="Dropdown", label=label, **idKwargs), **inputDict),
                ]
            ),
            width=colWidth,
        )
        return inputGroupCol

    cardBody = [
        dbc.Row(
            [
                returnInputGroupForGroups("Marker Source", colWidth=4, **idDict),
                returnInputGroupForGroups("Source Name", colWidth=8, **idDict),
            ],
            style={"margin-top": "10px"}
        )
    ]

    graph = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", graphIndex=0, **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=[
                            "zoom", "pan", "select", "lasso2d",
                            "zoomIn", "zoomOut", "autoScale",
                        ],
                    ),
                ),
                width={"size": 6},
            ),
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", graphIndex=1, **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=[
                            "zoom", "pan", "select", "lasso2d",
                            "zoomIn", "zoomOut", "autoScale",
                        ],
                    ),
                ),
                width={"size": 6},
            ),
        ],
    )
    cardBody.append(graph)

    rowChildren = [
        dbc.Col(
            dbc.InputGroup(
                children=returnInputGroup(
                    "Cell Cluster", dropdownDict={"clearable": False},
                    dropdownIndex=0, **idDict  # these parameters will be treated as a new idDict
                ),
                id=returnIDDict(type="InputGroup", dropdownIndex=0,  **idDict)
            ),
            width={"size": 3},
        ),
        dbc.Col(
            dbc.InputGroup(
                children=[
                    dbc.Button(
                        "Gene Number",
                        id=returnIDDict(type="Button", inputIndex=1, **idDict),
                        class_name="navButton inputGroup_label_inputText",
                        style={
                            "height": "36px", "line-height": "36px",
                            "width": "60%", "padding": "0 3px",
                            "justify-content": "center",
                        }
                    ),
                    dbc.Input(
                        id=returnIDDict(type="Input", inputIndex=1, **idDict),
                        style={
                            "height": "36px", "line-height": "36px",
                            "width": "30%", "padding": "0 3px",
                            "justify-content": "center",
                        }
                    ),
                ],
                id=returnIDDict(type="InputGroup", inputIndex=1, **idDict),
            ),
            width={"size": 3},
        ),
        dbc.Col(
            dbc.InputGroup(
                returnInputGroup(
                    "Cell Type", dropdownDict={"clearable": False},
                    dropdownIndex=2, **idDict  # these parameters will be treated as a new idDict
                ),
                id=returnIDDict(type="InputGroup", inputIndex=2, **idDict),
            ),
            width={"size": 3},
        ),
        dbc.Col(
            dbc.InputGroup(
                children=[
                    dbc.Button(
                        "Annotation",
                        id=returnIDDict(type="Button", inputIndex=3, **idDict),
                        class_name="navButton inputGroup_label_inputText",
                        style={
                            "height": "36px", "line-height": "36px",
                            "width": "60%", "padding": "0 3px",
                            "justify-content": "center",
                        }
                    ),
                    dbc.Input(
                        id=returnIDDict(type="Input", inputIndex=3, **idDict),
                        style={
                            "height": "36px", "line-height": "36px",
                            "width": "30%", "padding": "0 3px",
                            "justify-content": "center",
                        }
                    ),
                ],
                id=returnIDDict(type="InputGroup", inputIndex=3, **idDict),
            ),
            width={"size": 3},
        ),
    ]
    cardBody.append(dbc.Row(rowChildren))
    return dbc.CardBody(cardBody)


def returnCellSelectionCardBody(**idDict):
    import pandas as pd
    from dash import dash_table
    # refer to https://github.com/plotly/dash-table/issues/436
    # Empty DataFrame to start the DataTable
    # (workaround for bug in DataTable - https://github.com/plotly/dash-table/issues/436#issuecomment-615924723)
    start_table_df = pd.DataFrame(columns=[''])

    cardBody = []
    graph = dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id=returnIDDict(type="Graph", **idDict),
                    config=dict(
                        toImageButtonOptions=dict(
                            format="svg",
                            height=500,
                            width=500,
                        ),
                        displaylogo=False,
                        modeBarButtonsToRemove=["zoom", "autoScale"],
                    ),
                ),
                width={"size": 6},
            ),
            dbc.Col(
                dash_table.DataTable(
                    id=returnIDDict(type="Table", **idDict),
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
                    style_table={'height': "450px", 'overflowX': 'auto', "max-width": "100%", "margin-bottom": "-25px"},
                    # defaults to 500, each row takes up 30px
                    style_header={"height": "50px"},
                    style_cell={
                        'height': '40px', 'whiteSpace': 'normal',
                        # all three widths are needed
                        'width': '200px', 'minWidth': '200px', 'maxWidth': '200px',
                    },
                ),
                width={"size": 6},
                style={"padding-top": "5px"},
            )
        ],
    )
    cardBody.append(graph)
    dropdownLabels = ["Embedding", "Annotation", "Table Content"]
    cardBody.append(returnDropdownRow(dropdownLabels, **idDict))

    def returnInputGroupForGroups(label):
        labelDict = dict(
            className="inputGroup_label_inputText",
            style={
                "height": "36px", "line-height": "36px",
                "width": "45%", "padding": "0 3px",
                "justify-content": "center",
            }
        )
        inputDict = dict(clearable=False, style={"width": "55%"})
        colWidth = 4

        inputGroupCol = dbc.Col(
            dbc.InputGroup(
                [
                    dbc.Button(label, id=returnIDDict(type="Button", label=label, **idDict), **labelDict),
                    dcc.Dropdown(id=returnIDDict(type="Dropdown", label=label, **idDict), **inputDict),
                ]
            ),
            width=colWidth
        )
        return inputGroupCol

    controllerRow = dbc.Row(
        [
            returnInputGroupForGroups("Add Column"),
            returnInputGroupForGroups("Remove Column"),
            dbc.Col(
                dbc.Button(
                    "Select in Cell Table",
                    id=returnIDDict(type="Button", label="Select All", **idDict),
                    n_clicks=0,
                    style={
                        "height": "36px", "line-height": "36px",
                        "width": "100%",
                        "padding": "0 3px",
                        "justify-content": "center",
                        "border-radius": "0.25rem",
                    },
                ),
                # style={"display": "flex", "justify-content": "flex-end"},
                width={"size": 4}
            ),
        ],
        style={"margin-top": "5px"}
    )
    cardBody.append(controllerRow)
    return dbc.CardBody(cardBody)


def returnVisualizationCardBody(**idDict):
    cardBody = []
    graph = dbc.Row(dcc.Graph(
        id=returnIDDict(type="Graph", **idDict),
        config=dict(
            toImageButtonOptions=dict(
                format="svg",
                height=500,
                width=500,
            ),
            displaylogo=False,
            modeBarButtonsToRemove=[
                "zoom", "pan", "select", "lasso2d",
                "zoomIn", "zoomOut", "autoScale"
            ],
        ),
    ))
    cardBody.append(graph)

    dropdownLabels = ["Cell Cluster"]
    row = returnDropdownRow(dropdownLabels, **idDict)
    row.children[0].width["size"] = 6
    cardBody.append(row)

    return dbc.CardBody(cardBody)


def returnDropdownRow(dropdownLabels, dropdownDict={"clearable": False}, **idDict):
    dropdownList = []
    assert len(dropdownLabels) in [1, 2, 3, 4, 6, 12], """number of dropdown group should be 2, 3, 4, 6, 12"""
    for dropdownLabel, dropdownIndex in zip(dropdownLabels, range(0, len(dropdownLabels))):
        inputGroup = dbc.InputGroup(id=returnIDDict(type="InputGroup", dropDownIndex=dropdownIndex, **idDict))
        inputGroup.children = returnInputGroup(
            dropdownLabel, dropdownDict=dropdownDict,
            dropDownIndex=dropdownIndex, **idDict  # these parameters will be treated as a new idDict
        )
        dropdownList.append(
            dbc.Col(inputGroup, width={"size": int(12 / len(dropdownLabels))})
        )
    return dbc.Row(dropdownList, style={"margin-top": "5px"})


def returnButtonRow(buttonLabels, **idDict):
    buttonList = []
    assert len(buttonLabels) in [1, 2, 3, 4, 6, 12], """number of button should be 2, 3, 4, 6, 12"""
    for buttonLabel, buttonIndex in zip(buttonLabels, range(0, len(buttonLabels))):
        button = dbc.Button(
            buttonLabel,
            id=returnIDDict(type="Button", buttonIndex=buttonIndex, **idDict),
            className="navButton",
            active=False, n_clicks=0
        )
        buttonList.append(
            dbc.Col(button, width={"size": int(12 / len(buttonLabels))})
        )
    return dbc.Row(buttonList, justify="end", style={"margin-top": "5px"})


def returnInputGroup(inputLabel, options=None, dropdownDict={}, **idDict):
    optionsDictList = [{"label": option, "value": option} for option in options] if options is not None else []

    inputGroup = dbc.InputGroup(
        [
            dbc.InputGroupText(
                inputLabel, className="inputGroup_label_inputText",
                style={
                    "height": "36px", "line-height": "36px",
                    "width": "45%", "padding": "0 3px",
                    "justify-content": "center",
                }
            ),
            dcc.Dropdown(
                options=optionsDictList,
                style={"width": "55%"},  # class name was set to select-controller
                id=returnIDDict(type="Dropdown", **idDict),
                **dropdownDict,
            ),
        ]
    )
    return inputGroup
