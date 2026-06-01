#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_5_geneAnalysis.py
@time: 2024/11/13 10:35
"""
import json

import dash
import pandas as pd

from callbacks.callbacks_4_dataVisualization import *


@callback(
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group A", "type": "Button"
        },
        "active"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group A", "type": "Button"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group A", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group A", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group A", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group B", "type": "Button"
        },
        "active"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group B", "type": "Button"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group B", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group B", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Group B", "type": "Dropdown"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
        annotationDropdown=(
            Input(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Annotation", "type": "Dropdown"
                },
                "value"
            ),
        ),
        buttonGroup=(
            State(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Group A", "type": "Button"
                },
                "active"
            ),
            Input(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Group A", "type": "Button"
                },
                "n_clicks"
            ),
            State(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Group B", "type": "Button"
                },
                "active"
            ),
            Input(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Group B", "type": "Button"
                },
                "n_clicks"
            )
        ),
        dropdownValues=(
            State(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Group A", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": "Group B", "type": "Dropdown"
                },
                "value"
            ),
        ),
    ),
)
def returnMarkerGeneIdentificationForm(
        userSessionId, annotationDropdown, refresh_clusterHistoryRecorder, refresh_annotationTypeRecorder,
        buttonGroup, dropdownValues
):
    """
    return :
        dropdown [value, options, disabled]
        groupAButton [active, disabled],
        groupADropdown [value, options, disabled],
        groupBButton [active, disabled],
        groupBDropdown [value, options, disabled],
    """
    def returnAnnotationDropdown():
        annotationTypeRecorder = cellClickManager.annotationTypeRecorder
        annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotationDropdown(annotationDropdown[0])
        annotationOptions = returnDropdownOptions(annotationOptions)
        if annotationValue is None:
            return True, None, {"label": "No Reference", "value": None}
        else:
            return False, annotationValue, annotationOptions

    def returnGroupDropdown(group, annotationValue):
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        if clusterHistoryRecorder.refCol and annotationValue == clusterHistoryRecorder.refCol:
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
        else:
            adata = cellClickManager.returnAdata()
            annotationSeries = adata.obs[annotationValue]

        if group == "A":
            optionList = ["selected", "all"] + sorted(annotationSeries.unique())
        else:
            optionList = sorted(annotationSeries.unique()) + ["rest", "none"]
        group_options = returnDropdownOptions(optionList, sort=False)

        group_Value = dropdownValues[0] if group == "A" else dropdownValues[1]
        if group_Value is None or group_Value not in optionList:
            group_Value = optionList[2] if group == "A" else optionList[0]  # the first value in adata

        return group_Value, group_options

    (
        groupA_buttonActive, groupB_buttonActive,
        groupA_buttonDisabled, groupB_buttonDisabled,
        annotation_dropdownDisabled, groupA_dropdownDisabled, groupB_dropdownDisabled,
        annotation_dropdownValue, groupA_dropdownValue, groupB_dropdownValue,
        annotation_dropdownOptions, groupA_dropdownOptions, groupB_dropdownOptions
    ) = [dash.no_update] * 13
    if userSessionId is None:
        annotation_dropdownDisabled, groupA_dropdownDisabled, groupB_dropdownDisabled = [True] * 3
        groupA_buttonDisabled, GroupB_buttonDisabled = [True] * 2
    else:
        annotation_dropdownDisabled, annotation_dropdownValue, annotation_dropdownOptions = returnAnnotationDropdown()
        if annotation_dropdownValue is None:
            groupA_dropdownValue, groupA_dropdownOptions = None, []

            groupA_buttonDisabled, groupB_buttonDisabled = True, True
            groupA_buttonActive, groupB_buttonActive = False, False
        else:
            groupA_dropdownValue, groupA_dropdownOptions = returnGroupDropdown("A", annotation_dropdownValue)
            groupB_dropdownValue, groupB_dropdownOptions = returnGroupDropdown("B", annotation_dropdownValue)

            ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
            try:
                ctxId = json.loads(ctxIdStr)
                if ctxId["type"] == "Button":
                    clickButton = ctxId["label_name"]
                elif ctxId["type"] == "Dropdown" and ctxId["label_name"] == "Annotation":
                    clickButton = "Annotation"
                else:
                    clickButton = None
            except json.JSONDecodeError:
                clickButton = None

            groupA_buttonActive, n_clicks_A, groupB_buttonActive,  n_clicks_B = buttonGroup
            groupA_buttonDisabled = False
            if clickButton is None:
                pass
            elif clickButton == "Annotation":
                groupA_buttonActive = True
                groupB_buttonActive = False
                groupB_buttonDisabled = True
            elif clickButton == "Group A":
                groupA_buttonActive = not groupA_buttonActive
                if groupA_buttonActive:
                    groupB_buttonActive = False
                    groupB_buttonDisabled = True
                else:
                    groupB_buttonActive = True
                    groupB_buttonDisabled = False
            elif clickButton == "Group B":
                groupB_buttonActive = not groupB_buttonActive
            else:
                raise ValueError("Unexpected button has been clicked: {}".format(clickButton))
        groupA_dropdownDisabled, groupB_dropdownDisabled = not groupA_buttonActive, not groupB_buttonActive

    return [
        annotation_dropdownValue, annotation_dropdownOptions, annotation_dropdownDisabled,
        groupA_buttonActive, groupA_buttonDisabled,
        groupA_dropdownValue, groupA_dropdownOptions, groupA_dropdownDisabled,
        groupB_buttonActive, groupB_buttonDisabled,
        groupB_dropdownValue, groupB_dropdownOptions, groupB_dropdownDisabled,
    ]


@callback(
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        group_cells=Input(
            {"type": "Group Cells", "label_name": ALL, "function": "refresh"},
            "data"
        ),
        buttonActives=(
                State(
                    {
                        "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                        "label_name": "Group A", "type": "Button"
                    },
                    "active"
                ),
                State(
                    {
                        "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                        "label_name": "Group B", "type": "Button"
                    },
                    "active"
                ),
        )
    )
)
def returnMarkerGeneIdentificationSubmit(group_cells, buttonActives):
    return buttonActives[0] or buttonActives[1]


@callback(
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Store", "index": MATCH, "label": ALL,
        },
        "data"
    ),
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Button", "index": MATCH, "label": ALL
        },
        "active"
    ),
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Button", "index": MATCH, "label": ALL
        },
        "disabled"
    ),
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": ALL
        },
        "disabled"
    ),
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": ALL
        },
        "value"
    ),
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": ALL
        },
        "options"
    ),

    inputs=dict(
        userSessionId=Input('User Session ID', 'data'),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
        dataID=State(
            {
                'class': 'markerGeneIdentification', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "markerGeneIdentification", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        annotationParameters=(
            Input(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": "Annotation"
                },
                "value"
            ),
        ),
        groupParameters=(
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Store", "index": MATCH, "label": ALL,
                },
                "data"
            ),
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": "Group A"
                },
                "value"
            ),
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": "Group B"
                },
                "value"
            ),
        ),
        buttonGroupParameters=(
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Button", "index": MATCH, "label": ALL
                },
                "active"
            ),
            Input(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Button", "index": MATCH, "label": ALL
                },
                "n_clicks"
            ),
        )
    )
)
def returnMarkerGeneIdentificationGraphGroupController(
        userSessionId, refresh_clusterHistoryRecorder, refresh_annotationTypeRecorder, dataID,
        defaultParameters, annotationParameters, groupParameters, buttonGroupParameters
):
    def returnAnnotationDropdown():
        annotationTypeRecorder = cellClickManager.annotationTypeRecorder
        annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotationDropdown(
            defaultParameters["Annotation"] if annotationParameters[0] is None else annotationParameters[0]
        )
        annotationOptions = returnDropdownOptions(annotationOptions)
        if annotationValue is None:
            raise ValueError("No category annotation found for current data: {}".format(cellClickManager.currentData))
        else:
            return False, annotationValue, annotationOptions

    def returnGroupDropdown(group, annotationValue):
        if clusterHistoryRecorder.refCol and annotationValue == clusterHistoryRecorder.refCol:
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
        else:
            adata = cellClickManager.returnAdata()
            annotationSeries = adata.obs[annotationValue]

        if group == "A":
            optionList = ["selected", "all"] + sorted(annotationSeries.unique())
        else:
            optionList = sorted(annotationSeries.unique()) + ["rest", "none"]
        group_options = returnDropdownOptions(optionList, sort=False)

        group_Value = groupParameters[1] if group == "A" else groupParameters[2]
        if group_Value is None:
            group_Value = defaultParameters["Group A Name"] if group == "A" else defaultParameters["Group B Name"]
        elif group_Value not in optionList:
            group_Value = optionList[2] if group == "A" else optionList[0]  # the first value in adata

        return group_Value, group_options

    def returnGroup(annotationValue, groupValue, groupName):
        [groupA_cells, groupB_cells], groupA_name, groupB_name = groupParameters
        if ctxIdStr == "":  # init
            if groupName == "Group A" and groupA_cells is None:
                return defaultParameters["Group A"]
            if groupName == "Group B" and groupB_cells is None:
                return defaultParameters["Group B"]
        try:
            ctxId = json.loads(ctxIdStr)
            if ctxId["type"] == "Button" and ctxId["label"] == groupName:
                if groupValue == "selected":
                    return selectedCellsRecorder.selectedCells
                elif groupValue == "all":
                    return list(adata.obs_names)
                elif groupValue == "rest":  # group B
                    cellIDs = adata.obs_names
                    return list(cellIDs[~ cellIDs.isin(groupA_cells)])
                elif groupValue == "none":
                    return []
                else:
                    if clusterHistoryRecorder.refCol and clusterHistoryRecorder.refCol == annotationValue:
                        annotationSeries = clusterHistoryRecorder.returnAnnotation()
                    else:
                        annotationSeries = adata.obs[annotationValue]
                    return list(annotationSeries[annotationSeries == groupValue].index)
            else:
                return dash.no_update
        except json.JSONDecodeError:
            return dash.no_update

    (
        groupA, groupB,
        groupA_buttonActive, groupB_buttonActive,
        groupA_buttonDisabled, groupB_buttonDisabled,
        annotation_dropdownDisabled, groupA_dropdownDisabled, groupB_dropdownDisabled,
        annotation_dropdownValue, groupA_dropdownValue, groupB_dropdownValue,
        annotation_dropdownOptions, groupA_dropdownOptions, groupB_dropdownOptions
    ) = [dash.no_update] * 15

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
    selectedCellsRecorder = cellClickManager.selectedCellsRecorder
    adata = cellClickManager.returnAdata()

    if cellClickManager.currentData != dataID:
        annotation_dropdownDisabled, groupA_dropdownDisabled, groupB_dropdownDisabled = [True] * 3
        groupA_buttonDisabled, GroupB_buttonDisabled = [True] * 2
        groupA_buttonActive, groupB_buttonActive = [False] * 2
    else:
        annotation_dropdownDisabled, annotation_dropdownValue, annotation_dropdownOptions = returnAnnotationDropdown()

        groupA_dropdownValue, groupA_dropdownOptions = returnGroupDropdown("A", annotation_dropdownValue)
        groupB_dropdownValue, groupB_dropdownOptions = returnGroupDropdown("B", annotation_dropdownValue)

        try:
            ctxId = json.loads(ctxIdStr)
            if ctxId["type"] == "Button":
                clickButton = ctxId["label"]
            elif ctxId["type"] == "Dropdown" and ctxId["label"] == "Annotation":
                clickButton = "Annotation"
            else:
                clickButton = None
        except json.JSONDecodeError:
            clickButton = None

        [groupA_buttonActive, groupB_buttonActive], [n_clicks_A, n_clicks_B] = buttonGroupParameters
        groupA_buttonDisabled = False
        if clickButton is None:
            pass
        elif clickButton == "Annotation":
            groupA_buttonActive = True
            groupB_buttonActive = False
            groupB_buttonDisabled = True
        elif clickButton == "Group A":
            groupA_buttonActive = not groupA_buttonActive
            if groupA_buttonActive:
                groupB_buttonActive = False
                groupB_buttonDisabled = True
            else:
                groupB_buttonActive = True
                groupB_buttonDisabled = False
        elif clickButton == "Group B":
            groupB_buttonActive = not groupB_buttonActive
        else:
            raise ValueError("Unexpected button has been clicked: {}".format(clickButton))
        groupA_dropdownDisabled, groupB_dropdownDisabled = not groupA_buttonActive, not groupB_buttonActive

        groupA = returnGroup(annotation_dropdownValue, groupA_dropdownValue, "Group A")
        groupB = returnGroup(annotation_dropdownValue, groupB_dropdownValue, "Group B")

    group_cells = [groupA, groupB]
    buttonActive = [groupA_buttonActive, groupB_buttonActive]
    buttonDisabled = [groupA_buttonDisabled, groupB_buttonDisabled]
    dropdownDisabled = [annotation_dropdownDisabled, groupA_dropdownDisabled, groupB_dropdownDisabled]
    dropdownValue = [annotation_dropdownValue, groupA_dropdownValue, groupB_dropdownValue]
    dropdownOptions = [annotation_dropdownOptions, groupA_dropdownOptions, groupB_dropdownOptions]
    return group_cells, buttonActive, buttonDisabled, dropdownDisabled, dropdownValue, dropdownOptions


@callback(
    Output(
        {
            'class': 'markerGeneIdentification', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
        },
        "disabled"
    ),
    Output(
        {
            'class': 'markerGeneIdentification', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
        },
        "value"
    ),
    Output(
        {
            'class': 'markerGeneIdentification', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
        },
        "options"
    ),

    Output(
        {
            'class': 'markerGeneIdentification', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 1
        },
        "disabled"
    ),
    Output(
        {
            'class': 'markerGeneIdentification', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 1
        },
        "active"
    ),
    Output(
        {
            'class': 'markerGeneIdentification', 'group': 'graph',
            'type': 'Input', 'index': MATCH, "inputIndex": 1
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input('User Session ID', 'data'),
        dataID=State(
            {
                'class': 'markerGeneIdentification', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        annotationValue=Input(
            {
                "class": "markerGeneIdentification", "group": "graph",
                "type": "Dropdown", "index": MATCH, "label": "Annotation",
            },
            "value"
        ),
        cellCluster=State(
            {
                'class': 'markerGeneIdentification', 'group': 'graph',
                'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
            },
            "value"
        )
    )

)
def returnMarkerGeneIdentificationGraphAnnotationController(
    userSessionId, dataID,
    refresh_clusterHistoryRecorder, annotationValue, cellCluster
):
    (
        rawAnnotationDisabled, rawAnnotationValue, rawAnnotationOptions,
        newAnnotationButtonDisabled, newAnnotationButtonActive, newAnnotationInputDisabled
    ) = [dash.no_update]*6

    if userSessionId != dataID:
        rawAnnotationDisabled, newAnnotationButtonDisabled, newAnnotationInputDisabled = True, True, True
        newAnnotationButtonActive = False
    else:
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        if clusterHistoryRecorder.refCol and annotationValue == clusterHistoryRecorder.refCol:
            rawAnnotationDisabled, newAnnotationButtonDisabled, newAnnotationInputDisabled = False, False, False
            newAnnotationButtonActive = True

            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            optionList = ["selected"] + sorted(annotationSeries.unique())
            rawAnnotationValue, rawAnnotationOptions = returnDropdown(optionList, value=cellCluster)
        else:
            rawAnnotationDisabled, newAnnotationButtonDisabled, newAnnotationInputDisabled = True, True, True
            newAnnotationButtonActive = False

            rawAnnotationOptions = [{"label": "No Reference", "value": False}]
            rawAnnotationValue = False

    return (
        rawAnnotationDisabled, rawAnnotationValue, rawAnnotationOptions,
        newAnnotationButtonDisabled, newAnnotationButtonActive, newAnnotationInputDisabled
    )


@callback(
    Output(
        {
            "class": "markerGeneIdentification", "group": "graph",
            "type": "Graph", "index": MATCH,
        },
        "figure"
    ),
    Output(
        {
            'class': "markerGeneIdentification", 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download",
        },
        "data"
    ),
    inputs=dict(
        # maybe a state is also works, because controllers are disabled in returnGroupController callbacks
        userSessionId=State('User Session ID', 'data'),
        dataID=State(
            {
                'class': 'markerGeneIdentification', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        # defaultParameters=State(
        #     {
        #         "class": "markerGeneIdentification", "group": "graph",
        #         "type": "Store", "index": MATCH
        #     },
        #     "data"
        # ),
        plotParameters=(
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Store", "index": MATCH, "label": ALL,
                },
                "data"
            ),
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": ALL
                },
                "value"
            ),
        ),
        buttonGroupParameters=(
            Input(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Button", "index": MATCH, "label": ALL
                },
                "active"
            ),
        ),
        export=Input(
            {
                'class': "markerGeneIdentification", 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit",
            },
            "n_clicks"
        )
    ),
    prevent_initial_call=True
)
def returnMarkerGeneIdentificationGraph(
        userSessionId, dataID,
        # defaultParameters,
        plotParameters, buttonGroupParameters,
        export
):
    adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder

    if cellClickManager.currentData != dataID:
        figure, exportDf = dash.no_update, dash.no_update
    else:
        [groupA, groupB], [annotationValue, groupA_name, groupB_name] = plotParameters

        buttonGroupA_Active, buttonGroupB_Active = buttonGroupParameters[0]
        if buttonGroupA_Active or buttonGroupB_Active:
            raise PreventUpdate
        else:
            if (len(groupA) == 0 and len(groupB) > 0) | (len(set(groupA) & set(groupB)) > 0):
                raise ValueError("There is overlap between groupA and groupB")

            # groupB == []; it means groupB is selected by None, which identification for groupA with annotation
            if not groupB:
                if clusterHistoryRecorder.refCol and annotationValue == clusterHistoryRecorder.refCol:
                    groupB = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
                else:
                    groupB = cellClickManager.returnAdata().obs[annotationValue]

            figure, exportDf = adataProcessor.get_marker_gene_plot_for_groups(
                groupA, groupB, [groupA_name, groupB_name], graphType="Dot"
            )

            export = checkExport(dash.callback_context, index=0)
            if export:
                exportDf = dash.dcc.send_data_frame(exportDf.to_csv, "MarkerGene.csv")
            else:
                exportDf = dash.no_update

    return figure, exportDf


@callback(
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Marker Source", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Marker Source", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Species", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Species", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Cluster Name", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Cluster Name", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Gene Number", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        markerSource=Input(
            {
                "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
                "label_name": "Marker Source", "type": "Dropdown"
            },
            "value"
        ),
        speciesValue=State(
            {
                "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
                "label_name": "Species", "type": "Dropdown"
            },
            "value"
        ),
        clusterNameValue=State(
            {
                "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
                "label_name": "Cluster Name", "type": "Dropdown"
            },
            "value"
        ),
        geneNumValue=State(
            {
                "card_name": "Gene Analysis", "form_name": "Marker Gene Evaluation",
                "label_name": "Gene Number", "type": "Input"
            },
            "value"
        ),
    )
)
def returnGeneSimilarityForm(
    userSessionId, refresh_clusterHistoryRecorder,
    # refresh_annotationTypeRecorder, annotationValue,
    markerSource, speciesValue, clusterNameValue, geneNumValue
):
    if userSessionId is None:
        markerValue, markerOptions = False, [dict(label="No Reference", value=False)]
        speciesValue, speciesOptions = False, [dict(label="No Reference", value=False)]
        clusterNameValue, clusterNameOptions = None, []
        submitDisabled = True
    else:
        speciesValue, speciesOptions = returnDropdown(["human", "mouse"], value=speciesValue)

        sources = returnMarkerSource(marker_ref)
        markerOptions = [returnMarkerFile(sourceName, analysis="Gene Analysis", species=speciesValue) for sourceName in sources]
        markerOptions = [{"label": sourceName, "value": sourceFile} for sourceName, sourceFile in markerOptions]
        markerValue = markerOptions[0]["value"]

        # annotationTypeRecorder = cellClickManager.annotationTypeRecorder
        # annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotationDropdown(annotationValue)
        # annotationOptions = returnDropdownOptions(annotationOptions)
        # if annotationValue is None:
        #     clusterNameValue, clusterNameOptions = None, None
        #     submitDisabled = True
        # else:
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        if clusterHistoryRecorder.refCol:
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            optionList = sorted(annotationSeries.unique())
            clusterNameOptions = returnDropdownOptions(optionList, ["selected"])
            if clusterNameValue is None:
                clusterNameValue = optionList[0]

            submitDisabled = False
        else:
            clusterNameValue, clusterNameOptions = None, []
            submitDisabled = True

    if geneNumValue is None:
        geneNumValue = 10

    return [
        markerValue, markerOptions,
        speciesValue, speciesOptions,
        clusterNameValue, clusterNameOptions,
        geneNumValue, submitDisabled
    ]


@callback(
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Graph", "index": MATCH, "graphIndex": 0,
        },
        "figure"
    ),
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Graph", "index": MATCH, "graphIndex": 1,
        },
        "figure"
    ),
    Output(
        {
            'class': "markerGeneEvaluation", 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download",
        },
        "data"
    ),
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": ALL
        },
        "value"
    ),
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": ALL
        },
        "options"
    ),
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": ALL
        },
        "disabled"
    ),
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Input", "index": MATCH, "label": "Gene Number"
        },
        "value"
    ),
    Output(
        {
            "class": "markerGeneEvaluation", "group": "graph",
            "type": "Input", "index": MATCH, "label": "Gene Number"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=State('User Session ID', 'data'),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        refresh_selectedCellsRecorder=Input("refresh_selectedCellsRecorder", "data"),
        dataID=State(
            {
                'class': 'markerGeneEvaluation', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "markerGeneEvaluation", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        dropdowns=Input(
            {
                "class": "markerGeneEvaluation", "group": "graph",
                "type": "Dropdown", "index": MATCH, "label": ALL
            },
            "value"
        ),
        geneNum=Input(
            {
                "class": "markerGeneEvaluation", "group": "graph",
                "type": "Input", "index": MATCH, "label": "Gene Number"
            },
            "value"
        ),
        export=Input(
            {
                'class': "markerGeneEvaluation", 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit",
            },
            "n_clicks"
        )
    )
)
def returnGeneSimilarityGraph(
    userSessionId, refresh_clusterHistoryRecorder, refresh_selectedCellsRecorder, dataID,
    defaultParameters, dropdowns, geneNum, export
):
    (
        fig1, fig2, export,
        markerSourceValue, markerSourceOptions, markerSourceDisabled,
        speciesValue, speciesOptions, speciesDisabled,
        cellClusterValue, cellClusterOptions, cellClusterDisabled,
        geneNumValue, geneNumDisabled,
        cellTypeValue, cellTypeOptions, cellTypeDisabled,
    ) = [dash.no_update]*17

    if cellClickManager.currentData != dataID:
        markerSourceDisabled, speciesDisabled, cellClusterDisabled, geneNumDisabled, cellTypeDisabled = [True]*5
    else:
        markerSourceValue, speciesValue, cellTypeValue, cellClusterValue = dropdowns
        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        selectedCellsRecorder = cellClickManager.selectedCellsRecorder

        if speciesValue is None:
            speciesValue = defaultParameters["Species"]
        speciesValue, speciesOptions = returnDropdown(["human", "mouse"], value=speciesValue)

        # for gene analysis, the path to gene weight is depend on speciesValue
        sources = returnMarkerSource(marker_ref)
        markerSourceOptions = [returnMarkerFile(sourceName, analysis="Gene Analysis", species=speciesValue) for sourceName in sources]
        markerSourceOptions = [
            {"label": sourceName, "value": sourceFile} for sourceName, sourceFile in markerSourceOptions
        ]
        if markerSourceValue is None:
            markerSourceValue = defaultParameters["Marker Source"]

        annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
        optionList = sorted(annotationSeries.unique())
        if not cellClusterValue:
            cellClusterValue = defaultParameters["Cluster Name"]
        elif (cellClusterValue not in optionList) and (cellClusterValue != "selected"):
            cellClusterValue = optionList[0]
        else:
            pass
        cellClusterValue, cellClusterOptions = returnDropdown(optionList, first=["selected"], value=cellClusterValue)

        if cellClusterValue == "selected":
            cells = selectedCellsRecorder.selectedCells
        else:
            cells = list(annotationSeries[annotationSeries == cellClusterValue].index)

        if geneNum is None:
            geneNumValue = defaultParameters["Gene Number"]
        else:
            geneNumValue = geneNum

        fig1, overlapDf = adataProcessor.returnMarkerGeneEvaluationPlot(
            cells, cellClusterValue, annotationSeries, markerSourceValue, int(geneNumValue)
        )  # compared with other cell clusters

        cellTypeOptions = [
            {"label": cellType, "value": cellType} for cellType in overlapDf.index
        ]
        if (cellTypeValue is None) or (cellTypeValue not in overlapDf.index):
            cellTypeValue = overlapDf.index[0]

        fig2, exportDf = adataProcessor.returnColorDotPlot(
            cellClusterValue, annotationSeries, overlapDf, cellTypeValue
        )

        cellClusterDisabled, geneNumDisabled, cellTypeDisabled = [False] * 3
        exportDf = pd.concat([overlapDf, exportDf], ignore_index=True)

    export = checkExport(dash.callback_context, index=0)
    if export:
        exportDf = dash.dcc.send_data_frame(exportDf.to_csv, "GeneExpression.csv")
    else:
        exportDf = dash.no_update
    return (
        fig1, fig2, exportDf,
        [markerSourceValue, speciesValue, cellTypeValue, cellClusterValue],
        [markerSourceOptions, speciesOptions, cellTypeOptions, cellClusterOptions],
        [markerSourceDisabled, speciesDisabled, cellTypeDisabled, cellClusterDisabled],
        geneNumValue, geneNumDisabled,
    )

# @callback(
#     Output(
#         {
#             "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#             "label_name": "Annotation", "type": "Dropdown"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#             "label_name": "Annotation", "type": "Dropdown"
#         },
#         "options"
#     ),
#     Output(
#         {
#             "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#             "label_name": "Gene Name", "type": "Dropdown"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#             "label_name": "Gene Name", "type": "Dropdown"
#         },
#         "options"
#     ),
#     Output(
#         {
#             "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#             "label_name": "Submit", "type": "Button"
#         },
#         "disabled"
#     ),
#     inputs=dict(
#         userSessionId=Input("User Session ID", "data"),
#         refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
#         annotationValue=State(
#             {
#                 "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#                 "label_name": "Annotation", "type": "Dropdown"
#             },
#             "value"
#         ),
#         geneNameValue=State(
#             {
#                 "card_name": "Gene Analysis", "form_name": "Expression Similarity Search",
#                 "label_name": "Gene Name", "type": "Dropdown"
#             },
#             "value"
#         ),
#     )
# )
# def returnExpressionSimilaritySearchForm(
#         userSessionId, refresh_annotationTypeRecorder,
#         annotationValue, geneNameValue
# ):
#     if userSessionId is None:
#         annotationValue, annotationOptions = None, []
#         geneNameValue, geneNameOptions = None, []
#         submitDisabled = True
#     else:
#         annotationTypeRecorder = cellClickManager.annotationTypeRecorder
#         annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotationDropdown(annotationValue)
#         annotationOptions = returnDropdownOptions(annotationOptions)
#
#         if annotationValue:
#             submitDisabled = False
#         else:
#             submitDisabled = True
#
#         geneNameList = list(cellClickManager.returnAdata().var_names)
#         geneNameValue, geneNameOptions = returnDropdown(geneNameList, value=geneNameValue)
#
#     return annotationValue, annotationOptions, geneNameValue, geneNameOptions, submitDisabled
#
# @callback(
#     Output(
#         {
#             "class": "expressionSimilaritySearch", "group": "graph",
#             "type": "Graph", "index": MATCH,
#         },
#         "figure"
#     ),
#     Output(
#         {
#             'class': "expressionSimilaritySearch", 'group': 'graph',
#             'type': 'Download', 'index': MATCH, "function": "Download",
#         },
#         "data"
#     ),
#     Output(
#         {
#             "class": "expressionSimilaritySearch", "group": "graph",
#             "type": "Dropdown", "index": MATCH, "dropDownIndex": ALL
#         },
#         "value"
#     ),
#     Output(
#         {
#             "class": "expressionSimilaritySearch", "group": "graph",
#             "type": "Dropdown", "index": MATCH, "dropDownIndex": ALL
#         },
#         "options"
#     ),
#     Output(
#         {
#             "class": "expressionSimilaritySearch", "group": "graph",
#             "type": "Dropdown", "index": MATCH, "dropDownIndex": ALL
#         },
#         "disabled"
#     ),
#     inputs=dict(
#         userSessionId=State('User Session ID', 'data'),
#         refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
#         dataID=State(
#             {
#                 'class': 'expressionSimilaritySearch', 'group': 'graph',
#                 'type': "Label", 'function': "Data ID",
#                 'index': MATCH,
#             },
#             "children"
#         ),
#         defaultParameters=State(
#             {
#                 "class": "expressionSimilaritySearch", "group": "graph",
#                 "type": "Store", "index": MATCH
#             },
#             "data"
#         ),
#         dropdowns=Input(
#             {
#                 "class": "expressionSimilaritySearch", "group": "graph",
#                 "type": "Dropdown", "index": MATCH, "dropDownIndex": ALL
#             },
#             "value"
#         ),
#     )
# )
# def returnExpressionSimilaritySearchGraph(
#     userSessionId, refresh_annotationTypeRecorder, dataID, defaultParameters, dropdowns
# ):
#
#     (
#         fig, exportDf,
#         annotationValue, annotationOptions, annotationDisabled,
#         geneNameValue, geneNameOptions, geneNameDisabled
#     ) = [dash.no_update]*8
#     if userSessionId != dataID:
#         annotationDisabled, geneNameDisabled = True, True
#     else:
#         annotationTypeRecorder = cellClickManager.annotationTypeRecorder
#         annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotationDropdown(
#             defaultParameters["Annotation"] if dropdowns[0] is None else dropdowns[0]
#         )
#         annotationOptions = returnDropdownOptions(annotationOptions)
#         annotationDisabled = False
#
#         geneNameOptions = returnDropdownOptions(list(cellClickManager.returnAdata().var_names))
#         if dropdowns[1] is None:
#             geneNameValue = defaultParameters["Gene Name"]
#         else:
#             geneNameValue = dropdowns[1]
#         geneNameDisabled = False
#
#         clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
#         if clusterHistoryRecorder.refCol and clusterHistoryRecorder.refCol == annotationValue:
#             annotationSeries = clusterHistoryRecorder.returnAnnotation()
#         else:
#             adata = cellClickManager.returnAdata()
#             annotationSeries = adata.obs[annotationValue]
#
#         adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
#         fig, exportDf = adataProcessor.returnGeneSimilarityGraph(geneNameValue, annotationSeries)
#
#         export = checkExport(dash.callback_context, index=0)
#         if export:
#             exportDf = dash.dcc.send_data_frame(exportDf.to_csv, "GeneDxpression.csv")
#         else:
#             exportDf = dash.no_update
#
#     return (
#         fig, exportDf,
#         [annotationValue, geneNameValue], [annotationOptions, geneNameOptions], [annotationDisabled, geneNameDisabled]
#     )
