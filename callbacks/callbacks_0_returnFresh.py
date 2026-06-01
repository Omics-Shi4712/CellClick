#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_0_returnFresh.py.py
@time: 2023/11/7 14:23
"""
from callbacks.init import *

"""
    return store data named with "fresh" prefix, inlcuding 
    [
        refresh_annotationTypeRecorder, refresh_clusterHistoryRecorder, returnSelectedCells, returnGroupCells
    ],
    in which refresh_annotationTypeRecorder was achieved in callback_3
"""


@callback(
    Output("refresh_clusterHistoryRecorder", "data"),
    Output("rollback", "disabled"),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh=State("refresh_clusterHistoryRecorder", "data"),
        initParameters=(
            Input(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Preprocessed", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Reference", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Method", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Resolution", "type": "Input"
                },
                "value"
            ),
        ),
        reAnnotationParameters=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Reannotation",
                    "label_name": "Raw Name", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Reannotation",
                    "label_name": "New Name", "type": "Input"
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Cell Reannotation", "form_name": "Reannotation",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        # reClusteringParameters=(
        #     State(
        #         {
        #             "card_name": "Cell Reannotation", "form_name": "Re-cluster",
        #             "label_name": "Cluster", "type": "Dropdown"
        #         },
        #         "value"
        #     ),
        #     State(
        #         {
        #             "card_name": "Cell Reannotation", "form_name": "Re-cluster",
        #             "label_name": "Prefix", "type": "Input"
        #         },
        #         "value"
        #     ),
        #     State(
        #         {
        #             "card_name": "Cell Reannotation", "form_name": "Re-cluster",
        #             "label_name": "Method", "type": "Dropdown"
        #         },
        #         "value"
        #     ),
        #     State(
        #         {
        #             "card_name": "Cell Reannotation", "form_name": "Re-cluster",
        #             "label_name": "Resolution", "type": "Input"
        #         },
        #         "value"
        #     ),
        #     Input(
        #         {
        #             "card_name": "Cell Reannotation", "form_name": "Re-cluster",
        #             "label_name": "Submit", "type": "Button"
        #         },
        #         "n_clicks"
        #     ),
        # ),
        mergeDataParams=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Merge Data",
                    "label_name": "Ref Data", "type": "Input"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Merge Data",
                    "label_name": "Other Data", "type": "Dropdown"
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Cell Reannotation", "form_name": "Merge Data",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        clusterEvaluationParameters=(
            Input(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Button", "index": ALL, "inputIndex": 3
                },
                "n_clicks"
            ),
            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    'type': 'Dropdown', 'index': ALL, "dropdownIndex": 0
                },
                "value"
            ),
            State(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Input", "index": ALL, "inputIndex": 3,
                },
                "id"
            ),
            State(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Input", "index": ALL, "inputIndex": 3
                },
                "value"
            )
        ),
        markerGeneIdentificationParameters=(
            Input(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Button", "index": ALL, "inputIndex": 1
                },
                "n_clicks"
            ),
            State(
                {
                    'class': 'markerGeneIdentification', 'group': 'graph',
                    'type': 'Dropdown', 'index': ALL, "dropdownIndex": 0
                },
                "value"
            ),
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Input", "index": ALL, "inputIndex": 1,
                },
                "id"
            ),
            State(
                {
                    "class": "markerGeneIdentification", "group": "graph",
                    "type": "Input", "index": ALL, "inputIndex": 1
                },
                "value"
            )
        ),
        markerGeneEvaluationParameters=(
            Input(
                {
                    "class": "markerGeneEvaluation", "group": "graph",
                    "type": "Button", "index": ALL, "inputIndex": 0
                },
                "n_clicks"
            ),
            State(
                {
                    "class": "markerGeneEvaluation", "group": "graph",
                    'type': 'Dropdown', 'index': ALL, "label": "Cluster Name"
                },
                "value"
            ),
            State(
                {
                    "class": "markerGeneEvaluation", "group": "graph",
                    "type": "Input", "index": ALL, "inputIndex": 0,
                },
                "id"
            ),
            State(
                {
                    "class": "markerGeneEvaluation", "group": "graph",
                    "type": "Input", "index": ALL, "inputIndex": 0
                },
                "value"
            )
        ),
        # markerGeneEvaluationParameters=(
        #     Input(),
        # ),
        rollbackParameters=(
            Input("rollback", "n_clicks")
        ),
        reset=Input("reset", "n_clicks"),
    ),
)
def returnClusterRecordDict(
    userSessionId,
    refresh,
    initParameters,
    reAnnotationParameters,
    # reClusteringParameters,
    mergeDataParams,
    clusterEvaluationParameters,
    markerGeneIdentificationParameters,
    markerGeneEvaluationParameters,
    rollbackParameters,
    reset,
):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "" or userSessionId is None:
        refresh = dash.no_update
        disabled = True
    else:
        if ctxIdStr == "User Session ID":
            refresh += 1
        elif ctxIdStr == "rollback":
            if cellClickManager.refreshRecoder(
                recoder="clusterHistoryRecorder", method="rollback",
            ):
                refresh += 1
            else:
                refresh = dash.no_update
        elif ctxIdStr == "reset":
            refresh = dash.no_update
        else:
            ctxId = json.loads(ctxIdStr)
            if "form_name" in ctxId:
                if ctxId["form_name"] == "Cell Clustering":
                    n_clicks, processedBy, refCol, cluster_method, resolution = initParameters
                    if cellClickManager.refreshRecoder(
                        recoder="clusterHistoryRecorder", method="init",
                        refExisted=True if processedBy == "Custom" else False, refCol=refCol,
                        cluster_method=cluster_method, resolution=float(resolution),
                    ):
                        refresh += 1
                        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
                        adataProcessor.isPreprocess = "Cell Clustering"
                    else:
                        refresh = dash.no_update
                elif ctxId["form_name"] == "Reannotation":
                    rawName, newName, n_clicks = reAnnotationParameters
                    if cellClickManager.refreshRecoder(
                        recoder="clusterHistoryRecorder", method="reAnnotation",
                        rawName=rawName, newName=newName
                    ):
                        refresh += 1
                    else:
                        refresh = dash.no_update
                # elif ctxId["form_name"] == "Re-cluster":
                #     value, prefix, cluster_method, resolution, n_clicks = reClusteringParameters
                #     if cellClickManager.refreshRecoder(
                #         recoder="clusterHistoryRecorder", method="reClustering",
                #         value=value, prefix=prefix,
                #         cluster_method=cluster_method, resolution=float(resolution),
                #     ):
                #         refresh += 1
                #     else:
                #         refresh = dash.no_update
                elif ctxId["form_name"] == "Merge Data":
                    refData, otherData, n_clicks = mergeDataParams
                    otherCellClick = cellClickManager.CellClick[otherData]
                    otherAnnotation = otherCellClick.clusterHistoryRecorder.returnAnnotation()
                    cellClickManager.refreshRecoder(
                        recoder="clusterHistoryRecorder", method="mergeData",
                        annotation=otherAnnotation,
                    )
                    refresh += 1
                else:
                    raise ValueError("Unexpected input received: {}".format(ctxIdStr))

            elif "class" in ctxId:
                switchDict = {
                    "markerGeneScoring": clusterEvaluationParameters,
                    "markerGeneIdentification": markerGeneIdentificationParameters,
                    "markerGeneEvaluation": markerGeneEvaluationParameters
                }
                graphIndex = ctxId["index"]
                reAnnotationParameters = switchDict[ctxId["class"]]
                n_clicks, clusters, ids, values = reAnnotationParameters
                for n_click, cluster, id, value in zip(n_clicks, clusters, ids, values):
                    if id["index"] == graphIndex:
                        if value in [None, ""] or n_clicks in [0, None]: # prevent callback when init
                            raise PreventUpdate
                        cellClickManager.refreshRecoder(
                            recoder="clusterHistoryRecorder", method="reAnnotation",
                            rawName=cluster, newName=value,
                        )
                refresh += 1
            else:
                raise ValueError("Unexpected input received: {}".format(ctxIdStr))

        if cellClickManager.clusterHistoryRecorder.level and cellClickManager.clusterHistoryRecorder.level >= 1:
            disabled = False
        else:
            disabled = True

    # I don't know why it works for some errors.
    # when reset, non-exist input/output error occurs for callbacks including ClusterHistory inputs
    import time
    time.sleep(1)

    return refresh, disabled


@callback(
    Output("refresh_selectedCellsRecorder", "data"),
    inputs=dict(
        userSessionId=Input('User Session ID', 'data'),
        dataIDParameters=(
            State(
                {
                    'class': ALL, 'group': 'graph',
                    'type': "Label", 'function': "Data ID",
                    'index': ALL,
                },
                "children"
            ),
            State(
                {
                    'class': ALL, 'group': 'graph',
                    'type': "Label", 'function': "Data ID",
                    'index': ALL,
                },
                "id"
            )
        ),
        refresh_clusterHistoryRecorder=State("refresh_clusterHistoryRecorder", "data"),
        cellEmbeddingParameters=(
            Input(
                {
                    "class": "cellEmbedding", "group": "graph",
                    "type": "Graph", "index": ALL,
                },
                'selectedData'
            ),
        ),
        # cellStatParameters=(
        #     State(
        #         {
        #             "class": "cellStat", 'group': 'graph',
        #             "type": "Graph", 'index': ALL,
        #         },
        #         'id'
        #     ),
        #     State(
        #         {
        #             "class": "cellStat", 'group': 'graph',
        #             "type": "Graph", 'index': ALL,
        #         },
        #         'figure'
        #     ),
        #     Input(
        #         {
        #             "class": "cellStat", 'group': 'graph',
        #             "type": "Graph", 'index': ALL,
        #         },
        #         'selectedData'
        #     ),
        # ),
        # tableUpdateParameters=(
        #     Input(
        #         {
        #             "class": "Cells Table", "group": "controller",
        #             "type": "Button", "label": "Select All"
        #         },
        #         "n_clicks"
        #     ),
        #     Input(
        #         {
        #             "class": "Cells Table", "group": "controller",
        #             "type": "Button", "label": "Unselect All"
        #         },
        #         "n_clicks"
        #     ),
        # ),
        tableUpdateParameters=(
            Input(
                {
                    "class": "cellSelection", "group": "graph",
                    "type": "Graph", "index": ALL,
                },
                'selectedData'
            ),
            Input(
                {
                    "class": "cellSelection", "group": "graph",
                    "label": "Select All", "index": ALL, "type": "Button",
                },
                "n_clicks"
            ),
        ),
        fixedActive=Input("fixSelection", "active"),
        refresh=State("refresh_selectedCellsRecorder", "data")
    ),
)
def returnSelectedCells(
        userSessionId, dataIDParameters,
        refresh_clusterHistoryRecorder,
        cellEmbeddingParameters,
        # cellStatParameters,
        tableUpdateParameters,
        fixedActive,
        refresh
):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "" or userSessionId is None:
        refresh = dash.no_update
    # if ctxIdStr == "User Session ID" or ctxIdStr == "" or len(ctx.triggered) > 1:
    elif ctxIdStr == "User Session ID":
        refresh += 1
    elif ctxIdStr == "fixSelection":
        if cellClickManager.refreshRecoder(
            recoder="selectedCellsRecorder", method="fixedSelection",
            fixedActive=fixedActive
        ):
            refresh += 1
        else:
            refresh = dash.no_update
    else:
        ctx = dash.callback_context
        ctxId = json.loads(ctxIdStr)
        if ctxId["type"] == "Graph":
            index = ctxId["index"]
            dataIDs, storeIDs = dataIDParameters
            for dataID, storeID in zip(dataIDs, storeIDs):
                if storeID["index"] == index:
                    dataSelected = dataID
                    break
            if cellClickManager.currentData != dataSelected:    # only received selected from same Data graph
                refresh = dash.no_update
            else:
                selection = ctx.triggered[0]["value"]
                if cellClickManager.refreshRecoder(
                    recoder="selectedCellsRecorder", method="canvas",
                    selection=selection, ctxId=ctxId, fixedActive=fixedActive,
                    # cellStatParameters=cellStatParameters
                ):
                    refresh += 1
                else:
                    refresh = dash.no_update
        elif ctxId["type"] == "Button":
            if cellClickManager.refreshRecoder(
                recoder="selectedCellsRecorder", method="table",
                operation=ctxId["label"]
            ):
                refresh += 1
            else:
                refresh = dash.no_update
        else:
            raise ValueError("Unexpected Input received: {}".format(ctxIdStr))

    return refresh


@callback(
    Output("fixSelection", "active"),
    Output("fixSelection", "style"),
    Output("fixSelection", "disabled"),  # the default value is True
    Output({"class": "fixSelection", "type": "Button", "name": ALL}, "style"),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        fixSelectionButton=(
            State("fixSelection", "style"),
            Input("fixSelection", "n_clicks"),
        ),
        refParameters=(
            State("fixSelection", "active"),
            State({"class": "fixSelection", "type": "Button", "name": ALL}, "style"),
        )
    ),
)
def returnFixedSelectionButtonGroup(userSessionId, fixSelectionButton, refParameters):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    buttonStyle, n_clicks = fixSelectionButton
    active, styles = refParameters

    if userSessionId is None or ctxIdStr == "":
        disabled = False
        active = False
        for style in styles:
            style["visibility"] = "hidden"
    else:
        if ctxIdStr == "User Session ID":
            disabled = False
            active = False
            for style in styles:
                style["visibility"] = "hidden"
        elif ctxIdStr == "fixSelection":
            disabled = False
            for style in styles:
                style["visibility"] = "hidden" if active else "visible"
            active = not active
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))

        if "background-color" in buttonStyle:
            del buttonStyle["background-color"]
        if "border-color" in buttonStyle:
            del buttonStyle["border-color"]

    return active, buttonStyle, disabled, styles


@callback(
    Output("refresh_fixedCellsRecorder", "data"),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        active=Input("fixSelection", "active"),
        refresh=State("refresh_fixedCellsRecorder", "data"),
        buttonGroup=Input({"class": "fixSelection", "type": "Button", "name": ALL}, "n_clicks"),
    ),
)
def returnFixedCells(userSessionId, active, refresh, buttonGroup):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "" or userSessionId is None:
        refresh = dash.no_update
    if not active:
        refresh = dash.no_update
    elif ctxIdStr == "User Session ID":
        if cellClickManager.refreshRecoder(
            recoder="fixedCellsRecorder", method="init",
        ):
            refresh += 1
        else:
            refresh = dash.no_update
    elif ctxIdStr == "fixSelection":
        if cellClickManager.refreshRecoder(
            recoder="fixedCellsRecorder", method="selected",
        ):
            refresh += 1
        else:
            refresh = dash.no_update
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId["type"] == "Button":
            if cellClickManager.refreshRecoder(
                recoder="fixedCellsRecorder", method="modify",
                operation=ctxId["name"]
            ):
                refresh += 1
            else:
                refresh = dash.no_update
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))
    return refresh


@callback(
    Output({"type": "Group Cells", "label_name": MATCH, "function": "refresh"}, "data"),
    inputs=dict(
        groupsButton=(
            State(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": MATCH,  "type": "Button"
                },
                "id"
            ),
            Input(
                {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": MATCH, "type": "Button"
                },
                "active"
            ),
        ),
        annotationValue=State(
            {
                "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                "label_name": "Annotation", "type": "Dropdown"
            },
            "value"
        ),
        groupValue=State(
            {
                    "card_name": "Gene Analysis", "form_name": "Marker Gene Identification",
                    "label_name": MATCH, "type": "Dropdown"
            },
            "value"
        ),
        refresh=State({"type": "Group Cells", "label_name": MATCH, "function": "refresh"}, "data"),
    ),
    prevent_initial_call=True,
)
def returnGroupCells(groupsButton, groupValue,  annotationValue, refresh):
    buttonId, active = groupsButton

    if annotationValue is None or groupValue is None:
        raise PreventUpdate
    if not active:
        if cellClickManager.refreshRecoder(
            recoder="groupCellsRecorder", method=groupValue,
            group=buttonId["label_name"], annotation=annotationValue,
        ):
            refresh += 1
        else:
            refresh = dash.no_update

    else:
        refresh = dash.no_update

    return refresh


if __name__ == '__main__':
    pass
