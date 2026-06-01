#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: moduleSettings.py
@time: 2024/11/9 13:39
"""

"""
    navBar
        card
            form
                line
                    label_input
        table
"""
defaultLabelClass = "inputGroup_label collapseCard_row_height collapseCard_label_width"
defaultInputClass = "collapseCard_row_height collapseCard_input_width"


def modifyClassName(defaultClass, classNames):
    if isinstance(classNames, list):
        return defaultClass + " " + " ".join(classNames)
    else:
        return defaultClass + " " + classNames


def returnInputLine(
        label_name, input_name, labelClass=defaultLabelClass, inputClass=defaultInputClass,
        labelKwargs={"setID": False}, inputKwargs={"setID": True}
):
    """Change label name for more accurate presentation"""
    return [
        {
            "label_name": input_name, "show_name": label_name, "type": "Label",
            "component_kwargs": {"children": label_name, "class_name": labelClass},
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "Input",
            "component_kwargs": {"class_name": inputClass},
            "kwargs": inputKwargs,
        }
    ]


def returnDropdownLine(
        label_name, input_name, labelClass=defaultLabelClass,
        labelKwargs={"setID": False}, inputKwargs={"setID": True},
):
    return [
        {
            "label_name": input_name, "show_name": label_name, "type": "Label",
            "component_kwargs": {"children": label_name, "class_name": labelClass},
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "Dropdown",
            "component_kwargs": {"style": {"width": "60%"}},
            "kwargs": inputKwargs,
        }
    ]


def returnCheckLine(label_name, input_name, labelKwargs={"setID": False}, inputKwargs={"setID": True}):
    """Label name is shown in check list"""
    return [
        {
            "label_name": input_name, "show_name": label_name, "type": "Label",
            "component_kwargs": {"children": None, "style": {"width": "10%"}},
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "Checklist",
            "component_kwargs": {
                "options": [dict(label=label_name, value=input_name)], "value": input_name,
                "style": {"width": "90%"}, "labelStyle":  {"display": "flex", "align-items": "center"},
            },
            "kwargs": inputKwargs,
        }
    ]

def returnCheckLine_button(label_name, input_name, labelKwargs={"setID": False}, inputKwargs={"setID": True}):
    """Label name is shown in check list"""
    return [
        {
            "label_name": input_name, "show_name": label_name, "type": "Checklist",
            "component_kwargs": {
                "options": [
                    dict(
                        label="",
                        value=input_name
                    )
                ],
                "value": input_name,
                "style": {"margin-left": "33%"}, "labelStyle":  {"display": "flex", "align-items": "center"},
            },
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "Button",
            "component_kwargs": {
                "children": label_name,
                # "active": True,
                "class_name": modifyClassName(defaultInputClass, ["inputGroup_label_inputText"]),
                "style": {"padding": "0", "border-radius": "0.25rem"}
            },
            "kwargs": inputKwargs,
        },
    ]


def returnSliderLine(
    label_name, input_name, sliderKwargs=dict(min=0, max=1, step=0.1, value=0.5),
    labelKwargs={"setID": False}, inputKwargs={"setID": True}
):
    # sliderMin, sliderMax, sliderStep, sliderValue = (
    #     sliderKwargs.get("min", 0), sliderKwargs.get("max", 1),
    #     sliderKwargs.get("step", 0.1), sliderKwargs.get("value", 0.5)
    # )
    if "className" not in sliderKwargs:
        sliderKwargs["className"] = defaultInputClass
    if "tooltip" not in sliderKwargs:
        sliderKwargs["tooltip"] = {"placement": "bottom", "always_visible": True, }
    if "marks" not in sliderKwargs:
        sliderKwargs["marks"] = None
    return [
        {
            "label_name": input_name, "show_name": label_name, "type": "Label",
            "component_kwargs": {"children": label_name, "class_name": defaultLabelClass},
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "Slider",
            "component_kwargs": sliderKwargs,
            "kwargs": inputKwargs,
        },
    ]


def returnRangerSlider(
    label_name, input_name, labelKwargs={"setID": False}, inputKwargs={"setID": True}, label=False,
    # sliderKwargs=dict(min=0, max=1, step=0.1, value=0.5),
    sliderKwargs=dict(min=0, max=1, step=0.1)
):
    return [
        {
            "label_name": input_name, "show_name": label_name, "type": "Label",
            "component_kwargs": {
                "children": label_name, "class_name": defaultLabelClass,
                "style": {"width": "0"},
            },
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "RangeSlider",
            # "component_kwargs": sliderKwargs,
            "component_kwargs": dict(min=0, max=1, step=0.1),
            "kwargs": inputKwargs,
        },
    ]


def returnSubmitLine(withDownload=False, submitKwargs={"setID": True}):
    labelType = "Download" if withDownload else None
    buttonText = "Submit" if not withDownload else "Download"
    return [
        {
            "label_name": "Submit", "show_name": "Submit", "type": labelType,
            "component_kwargs": {},
            "kwargs": {"setID": False},
        },
        {
            "label_name": "Submit", "show_name": buttonText, "type": "Button",
            "component_kwargs": {
                "children": buttonText, "n_clicks": 0,
                "class_name": modifyClassName(defaultInputClass, ["inputGroup_label_inputText"]),
                "style": {"padding": "0", "border-radius": "0.25rem", "margin-left": "40%"}
                # the css was failed in btn css
            },
            "kwargs": submitKwargs,
        }
    ]

def returnButtonLine(label_name, input_name, labelKwargs={"setID": False}, inputKwargs={"setID": True}):
    return [
        {
            "label_name": "Submit", "show_name": "Submit", "type": "Label",
            "component_kwargs": {"style": {"margin-bottom": "0.5rem"}},
            "kwargs": labelKwargs,
        },
        {
            "label_name": input_name, "show_name": label_name, "type": "Button",
            "component_kwargs": {
                "children": label_name, "n_clicks": 0, "active": True,
                "class_name": modifyClassName(defaultInputClass, ["navButton", "inputGroup_label_inputText"]),
                "style": {"padding": "0", "border-radius": "0.25rem", "margin-left": "40%", "margin-bottom": "0.5rem"}
                # the css was failed in btn css
            },
            "kwargs": inputKwargs,
        }
    ]


######################################################################################################
uploadForm = {
    "form_name": "Upload", "show_name": "Upload",
    "lines": [
        returnDropdownLine(label_name="Data Source", input_name="Data Source"),
        [
            {
                "label_name": "Local Data", "show_name": "Local Data", "type": "Label",
                "component_kwargs": {
                    "children": "Local Data", "class_name": defaultLabelClass,
                    # "style": {"height": "72px", "line-height": "72px"}
                },
                "kwargs": {"setID": True},
            },
            {
                "label_name": "Local Data", "show_name": "Local Data", "type": "Upload",
                "component_kwargs": {"children": "Upload Data", "style": {"text-align": "center"}},
            },
        ],
        returnDropdownLine(label_name="History Data", input_name="History Data", labelKwargs={"setID": True}),
        returnDropdownLine(label_name="Current Data", input_name="Current Data", labelKwargs={"setID": True}),
        returnDropdownLine(label_name="Object Name", input_name="Object Name", labelKwargs={"setID": True}),
        returnSubmitLine(),
    ],
}
removeForm = {
    "form_name": "Remove", "show_name": "Remove",
    "lines": [
        returnInputLine(label_name="Current ID", input_name="Current ID"),
        returnDropdownLine(label_name="Data ID", input_name="Data ID"),
        returnSubmitLine(),
    ]
}
changeForm = {
    "form_name": "Change", "show_name": "Change",
    "lines": [
        returnInputLine(label_name="Current ID", input_name="Current ID"),
        returnDropdownLine(label_name="Data ID", input_name="Data ID"),
        returnSubmitLine(),
    ]
}
annotationTypeForm = {
    "form_name": "Annotation Type", "show_name": "Annotation Type",
    "lines": [
        returnDropdownLine(label_name="Annotation", input_name="Annotation"),
        returnDropdownLine(label_name="Data Type", input_name="Data Type"),
        returnSubmitLine(),
    ]
}
dataSettingCard = {
    "card_name": "Data Settings", "show_name": "Data Settings",
    "forms": [uploadForm, removeForm, changeForm, annotationTypeForm]
}

######################################################################################################
QCForm = {
    "form_name": "QC", "show_name": "QC",
    "lines": [
        # returnCheckLine_button(label_name="Cells Counts", input_name="Cell Counts", labelKwargs={"setID": True}),
        # returnRangerSlider(label_name="", input_name="Cell Counts"),
        # returnCheckLine_button(label_name="Cells Genes", input_name="Cell Genes", labelKwargs={"setID": True}),
        # returnRangerSlider(label_name="", input_name="Cell Genes"),
        # returnCheckLine_button(label_name="MT Pct", input_name="MT Pct", labelKwargs={"setID": True}),
        # returnRangerSlider(label_name="", input_name="MT Pct"),
        [
            {
                "label_name": "Attributes", "show_name": "Attributes", "type": "Label",
                "component_kwargs": {"children": None, "style": {"width": "10%"}},
                "kwargs": {"setID": False},
            },
            {
                "label_name": "Attributes", "show_name": "Attributes", "type": "Checklist",
                "component_kwargs": {
                    "options": [
                        dict(label="UMI Counts", value="UMI Counts"),
                        dict(label="Gene Counts", value="Gene Counts"),
                        dict(label="MT Pct", value="MT PCT"),
                    ], "value": ["UMI Counts", "Gene Counts", "MT PCT"],
                    "style": {"width": "90%"}, "labelStyle":  {"display": "flex", "align-items": "center"},
                },
                "kwargs": {},
            }
        ],
        returnSubmitLine(),
    ]
}
normalizationForm = {
    "form_name": "Normalization", "show_name": "Normalization",
    "lines": [
        # returnDropdownLine(label_name="Layer", input_name="Layer"),
        returnInputLine(label_name="Target Sum", input_name="Target Sum"),
        returnCheckLine(label_name="Exclude Highly Expressed", input_name="Exclude Highly Expressed"),
        returnCheckLine(label_name="Log1P", input_name="Log1P"),
        returnSubmitLine(),
    ]
}
hvgDetectionForm = {
    "form_name": "HVG Detection", "show_name": "HVG Detection",
    "lines": [
        returnDropdownLine(label_name="Flavor", input_name="Flavor"),
        returnInputLine(label_name="Top Genes", input_name="Top Genes"),
        returnSubmitLine(),
    ]
}
dimensionReductionForm = {
    "form_name": "Dimension Reduction", "show_name": "Dimension Reduction",
    "lines": [
        returnDropdownLine(label_name="Method", input_name="Method"),
        returnInputLine(label_name="N PCs", input_name="N PCs", labelKwargs={"setID": True}),
        returnInputLine(label_name="N Neighbors", input_name="N Neighbors", labelKwargs={"setID": True}),
        returnInputLine(label_name="Min Dist", input_name="Min Dist", labelKwargs={"setID": True}),
        returnDropdownLine(label_name="Metric", input_name="Metric", labelKwargs={"setID": True}),
        returnSubmitLine(),
    ]
}

# submitForm = {
#     "form_name": "Submit", "show_name": "Submission",
#     "lines": [
#         # [
#         #     {
#         #         "label_name": "tipInfo", "show_name": "tipInfo", "type": "Label",
#         #         "component_kwargs": {},
#         #         "kwargs": {"setID": False},
#         #     },
#         #     {
#         #         "label_name": "tipInfo", "show_name": "tipInfo", "type": "FormText",
#         #         "component_kwargs": {
#         #             "children": "There are errors in the parameters from Preprocessing form, please check it!", "color": "secondary",
#         #             "style": {
#         #                 "text-align": "left", "margin-top": "5px", "margin-bottom": "5px", "margin-left": "5px",
#         #                 "display": "block", "color": "red",
#         #                 "font-size": "0.8em", "width": "100%"
#         #             }
#         #         },
#         #     }
#         # ],
#         returnSubmitLine(),
#     ],
# }
cellClusteringForm = {
    "form_name": "Cell Clustering", "show_name": "Cell Clustering",
    "lines": [
        returnDropdownLine(label_name="Processed By", input_name="Preprocessed"),
        returnDropdownLine(label_name="Cluster Name", input_name="Reference", labelKwargs={"setID": True}),
        returnDropdownLine(label_name="Method", input_name="Method", labelKwargs={"setID": True}),
        returnInputLine(label_name="Resolution", input_name="Resolution", labelKwargs={"setID": True}),
        returnSubmitLine()
    ]
}
preprocessingCard = {
    "card_name": "Preprocessing", "show_name": "Preprocessing",
    "forms": [
        QCForm,
        normalizationForm,
        hvgDetectionForm,
        dimensionReductionForm,
        cellClusteringForm,
        # submitForm
    ]
}

######################################################################################################
cellEmbeddingForm = {
    "form_name": "Cell Embedding", "show_name": "Cell Embedding",
    "lines": [
        returnDropdownLine(label_name="Embedding", input_name="Embedding"),
        returnDropdownLine(label_name="Annotation", input_name="Annotation"),
        returnSubmitLine(),
    ]
}
# cellStatForm = {
#     "form_name": "Cell Stat", "show_name": "Cell Stat",
#     "lines": [
#         returnDropdownLine(label_name="Annotation", input_name="x_Annotation"),
#         returnDropdownLine(label_name="Feature", input_name="y_Annotation"),
#         # # whether to scale data
#         # [
#         #     {
#         #         "label_name": "Scale", "show_name": "Scale", "type": "Label",
#         #         "component_kwargs": {
#         #             "children": "Scale",
#         #             "class_name": defaultLabelClass,
#         #             "style": {"height": "72px", "line-height": "72px"},
#         #         },
#         #         "kwargs": {"setID": False},
#         #     },
#         #     {
#         #         "label_name": "Scale", "show_name": "Scale", "type": "RadioItems",
#         #         "component_kwargs": {
#         #             "class_name": defaultInputClass,
#         #             "style": {"height": "72px"},
#         #             "value": "No",
#         #             "options": [
#         #                 dict(label="Yes", value="No"),
#         #                 dict(label="Yes", value="No")
#         #             ],
#         #         },
#         #         "kwargs": {"setID": True},
#         #     }
#         #
#         # ],
#         returnSubmitLine(),
#     ]
# }
geneEmbeddingForm = {
    "form_name": "Gene Embedding", "show_name": "Gene Embedding",
    "lines": [
        returnDropdownLine(label_name="Gene Name", input_name="Gene Name"),
        returnDropdownLine(label_name="Embedding", input_name="Embedding"),

        returnSubmitLine(),
    ]
}
geneDotForm = {
    "form_name": "Gene Dot", "show_name": "Gene Dot",
    "lines": [
        returnDropdownLine(label_name="Gene Name", input_name="Gene Name"),
        returnDropdownLine(label_name="Annotation", input_name="Annotation"),
        returnSubmitLine(),
    ]
}
dataVisualizationCard = {
    "card_name": "Data Visualization", "show_name": "Data Visualization",
    "forms": [
        cellEmbeddingForm,
        # cellStatForm,
        geneEmbeddingForm,
        geneDotForm
    ]
}

######################################################################################################
markerGeneIdentificationForm = {
    "form_name": "Marker Gene Identification", "show_name": "Marker Gene Identification",
    "lines": [
        returnDropdownLine(label_name="Annotation", input_name="Annotation"),
        [
            {
                "label_name": "Group A", "show_name": "Group A", "type": "Button",
                "component_kwargs": {
                    "children": "Group A",
                    "active": False,
                    "class_name": "navButton inputGroup_label_inputText",
                    "style": {
                        "height": "36px", "line-height": "36px", "justify-content": "center",
                        "width": "40%", "padding": "0 3px",
                        "margin-bottom": "0.5rem",
                    }
                },
                "kwargs": {"setID": True},
            },
            {
                "label_name": "Group A", "show_name": "Group A", "type": "Dropdown",
                "component_kwargs": {
                    "style": {"width": "60%"},
                    "disabled": True
                },
                "kwargs": {"setID": True},
            },
        ],
        [
            {
                "label_name": "Group B", "show_name": "Group B", "type": "Button",
                "component_kwargs": {
                    "children": "Group B",
                    "active": False,
                    "class_name": "navButton inputGroup_label_inputText",
                    "style": {
                        "height": "36px", "line-height": "36px", "justify-content": "center",
                        "width": "40%", "padding": "0 3px",
                        "margin-bottom": "0.5rem",
                    }
                },
                "kwargs": {"setID": True},
            },
            {
                "label_name": "Group B", "show_name": "Group B", "type": "Dropdown",
                "component_kwargs": {
                    "style": {"width": "60%"},
                    "disabled": True
                },
                "kwargs": {"setID": True},
            },
        ],
        returnSubmitLine()
    ]
}
markerGeneEvaluationForm = {
    "form_name": "Marker Gene Evaluation", "show_name": "Cell Identification",
    "lines": [
        # returnDropdownLine(label_name="Annotation", input_name="Annotation"),
        returnDropdownLine(label_name="Marker Source", input_name="Marker Source"),
        returnDropdownLine(label_name="Species", input_name="Species"),
        returnDropdownLine(label_name="Cluster Name", input_name="Cluster Name"),
        returnInputLine(label_name="Gene Number", input_name="Gene Number"),
        returnSubmitLine()
    ]
}
# expressionSimilaritySearch = {
#     "form_name": "Expression Similarity Search", "show_name": "Expression Similarity Search",
#     "lines": [
#         returnDropdownLine(label_name="Annotation", input_name="Annotation"),
#         returnDropdownLine(label_name="Gene Name", input_name="Gene Name"),
#         returnSubmitLine()
#     ]
# }
geneAnalysisCard = {
    "card_name": "Gene Analysis", "show_name": "Cell Annotation",
    "forms": [
        markerGeneIdentificationForm,
        markerGeneEvaluationForm,
        # clusterEvaluationForm,
        # expressionSimilaritySearch
    ]
}

######################################################################################################
# cellClusteringForm = {
#     "form_name": "Cell Clustering", "show_name": "Cell Clustering",
#     "lines": [
#         returnDropdownLine(label_name="Processed By", input_name="Preprocessed"),
#         returnDropdownLine(label_name="Cluster Name", input_name="Reference", labelKwargs={"setID": True}),
#         returnDropdownLine(label_name="Method", input_name="Method", labelKwargs={"setID": True}),
#         returnInputLine(label_name="Resolution", input_name="Resolution", labelKwargs={"setID": True}),
#         returnSubmitLine()
#     ]
# }
annotationEvaluationForm = {
    "form_name": "Annotation Evaluation", "show_name": "Annotation Evaluation",
    "lines": [
        returnDropdownLine(label_name="Cell Cluster", input_name="Cell Cluster"),
        returnInputLine(label_name="Gene Number", input_name="Gene Number"),
        returnDropdownLine(label_name="Embedding", input_name="Embedding"),
        returnSubmitLine()
    ]
}
clusterEvaluationForm = {
    "form_name": "Marker Gene Scoring", "show_name": "Reference Comparison",
    "lines": [
        returnDropdownLine(label_name="Marker Source", input_name="Marker Source"),
        returnDropdownLine(label_name="Source Name", input_name="Source Name"),
        returnDropdownLine(label_name="Cell Cluster", input_name="Cell Cluster"),
        returnInputLine(label_name="Gene Number", input_name="Gene Number"),
        returnSubmitLine()
    ]
}
evaluationValidationCard = {
    "card_name": "Evaluation and Validation", "show_name": "Annotation Validation",
    "forms": [
        annotationEvaluationForm,
        clusterEvaluationForm
    ]
}
######################################################################################################
cellSelectionForm = {
    "form_name": "Cell Selection", "show_name": "Cell Selection",
    "lines": [
        returnDropdownLine(label_name="Embedding", input_name="Embedding"),
        returnDropdownLine(label_name="Annotation", input_name="Annotation"),
        returnDropdownLine(label_name="Table Content", input_name="Table Content"),
        returnSubmitLine()
    ]
}
re_clusterForm = {
    "form_name": "Re-cluster", "show_name": "Cluster Refinement",
    "lines": [
        returnDropdownLine(label_name="Cluster", input_name="Cluster"),
        # returnInputLine(label_name="Prefix", input_name="Prefix"),
        returnButtonLine(label_name="Dimension Reduction", input_name="Dimension Reduction"),
        returnDropdownLine(label_name="Method", input_name="dimension_Method", labelKwargs={"setID": True}),
        returnInputLine(label_name="N PCs", input_name="N PCs", labelKwargs={"setID": True}),
        returnInputLine(label_name="N Neighbors", input_name="N Neighbors", labelKwargs={"setID": True}),
        returnInputLine(label_name="Min Dist", input_name="Min Dist", labelKwargs={"setID": True}),
        returnDropdownLine(label_name="Metric", input_name="Metric", labelKwargs={"setID": True}),
        returnButtonLine(label_name="Cell Clustering", input_name="Cell Reclustering"),
        returnDropdownLine(label_name="Method", input_name="Method", labelKwargs={"setID": True}),
        returnInputLine(label_name="Resolution", input_name="Resolution", labelKwargs={"setID": True}),
        returnSubmitLine()
    ]
}
reannotationForm = {
    "form_name": "Reannotation", "show_name": "Cluster Reannotation",
    "lines": [
        returnDropdownLine(label_name="Raw Name", input_name="Raw Name"),
        returnInputLine(label_name="New Name", input_name="New Name"),
        returnSubmitLine()
    ]
}
mergeDataForm = {
    "form_name": "Merge Data", "show_name": "Annotation Update",
    "lines": [
        returnInputLine(label_name="Source Data", input_name="Ref Data"),
        returnDropdownLine(label_name="Subset Data", input_name="Other Data"),
        returnSubmitLine(),
    ]
}
# annotationSnakeyForm = {
#     "form_name": "Visualization", "show_name": "Results Export",
#     "lines": [
#         returnDropdownLine(label_name="Cluster Name", input_name="Cluster Name"),
#         returnSubmitLine()
#     ]
# }
# cellSelectionForm = {
#     "form_name": "Cell Selection", "show_name": "Cell Selection",
#     "faker_form": True,
# }
# cellsTableForm = {
#     "form_name": "CellsTable", "show_name": "CellsTable",
#     "faker_form": True,
# }
cellReannotationCard = {
    "card_name": "Cell Reannotation", "show_name": "Cell Reannotation",
    "forms": [
        # cellsTableForm,
        cellSelectionForm, re_clusterForm,
        reannotationForm,
        mergeDataForm,
        # annotationSnakeyForm
    ],
}
######################################################################################################


######################################################################################################
leftNavBar = [
    dataSettingCard, preprocessingCard,
    dataVisualizationCard,
    # clusterAnalysisCard,
    geneAnalysisCard,
    # geneAnalysisCard, clusterAnalysisCard,
    evaluationValidationCard,
    cellReannotationCard
]
