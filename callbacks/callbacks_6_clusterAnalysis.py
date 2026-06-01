#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_6_clusterAnalysis.py
@time: 2024/11/13 10:36
"""

from callbacks.callbacks_5_geneAnalysis import *


# these callbacks are re-organized as part of preprocessing or (evaluation and validation)


@callback(
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Preprocessed", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Preprocessed", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Preprocessed", "type": "Dropdown"
        },
        "disabled"
    ),
    # Output(
    #     {
    #         "card_name": "Preprocessing", "form_name": "Cell Clustering",
    #         "label_name": "Preprocessed", "type": "Dropdown"
    #     },
    #     "style"
    # ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Reference", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Reference", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Reference", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Reference", "type": ALL
        },
        "style"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Method", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Method", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Method", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Method", "type": ALL
        },
        "style"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Resolution", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Resolution", "type": "Input"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Resolution", "type": ALL
        },
        "style"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Cell Clustering",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        preprocessedParameters=(
            Input(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Preprocessed", "type": "Dropdown"
                },
                "value"
            ),
        ),
        referenceParameters=(
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
                    "label_name": "Reference", "type": ALL
                },
                "style"
            ),
        ),
        methodParameters=(
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
                    "label_name": "Method", "type": ALL
                },
                "style"
            ),
        ),
        resolutionParameters=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Resolution", "type": "Input"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Resolution", "type": ALL
                },
                "style"
            ),
        ),
        submitParameters=(
            Input(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        )
    ),
    prevent_initial_call=True
)
def returnDataSettingsForm(
    userSessionId,
    preprocessedParameters, methodParameters, referenceParameters, resolutionParameters,
    submitParameters
):
    def initForm():
        adata = cellClickManager.returnAdata()

        preprocessedValue, preprocessedOptions = returnDropdown(["Custom", "CellClick"], sort=False)
        referenceValue, referenceOptions = returnDropdown(adata.obs.columns)
        methodValue, methodOptions = returnDropdown(["Leiden", "Louvain"])
        resolutionValue = 1

        clusterHistoryRecord = cellClickManager.clusterHistoryRecorder
        if clusterHistoryRecord.refCol:
            referenceValue = clusterHistoryRecord.refCol
            preprocessedDisabled, referenceDisabled, methodsDisabled,  resolutionDisabled, submitDisabled = [True] * 5
            # preprocessedValue = "Custom"
        else:
            preprocessedDisabled, referenceDisabled, methodsDisabled,  resolutionDisabled, submitDisabled = [False] * 5
            # preprocessedValue = "Custom"

        # referenceStyles, methodStyles, resolutionStyles = (
        #     referenceParameters[1], methodParameters[1], resolutionParameters[1]
        # )
        referenceStyles = [{} if style is None else style for style in referenceParameters[1]]
        methodStyles = [{} if style is None else style for style in methodParameters[1]]
        resolutionStyles = [{} if style is None else style for style in resolutionParameters[1]]
        for i in range(0, len(referenceStyles)):
            referenceStyles[i]["display"] = "block"

        for i in range(0, len(methodStyles)):
            methodStyles[i]["display"] = "none"

        for i in range(0, len(resolutionStyles)):
            resolutionStyles[i]["display"] = "none"

        return (
            [preprocessedValue, preprocessedOptions, preprocessedDisabled],
            [referenceValue, referenceOptions, referenceDisabled, referenceStyles],
            [methodValue, methodOptions, methodsDisabled, methodStyles],
            [resolutionValue, resolutionDisabled, resolutionStyles],
            [submitDisabled]
        )

    def returnFormByDropdown():
        preprocessedValue = preprocessedParameters[0]
        referenceValue = referenceParameters[0]
        methodValue = methodParameters[0]
        resolutionValue = resolutionParameters[0]

        preprocessedOptions, referenceOptions, methodOptions = [dash.no_update]*3
        (
            preprocessedDisabled, referenceDisabled, methodsDisabled,  resolutionDisabled, submitDisabled
        ) = [dash.no_update]*5

        # referenceDisabled, resolutionDisabled = [False, True] if preprocessedValue == "Custom" else [True, False]
        referenceStyles, methodStyles, resolutionStyles = (
            referenceParameters[1], methodParameters[1], resolutionParameters[1]
        )
        for i in range(0, len(referenceStyles)):
            referenceStyles[i]["display"] = "block" if preprocessedValue == "Custom" else "none"

        for i in range(0, len(methodStyles)):
            methodStyles[i]["display"] = "none" if preprocessedValue == "Custom" else "block"

        for i in range(0, len(resolutionStyles)):
            resolutionStyles[i]["display"] = "none" if preprocessedValue == "Custom" else "block"

        return (
            [preprocessedValue, preprocessedOptions, preprocessedDisabled],
            [referenceValue, referenceOptions, referenceDisabled, referenceStyles],
            [methodValue, methodOptions, methodsDisabled, methodStyles],
            [resolutionValue, resolutionDisabled, resolutionStyles],
            [submitDisabled]
        )

    def returnFormByButton():
        preprocessedValue, referenceValue, methodValue, resolutionValue = [dash.no_update] * 4
        preprocessedOptions, referenceOptions, methodOptions = [dash.no_update] * 3
        preprocessedDisabled, referenceDisabled, methodsDisabled, resolutionDisabled, submitDisabled = [True] * 5
        referenceStyles, methodStyles, resolutionStyles = (
            [dash.no_update]*2, [dash.no_update]*2, [dash.no_update]*2
        )

        return (
            [preprocessedValue, preprocessedOptions, preprocessedDisabled],
            [referenceValue, referenceOptions, referenceDisabled, referenceStyles],
            [methodValue, methodOptions, methodsDisabled, methodStyles],
            [resolutionValue, resolutionDisabled, resolutionStyles],
            [submitDisabled]
        )

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "User Session ID":
        if userSessionId is None:
            raise PreventUpdate
        else:
            preprocessed, reference, method, resolution, submit = initForm()
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId["type"] == "Dropdown":
            preprocessed, reference, method, resolution, submit = returnFormByDropdown()
        elif ctxId["type"] == "Button":
            preprocessed, reference, method, resolution, submit = returnFormByButton()
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))

    # for style in reference[-1]:
    #     style["display"] = "block"
    return preprocessed + reference + method + resolution + submit



@callback(
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Cell Cluster", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Cell Cluster", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Cell Cluster", "type": "Dropdown"
        },
        "disabled"
    ),

    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Gene Number", "type": "Input"
        },
        "value"
    ),

    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "options"
    ),

    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
        geneNum=State(
            {
                "card_name": "Evaluation and Validation", "form_name": "Annotation Evaluation",
                "label_name": "Gene Number", "type": "Input"
            },
            "value"
        ),
    ),
)
def returnAnnotationEvaluationForm(userSessionId, refresh_clusterHistoryRecorder, refresh_annotationTypeRecorder, geneNum):
    if userSessionId is None:
        (
            clusterValue, clusterOptions, clusterDisabled,
            geneNum,
            embeddingValue, embeddingOptions,
            submitDisabled,
        ) = (
            None, [], True,
            None,
            None, [],
            True,
        )
    else:
        adata = cellClickManager.returnAdata()

        embeddings = resortObsm(adata.obsm.keys())
        embeddingValue, embeddingOptions = returnDropdown(embeddings, sort=False)

        geneNum = 10 if geneNum is None else geneNum

        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        clusterDisabled = True if clusterHistoryRecorder.refCol is None else False
        submitDisabled = clusterDisabled
        if clusterDisabled:
            clusterValue = False
            clusterOptions = [dict(label="No Reference", value=False)]
        else:
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            clusterOptions = sorted(annotationSeries.unique())
            clusterValue, clusterOptions = returnDropdown(clusterOptions, first=[], last=[])
    return clusterValue, clusterOptions, clusterDisabled, geneNum, embeddingValue, embeddingOptions, submitDisabled


@callback(
    Output(
        {
            'class': 'annotationEvaluation', 'group': 'graph',
            'type': 'Graph', 'index': MATCH, "graphIndex": 0
        },
        "figure"
    ),
    Output(
        {
            'class': 'annotationEvaluation', 'group': 'graph',
            'type': 'Graph', 'index': MATCH, "graphIndex": 1
        },
        "figure"
    ),

    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": "Cell Cluster",
        },
        "value"
    ),
    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": "Cell Cluster",
        },
        "options"
    ),

    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Input", "index": MATCH, "label": "Gene Number",
        },
        "value"
    ),

    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": "Gene Name",
        },
        "value"
    ),
    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": "Gene Name",
        },
        "options"
    ),

    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": "Embedding",
        },
        "value"
    ),
    Output(
        {
            "class": "annotationEvaluation", "group": "graph",
            "type": "Dropdown", "index": MATCH, "label": "Embedding",
        },
        "options"
    ),

    Output(
        {
            'class': 'annotationEvaluation', 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download"
        },
        "data"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
        dataID=State(
            {
                'class': 'annotationEvaluation', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "annotationEvaluation", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        plotParameters=(
            Input(
                {
                    "class": "annotationEvaluation", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": "Cell Cluster",  # It may be one or two dropdown
                },
                "value"
            ),
            Input(
                {
                    "class": "annotationEvaluation", "group": "graph",
                    "type": "Input", "index": MATCH, "label": "Gene Number",  # It may be one or two dropdown
                },
                "value"
            ),
            Input(
                {
                    "class": "annotationEvaluation", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": "Gene Name",  # It may be one or two dropdown
                },
                "value"
            ),
            Input(
                {
                    "class": "annotationEvaluation", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "label": "Embedding",  # It may be one or two dropdown
                },
                "value"
            ),
        ),
        exportClick=Input(
            {
                'class': 'annotationEvaluation', 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit"
            },
            "n_clicks"
        ),
    )
)
def returnAnnotationEvaluationGraph(
    userSessionId,
    refresh_clusterHistoryRecorder, refresh_annotationTypeRecorder,
    dataID, defaultParameters, plotParameters,
    exportClick,
):
    if cellClickManager.currentData != dataID:
        (
            dotFigure, embeddingFigure,
            cellClusterValue, cellClusterOptions,
            geneNumValue,
            geneNameValue, geneNameOptions,
            embeddingValue, embeddingOptions,
            exportDf
        ) = [dash.no_update]*10
    else:
        adata = cellClickManager.returnAdata()
        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor

        cellClusterValue, geneNumValue, geneNameValue, embeddingValue = plotParameters

        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
        cellClusterOptions = sorted(annotationSeries.unique())
        cellClusterValue, cellClusterOptions = returnDropdown(
            cellClusterOptions,
            value=defaultParameters["Cell Cluster"] if cellClusterValue is None else cellClusterValue,
        )

        geneNumValue = defaultParameters["Gene Number"] if geneNumValue is None else geneNumValue

        markerDf = adataProcessor.returnMarkerDf(
            groupby=annotationSeries, key_added="CellClick_cosg", n_genes_user=int(geneNumValue),
            remove_lowly_expressed=True
        )
        dotFigure, exportDf = adataProcessor.get_dot_plot(var_names=markerDf[cellClusterValue], groupby=annotationSeries)

        geneNameValue, geneNameOptions = returnDropdown(
            list(adata.var_names),
            value=list(markerDf[cellClusterValue])[0] if geneNameValue is None else geneNameValue,
        )

        embeddings = resortObsm(adata.obsm.keys())
        embeddingValue, embeddingOptions = returnDropdown(
            embeddings, value=defaultParameters["Embedding"] if embeddingValue is None else embeddingValue,
            sort=False
        )

        embeddingFigure, dropDf = adataProcessor.get_marker_scatter(use_rep=embeddingValue, marker_gene=geneNameValue)

    export = checkExport(dash.callback_context, index=0)
    if export:
        fileName = "markerGene.csv"
        return (
            dotFigure, embeddingFigure,
            cellClusterValue, cellClusterOptions,
            geneNumValue,
            geneNameValue, geneNameOptions,
            embeddingValue, embeddingOptions,
            dcc.send_data_frame(exportDf.to_csv, fileName)
        )
    else:
        return (
            dotFigure, embeddingFigure,
            cellClusterValue, cellClusterOptions,
            geneNumValue,
            geneNameValue, geneNameOptions,
            embeddingValue, embeddingOptions,
            dash.no_update,
        )

@callback(
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Marker Source", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Marker Source", "type": "Dropdown"
        },
        "options"
    ),

    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Source Name", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Source Name", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Source Name", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Cell Cluster", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Cell Cluster", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Cell Cluster", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Gene Number", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        markerSource=Input(
            {
                "card_name": "Evaluation and Validation", "form_name": "Marker Gene Scoring",
                "label_name": "Marker Source", "type": "Dropdown"
            },
            "value"
        ),
    ),
)
def returnMarkerGeneScoringForm(userSessionId, refresh_clusterHistoryRecorder, markerSource):
    if userSessionId is None:
        markerValue, markerOptions = False, [dict(label="No Reference", value=False)]
        sourceValue, sourceOptions, sourceDisabled = False, [dict(label="No Reference", value=False)], True
        clusterValue, clusterOptions, clusterDisabled = False, [dict(label="No Reference", value=False)], True
    else:
        markerValue, markerOptions = returnDropdown(
            options=returnMarkerSource(marker_ref_validation) + ["Upload Data"],
            value=markerSource
        )

        if markerValue == "Upload Data":
            dataIDs = cellClickManager.CellClickID.copy()
            dataIDs.remove(cellClickManager.currentData)
            sourceOptions = [{"label": dataID, "value": dataID} for dataID in dataIDs]
        else:
            sourceOptions = []
            for sourceName, sourceFile in returnMarkerFile(markerValue, analysis="Cluster Analysis"):
                sourceOptions.append({"label": sourceName, "value": sourceFile})

        if len(sourceOptions) == 0:
            sourceValue = False
            sourceOptions = [dict(label="No Reference", value=False)]
            sourceDisabled = True
        else:
            sourceValue = sourceOptions[0]["value"]
            sourceDisabled = False

        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        clusterDisabled = True if clusterHistoryRecorder.refCol is None else False
        if clusterDisabled:
            clusterValue = False
            clusterOptions = [dict(label="No Reference", value=False)]
        else:
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            clusterOptions = sorted(annotationSeries.unique())
            clusterValue = "selected"
            clusterOptions = returnDropdownOptions(clusterOptions, first=["selected"], last=[])

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "refresh_clusterHistoryRecorder":
        geneNumber = dash.no_update
    else:
        geneNumber = 10

    submitDisabled = sourceDisabled or clusterDisabled
    return (
        markerValue, markerOptions,
        sourceValue, sourceOptions, sourceDisabled,
        clusterValue, clusterOptions, clusterDisabled,
        geneNumber, submitDisabled
    )


@callback(
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 1
        },
        "disabled"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 1
        },
        "active"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Input', 'index': MATCH, "inputIndex": 1
        },
        "disabled"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Input', 'index': MATCH, "inputIndex": 1
        },
        "value"
    ),
    Input('User Session ID', 'data'),
    State(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': "Label", 'function': "Data ID",
            'index': MATCH,
        },
        "children"
    ),
    Input(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 1
        },
        "n_clicks"
    ),
    State(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 1
        },
        "active"
    ),
    State(
        {
            "class": "markerGeneScoring", "group": "graph",
            "type": "Store", "index": MATCH
        },
        "data"
    ),
    State(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Input', 'index': MATCH, "inputIndex": 1
        },
        "value"
    )
)
def returnMarkerGeneScoringGraphGeneNumController(userSessionID, dataID, n_clicks, active, defaultParameters, geneNumValue):
    if not geneNumValue:
        geneNumValue = int(defaultParameters["Gene Number"])
    else:
        geneNumValue = int(geneNumValue)

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "":
        return False, False, True, geneNumValue
    elif ctxIdStr == "User Session ID":
        if userSessionID != dataID:
            return True, True, False, dash.no_update
        else:
            return False, True, False, dash.no_update
    else:
        return False, not active, active, geneNumValue


@callback(
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 3
        },
        "disabled"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Button', 'index': MATCH, "inputIndex": 3
        },
        "active"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Input', 'index': MATCH, "inputIndex": 3
        },
        "disabled"
    ),
    Input('User Session ID', 'data'),
    State(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': "Label", 'function': "Data ID",
            'index': MATCH,
        },
        "children"
    ),
)
def returnMarkerGeneScoringGraphAnnotationController(userSessionID, dataID):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)

    if ctxIdStr == "":
        return False, True, False
    elif ctxIdStr == "User Session ID":
        if userSessionID != dataID:
            return True, True, True
        else:
            return False, True, False
    else:
        raise KeyError("Unexpected ctx is received: {}".format(ctxIdStr))


# {class : markerGeneScoring , group : graph , index :0, label : Data Source , type : Button }
@callback(
    # 3: Data Type; 1: Data Source
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Marker Source", 'type': 'Button', 'index': MATCH,
        },
        "active"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Marker Source", 'type': 'Button', 'index': MATCH,
        },
        "disabled"
    ),

    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Marker Source", 'type': 'Dropdown', 'index': MATCH,
        },
        "value"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Marker Source", 'type': 'Dropdown', 'index': MATCH,
        },
        "options"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Marker Source", 'type': 'Dropdown', 'index': MATCH,
        },
        "disabled"
    ),

    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Source Name", 'type': 'Button', 'index': MATCH,
        },
        "active"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Source Name", 'type': 'Button', 'index': MATCH,
        },
        "disabled"
    ),

    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Source Name", 'type': 'Dropdown', 'index': MATCH,
        },
        "value"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Source Name", 'type': 'Dropdown', 'index': MATCH,
        },
        "options"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            "label": "Source Name", 'type': 'Dropdown', 'index': MATCH,
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input('User Session ID', 'data'),
        dataID=State(
            {
                'class': 'markerGeneScoring', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "markerGeneScoring", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        groupParameters=(
            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Marker Source", 'type': 'Button', 'index': MATCH,
                },
                "active"
            ),
            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Marker Source", 'type': 'Dropdown', 'index': MATCH,
                },
                "value"
            ),
            Input(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Marker Source", 'type': 'Button', 'index': MATCH,
                },
                "n_clicks"
            ),

            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Source Name", 'type': 'Button', 'index': MATCH,
                },
                "active"
            ),
            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Source Name", 'type': 'Dropdown', 'index': MATCH,
                },
                "value"
            ),
            Input(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Source Name", 'type': 'Button', 'index': MATCH,
                },
                "n_clicks"
            ),
        )
    )
)
def returnMarkerGeneScoringDataGroupController(userSessionId, dataID, defaultParameters, groupParameters):
    sourceButtonActive, sourceButtonDisabled = [dash.no_update]*2
    sourceDropdownValue, sourceDropdownOptions, sourceDropdownDisabled = [dash.no_update]*3

    nameButtonActive, nameButtonDisabled = [dash.no_update]*2
    nameDropdownValue, nameDropdownOptions, nameDropdownDisabled = [dash.no_update]*3

    if cellClickManager.currentData != dataID:
        sourceButtonDisabled, sourceDropdownDisable, nameButtonDisabled, nameDropdownDisabled = [True]*4
    else:
        (
            sourceButtonActive, sourceDropdownValue, clicks_1,
            nameButtonActive, nameDropdownValue, clicks_2
        ) = groupParameters
        if sourceDropdownValue is None:
            sourceDropdownValue = defaultParameters["Marker Source"]
        sourceDropdownOptions = returnDropdownOptions(
            returnMarkerSource(marker_ref_validation) + ["Upload Data"]
        )

        if sourceDropdownValue == "Upload Data":
            cellClickIDs = cellClickManager.CellClickID
            nameDropdownOptions = []
            for cellClickID in cellClickIDs:
                hasRefCol = cellClickManager.CellClick[cellClickID].clusterHistoryRecorder.refCol
                if hasRefCol and cellClickID != cellClickManager.currentData:
                    nameDropdownOptions.append(cellClickID)
            nameDropdownOptions = returnDropdownOptions(nameDropdownOptions)
        else:
            nameDropdownOptions = []
            for sourceName, sourceFile in returnMarkerFile(sourceDropdownValue, analysis="Cluster Analysis"):
                nameDropdownOptions.append({"label": sourceName, "value": sourceFile})

        if len(nameDropdownOptions) == 0:
            nameDropdownValue = False
            nameDropdownOptions = [dict(label="No Reference", value=False)]
        elif nameDropdownValue is None:
            nameDropdownValue = defaultParameters["Source Name"]
        elif nameDropdownValue not in [option["value"] for option in nameDropdownOptions]:
            nameDropdownValue = nameDropdownOptions[0]["value"]
        else:
            pass

        ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
        if ctxIdStr == "" or ctxIdStr == 'User Session ID':
            sourceButtonDisabled, nameButtonDisabled = False, False
            sourceButtonActive = False
            nameButtonActive = False
        else:
            ctxId = json.loads(ctxIdStr)
            if ctxId["label"] == "Marker Source":
                sourceButtonActive = not sourceButtonActive
                if sourceButtonActive:
                    nameButtonDisabled = True
                    nameButtonActive = False
                else:
                    nameButtonDisabled = False
            elif ctxId["label"] == "Source Name":
                nameButtonDisabled = False
                nameButtonActive = not nameButtonActive
            else:
                raise ValueError("Unexpected input received: {}".format(ctxIdStr))
        sourceDropdownDisabled = not sourceButtonActive
        nameDropdownDisabled = not nameButtonActive

    return (
        sourceButtonActive, sourceButtonDisabled,
        sourceDropdownValue, sourceDropdownOptions, sourceDropdownDisabled,
        nameButtonActive, nameButtonDisabled,
        nameDropdownValue, nameDropdownOptions, nameDropdownDisabled
    )


@callback(
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Graph', 'index': MATCH, "graphIndex": 0
        },
        "figure"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Graph', 'index': MATCH, "graphIndex": 1
        },
        "figure"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download"
        },
        "data"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
        },
        "value"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
        },
        "options"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 0
        },
        "disabled"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 2
        },
        "value"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 2
        },
        "options"
    ),
    Output(
        {
            'class': 'markerGeneScoring', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropdownIndex": 2
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=State('User Session ID', 'data'),
        dataID=State(
            {
                'class': 'markerGeneScoring', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "markerGeneScoring", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        refParameters=(
            Input(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Marker Source", 'type': 'Button', 'index': MATCH,
                },
                "active"
            ),
            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Marker Source", 'type': 'Dropdown', 'index': MATCH,
                },
                "value"
            ),

            Input(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Source Name", 'type': 'Button', 'index': MATCH,
                },
                "active"
            ),
            State(
                {
                    'class': 'markerGeneScoring', 'group': 'graph',
                    "label": "Source Name", 'type': 'Dropdown', 'index': MATCH,
                },
                "value"
            ),
        ),
        plotParameters=(
            Input(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "dropdownIndex": 0,
                },
                "value"
            ),

            Input(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Button", "index": MATCH, "inputIndex": 1,
                },
                "active"
            ),
            State(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Input", "index": MATCH, "inputIndex": 1,
                },
                "value"
            ),

            Input(
                {
                    "class": "markerGeneScoring", "group": "graph",
                    "type": "Dropdown", "index": MATCH, "dropdownIndex": 2,
                },
                "value"
            ),
        ),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        export=Input(
            {
                'class': "markerGeneScoring", 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit",
            },
            "n_clicks"
        )
    )
)
def returnMarkerGeneScoringGraph(
        userSessionId, dataID, defaultParameters,
        refParameters, plotParameters, refresh_clusterHistoryRecorder,
        export
):
    # cellCluster(dropdown) dataSource(dropdown) GeneNum(Input)
    (
        sourceButtonActive, sourceDropdownValue,
        nameButtonActive, nameDropdownValue,
    ) = refParameters
    cellClusterValue, geneNumActive, geneNumValue, cellTypeValue = plotParameters

    if cellClickManager.currentData != dataID:
        scoreFigure = dash.no_update
        dotFigure = dash.no_update
        exportDf = dash.no_update
        cellClusterValue, cellClusterOptions, cellClusterDisabled = dash.no_update, dash.no_update, True
        cellTypeValue, cellTypeOptions, cellTypeDisabled = dash.no_update, dash.no_update, True
    else:
        if sourceButtonActive or nameButtonActive or geneNumActive:
            scoreFigure = dash.no_update
            dotFigure = dash.no_update
            exportDf = dash.no_update
            cellClusterValue, cellClusterOptions, cellClusterDisabled = dash.no_update, dash.no_update, dash.no_update
            cellTypeValue, cellTypeOptions, cellTypeDisabled = dash.no_update, dash.no_update, dash.no_update
        else:
            adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
            clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
            selectedCellsRecorder = cellClickManager.selectedCellsRecorder
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            cellClusterOptions = sorted(annotationSeries.unique())

            if not cellClusterValue:
                cellClusterValue = defaultParameters["Cell Cluster"]
            elif (cellClusterValue not in cellClusterOptions) and (cellClusterValue != "selected"):
                cellClusterValue = cellClusterOptions[0]
            else:
                pass
            cellClusterOptions = returnDropdownOptions(cellClusterOptions, ["selected"], [])
            cellClusterDisabled = False

            if cellClusterValue == "selected":
                cellIDs = selectedCellsRecorder.selectedCells
            else:
                cellIDs = cellClusterValue
                # by experience, "one vs rest" is better than "A vs B vs C"
                # cellIDs = clusterHistoryRecorder.returnCellIDs(cellClusterValue)

            if sourceDropdownValue not in returnMarkerSource(marker_ref_validation):
                refData = nameDropdownValue
                refCellClick = cellClickManager.get(refData)
                refClusterCol = refCellClick.clusterHistoryRecorder.refCol
                refRdataProcessor = cellClickManager.get(refData).adataProcessor
                refAdata = refRdataProcessor.adata
                key_added = "Gene_{}".format(geneNumValue)
                if ("{}_annotation".format(key_added) in refAdata.uns) and (refAdata.uns["{}_annotation".format(key_added)] == refAdata.obs[refClusterCol]):
                    markerDf = pd.DataFrame(refRdataProcessor.adata.uns[key_added]["names"])
                else:
                    markerDf = refRdataProcessor.returnMarkerDf(
                        key_added=key_added, groupBy=refClusterCol,
                        mu=1, remove_lowly_expressed=True,
                    )
                # if len(markerDf) < geneNumValue:
                #     raise ValueError("")
                markerDict = markerDf.to_dict(orient="list")
                # title = refAdata
            else:
                markerFile = nameDropdownValue
                with open(markerFile, "r") as f:
                    markerDict = json.load(f)
                # title = os.path.basename(refData).split(".")[0]  # assert only one "."

            scoreFigure, exportDf, marker_cosg = adataProcessor.returnMarkerGeneScoringPlot(
                cellIDs, annotation="selected" if cellClusterValue=="selected" else annotationSeries,
                markerDict=markerDict, geneUsed=geneNumValue, markerUsed=5,
                title=cellClusterValue
            )

            cellTypeOptions = exportDf.groupby("cluster").apply(
                lambda subDf: subDf["score"].median()
            ).sort_values(ascending=False).index
            cellTypeValue, cellTypeOptions = returnDropdown(list(cellTypeOptions), value=cellTypeValue, sort=False)
            cellTypeDisabled = False

            group_by = clusterHistoryRecorder.returnAnnotation()
            dotFigure, exportDf_ = adataProcessor.get_dot_plot(
                var_names=markerDict[cellTypeValue][:geneNumValue], groupby=group_by
            )

    export = checkExport(dash.callback_context, index=0)
    if export:
        exportDf = dash.dcc.send_data_frame(exportDf.to_csv, "Cluster Evaluation.csv")
    else:
        exportDf = dash.no_update

    return (
        scoreFigure, dotFigure, exportDf,
        cellClusterValue, cellClusterOptions, cellClusterDisabled,
        cellTypeValue, cellTypeOptions, cellTypeDisabled
    )