#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_7_reAnnotation.py.py
@time: 2023/11/7 17:16
"""
import dash

from callbacks.callbacks_6_clusterAnalysis import *


@callback(
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Cell Selection",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Cell Selection",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "options"
    ),

    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Cell Selection",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Cell Selection",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "options"
    ),

    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Cell Selection",
            "label_name": "Table Content", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Cell Selection",
            "label_name": "Table Content", "type": "Dropdown"
        },
        "options"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
    ),
)
def returnCellSelectionForm(userSessionId, refresh_annotationTypeRecorder):
    if userSessionId is None:
        (
            embeddingValue, embeddingOptions,
            annotationValue, annotationOptions,
            tableContentValue, tableContentOptions,
        ) = (
            None, [],
            None, [],
            None, [],
        )
    else:
        adata = cellClickManager.returnAdata()

        embeddings = resortObsm(adata.obsm.keys())
        embeddingValue, embeddingOptions = returnDropdown(embeddings, sort=False)

        annotationTypeRecorder = cellClickManager.annotationTypeRecorder
        annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotation()
        annotationValue, annotationOptions = returnDropdown(annotationOptions, last=["none"], value=annotationValue)

        tableContentValue, tableContentOptions = returnDropdown(["Meta Data", "Gene Expression"], sort=False)

    return embeddingValue, embeddingOptions, annotationValue, annotationOptions, tableContentValue, tableContentOptions



@callback(
    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Graph", "index": MATCH,
        },
        "figure"
    ),

    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Table", "index": MATCH,
        },
        "data"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Table", "index": MATCH,
        },
        "columns"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Table", "index": MATCH,
        },
        'sort_by'
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Table", "index": MATCH,
        },
        'filter_query'
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Table", "index": MATCH,
        },
        "page_current"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            "type": "Table", "index": MATCH,
        },
        "page_count"
    ),

    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
        },
        "value"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
        },
        "options"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
        },
        "disabled"
    ),

    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Dropdown', 'index': MATCH, 'label': ALL,
        },
        "value"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Dropdown', 'index': MATCH, 'label': ALL,
        },
        "options"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Dropdown', 'index': MATCH, 'label': ALL,
        },
        "disabled"
    ),
    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Button', 'index': MATCH, 'label': ALL,
        },
        "disabled"
    ),

    Output(
        {
            "class": "cellSelection", "group": "graph",
            'type': 'Download', 'index': MATCH, "function": "Download"
        },
        "data"
    ),
    inputs=dict(
        # userSessionId=Input("User Session ID", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        dataID=State(
            {
                "class": "cellSelection", "group": "graph",
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "cellSelection", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        plotParameters=(
                Input(
                    {
                        "class": "cellSelection", "group": "graph",
                        'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
                    },
                    "value"
                ),
                # Input(
                #     {
                #         "class": "cellSelection", "group": "graph",
                #         'type': 'Dropdown', 'index': MATCH, 'label': ALL,
                #     },
                #     "value"
                # ),
                Input("refresh_selectedCellsRecorder", "data"),
                Input("refresh_fixedCellsRecorder", "data"),
                State("fixSelection", "active"),
        ),
        tableShowContentParameters=(
            Input(
                {
                    "class": "cellSelection", "group": "graph", "type": "Table", "index": MATCH,
                },
                'sort_by'
            ),
            Input(
                {
                    "class": "cellSelection", "group": "graph", "type": "Table", "index": MATCH,
                },
                'filter_query'
            ),
            Input(
                {
                    "class": "cellSelection", "group": "graph", "type": "Table", "index": MATCH,
                },
                "page_current"
            ),
        ),
        modifyColumnParameters=(
            State(
                {
                    "class": "cellSelection", "group": "graph",
                    'type': 'Dropdown', 'index': MATCH, 'label': "Add Column",
                },
                "value"
            ),
            State(
                {
                    "class": "cellSelection", "group": "graph",
                    'type': 'Dropdown', 'index': MATCH, 'label': "Remove Column",
                },
                "value"
            ),
            Input(
                {
                    "class": "cellSelection", "group": "graph",
                    'type': 'Button', 'index': MATCH, 'label': "Add Column",
                },
                "n_clicks"
            ),
            Input(
                {
                    "class": "cellSelection", "group": "graph",
                    'type': 'Button', 'index': MATCH, 'label': "Remove Column",
                },
                "n_clicks"
            ),
        ),
        exportClick=Input(
            {
                "class": "cellSelection", "group": "graph",
                'type': 'Button', 'index': MATCH, "function": "Submit"
            },
            "n_clicks"
        ),
    ),
)
def returnCellSelectionGraph(
    refresh_annotationTypeRecorder, refresh_clusterHistoryRecorder, dataID,
    defaultParameters, plotParameters, tableShowContentParameters, modifyColumnParameters,
    exportClick,
):
    #  ["Embedding", "Annotation", "Table Content",]
    #  ["Add Columns", "Remove Columns"]
    (
        figure,
        data, columns, sort_by, filter_query, page_current, page_count, # table
        embeddingValue, embeddingOptions, embeddingDisabled,
        annotationValue, annotationOptions, annotationDisabled,
        tableContentValue, tableContentOptions, tableContentDisabled,
        addColValue, addColOptions, addColDisabled, addColDisabled_button,
        removeColValue, removeColOptions, removeColDisabled, removeColDisabled_button,
        selectCellsDisabled,
        exportDf
    ) = [dash.no_update] * (1+6+3*3+4*2+1+1)

    adata = cellClickManager.returnAdata()
    adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
    annotationTypeRecorder = cellClickManager.annotationTypeRecorder
    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
    selectedCellsRecorder = cellClickManager.selectedCellsRecorder
    fixedCellsRecorder = cellClickManager.fixedCellsRecorder
    tableManager = cellClickManager.cellTable
    annotationTypeDict = cellClickManager.annotationTypeRecorder.annotationTypeDict

    if cellClickManager.currentData != dataID:
        embeddingDisabled, annotationDisabled, tableContentDisabled = [True, True, True]
        addColDisabled_button, removeColDisabled_button, selectCellsDisabled = [True, True, True]
    else:
        if defaultParameters["Embedding"] is None or defaultParameters["Annotation"] is None:
            # default canvas, should not been updated
            raise PreventUpdate

        (
            [embeddingValue, annotationValue, tableContentValue],
            refresh_refresh_annotationTypeRecorder, refresh_fixedCellsRecorder,
            active
        ) = plotParameters
        selectedCells = selectedCellsRecorder.selectedCells

        # return the embedding and annotation input group
        if embeddingValue is None or annotationValue is None:
            # init the input group
            embeddingValue, annotationValue = defaultParameters["Embedding"], defaultParameters["Annotation"]

            embeddingOptions = returnDropdownOptions(resortObsm(adata.obsm.keys()), sort=False)
        else:
            embeddingOptions = dash.no_update
        annotationOptions = returnDropdownOptions(annotationTypeRecorder.returnTextAnnotation()[1], last=["none"])

        fixedCells = fixedCellsRecorder.fixedCells if active else None
        if annotationValue == clusterHistoryRecorder.refCol:
            refAnnotation = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
        else:
            refAnnotation = None

        figure, exportDf = adataProcessor.get_fig_by_embedding(
            embeddingValue, annotationValue, selectedCells, fixedCells, refAnnotation
        )

        export = checkExport(dash.callback_context, index=0)
        if export:
            fileName = "cellEmbedding.csv"
            exportDf = dcc.send_data_frame(exportDf.to_csv, fileName)
        else:
            exportDf = dash.no_update

        #### Cells Table
        def updateCellsTable(currentPage=0):
            tableManager.setCacheData()
            return tableManager.returnShowData(currentPage), currentPage, tableManager.returnPageCount()

        def returnColumnsControllerDropdown(removable=True):
            optionsList = tableManager.returnRemoveAbleColumns() if removable else tableManager.returnAddableColumns()
            value = optionsList[0] if len(optionsList) > 0 else None
            options = returnDropdownOptions(optionsList)
            return value, options

        # read input
        sort_by, filter_query, page_current = tableShowContentParameters
        addColValue, removeColValue, addClick, removeClick = modifyColumnParameters

        if tableContentValue is None:
            tableContentValue = defaultParameters["Table Content"]
        tableContentOptions = returnDropdownOptions(["Meta Data", "Gene Expression"])

        ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
        if ctxIdStr == '': # table init
            tableManager.initSwitcher()
            tableManager.setSelectedCells(selectedCells)
            data, page_current, page_count = updateCellsTable()
            columns = tableManager.returnTableColumns(annotationTypeDict)
            addColValue, addColOptions = returnColumnsControllerDropdown(False)
            removeColValue, removeColOptions = returnColumnsControllerDropdown(True)
        else:
            if ctxIdStr == "refresh_selectedCellsRecorder":
                tableManager.setSelectedCells(selectedCells)
            elif ctxIdStr == "refresh_annotationTypeRecorder":
                if tableManager.switcher[0] == "metaData":
                    columns = tableManager.returnTableColumns(annotationTypeDict)
                else:
                    raise PreventUpdate
            elif ctxIdStr == "refresh_clusterHistoryRecorder":
                if clusterHistoryRecorder.refCol:
                    refValues = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
                    refName = clusterHistoryRecorder.refCol
                    tableManager.modifyCellTabelData("metaData", refName, refValues)
                    data = tableManager.returnShowData(page_current)

                addColValue, addColOptions = returnColumnsControllerDropdown(False)
                removeColValue, removeColOptions = returnColumnsControllerDropdown(True)
            elif ctxIdStr == "refresh_fixedCellsRecorder":
                pass
            else:
                ctxId = json.loads(ctxIdStr)
                description = "metaData" if tableContentValue == "Meta Data" else "expressionData"
                tableManager.setSwitcher(description=description)

                if ctxId.get("dropDownIndex", 0) == 2: # change table content
                    tableManager.setRecords("filter_query", "")
                    tableManager.setRecords("sort_by", [])
                    filter_query = tableManager.returnRecords("filter_query")
                    sort_by = tableManager.returnRecords("sort_by")

                    addColValue, addColumnOptions = returnColumnsControllerDropdown(False)
                    removeColValue, removeColOptions = returnColumnsControllerDropdown(True)
                    columns = tableManager.returnTableColumns(annotationTypeDict)

                    data,  page_current, page_count = updateCellsTable()
                elif ctxId.get('label', None) in ["Add Column", "Remove Column"]:
                    if ctxId["label"] == "Add Column":
                        tableManager.modifyShowColumns(addColumn=addColValue)
                    else:
                        tableManager.modifyShowColumns(removeColumn=removeColValue)

                    addColValue, addColOptions = returnColumnsControllerDropdown(False)
                    removeColValue, removeColOptions = returnColumnsControllerDropdown(True)
                    columns = tableManager.returnTableColumns(annotationTypeDict)

                    data = tableManager.returnShowData(page_current)
                else:
                    triggeredValue = dash.callback_context.triggered[0]["prop_id"].split(".")[1]
                    if triggeredValue == "sort_by":
                        tableManager.setRecords("sort_by", sort_by)
                        data, page_current, page_count = updateCellsTable()
                    elif triggeredValue == "filter_query":
                        tableManager.setRecords("filter_query", filter_query)
                        data, page_current, page_count = updateCellsTable()
                    elif triggeredValue == "page_current":
                        data = tableManager.returnShowData(page_current)
                    else:
                        pass


    return (
        figure,
        data, columns, sort_by, filter_query, page_current, page_count,
        [embeddingValue, annotationValue, tableContentValue],
        [embeddingOptions, annotationOptions, tableContentOptions],
        [embeddingDisabled, annotationDisabled, tableContentDisabled],
        [addColValue, removeColValue],
        [addColOptions, removeColOptions],
        [addColDisabled, removeColDisabled],
        [addColDisabled_button, removeColDisabled_button, selectCellsDisabled],
        exportDf
    )


@callback(
Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Dimension Reduction", "type": "Button"
        },
        "active"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Cell Reclustering", "type": "Button"
        },
        "active"
    ),

    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "dimension_Method", "type": ALL
        },
        "style"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "N PCs", "type": ALL
        },
        "style"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "N Neighbors", "type": ALL
        },
        "style"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Min Dist", "type": ALL
        },
        "style"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Metric", "type": ALL
        },
        "style"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Method", "type": ALL
        },
        "style"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Resolution", "type": ALL
        },
        "style"
    ),
    inputs=dict(
        clicks=(
            Input(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Dimension Reduction", "type": "Button"
                },
                "n_clicks"
            ),
            Input(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Cell Reclustering", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        actives=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Dimension Reduction", "type": "Button"
                },
                "active"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Cell Reclustering", "type": "Button"
                },
                "active"
            ),
        ),
        ids=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "dimension_Method", "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N PCs", "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N Neighbors", "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Min Dist", "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Metric", "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Method", "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Resolution", "type": ALL
                },
            "id"
            )
        ),
        styles=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "dimension_Method", "type": ALL
                },
                "style"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N PCs", "type": ALL
                },
                "style"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N Neighbors", "type": ALL
                },
                "style"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Min Dist", "type": ALL
                },
                "style"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Metric", "type": ALL
                },
                "style"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Method", "type": ALL
                },
                "style"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Resolution", "type": ALL
                },
            "style"
            )
        ),
        dim_method_value=Input(
            {
                "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                "label_name": "dimension_Method", "type": "Dropdown"
            },
            "value"
        )
    ),
)
def returnReClusterStyles(clicks, actives, ids, styles, dim_method_value):

    def returnInputStyle(inputIds, inputStyles, labels, active=None):
        newStyles = []
        for id, style in zip(inputIds, inputStyles):
            if id["label_name"] in labels:
                # init
                if style is None:
                    style = {"display": "none"}
                elif "display" not in style:
                    style["display"] = "none"
                else:
                    if active is not None:
                        style["display"] = "block" if active else "none"
                    else:
                        style["display"] = "block" if style["display"] == "none" else "none"
            newStyles.append(style)
        return newStyles

    dimLabels = ["dimension_Method", "N PCs", "N Neighbors", "Min Dist", "Metric"]
    cluLabels = ["Method", "Resolution"]

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    try:
        ctxId = json.loads(ctxIdStr)
        labels = cluLabels if ctxId["label_name"]=="Cell Reclustering" else dimLabels
        actives = [
            not actives[0] if ctxId["label_name"]=="Dimension Reduction" else actives[0],
            True
        ]
    except json.JSONDecodeError:
        labels = dimLabels
        actives = [False, True]

    newStyles = []
    for inputIds, inputStyles in zip(ids, styles):
        if labels == cluLabels:
            newStyles.append(returnInputStyle(inputIds, inputStyles, labels))
        else:
            newStyles.append(returnInputStyle(inputIds, inputStyles, labels, active=actives[0]))

    def returnDimLabelStyle(inputIds, inputStyles):
        switchDict = {
            "N PCs": "block",
            "N Neighbors": "block" if dim_method_value in ["UMAP"] else "none",
            "Min Dist": "block" if dim_method_value in ["UMAP"] else "none",
            "Metric": "block" if dim_method_value in ["UMAP", "t-SNE"] else "none",
        }
        newStyles = []
        for id, style in zip(inputIds, inputStyles):
            if id["label_name"] in switchDict:
                style["display"] = switchDict[id["label_name"]]
            newStyles.append(style)
        return newStyles

    if actives[0]:
        returnStyles = []
        for inputIds, inputStyles in zip(ids, newStyles):
            returnStyles.append(returnDimLabelStyle(inputIds, inputStyles))
    else:
        returnStyles = newStyles

    return actives + returnStyles


@callback(
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Cluster", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Cluster", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Cluster", "type": "Dropdown"
        },
        "disabled"
    ),

    # Output(
    #     {
    #         "card_name": "Cell Reannotation", "form_name": "Re-cluster",
    #         "label_name": "Prefix", "type": "Input"
    #     },
    #     "disabled"
    # ),

    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "dimension_Method", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "dimension_Method", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "N PCs", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "N Neighbors", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Min Dist", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Metric", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Metric", "type": "Dropdown"
        },
        "options"
    ),


    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Method", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Method", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Resolution", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Re-cluster",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        dim_method=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "dimension_Method", "type": "Dropdown"
                },
                "value"
            ),
        ),
        n_pcs=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N Neighbors", "type": "Input"
                },
                "value"
            ),
        ),
        n_nei=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N Neighbors", "type": "Input"
                },
                "value"
            ),
        ),
        min_dist=(
            State(
                {
                "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                "label_name": "Min Dist", "type": "Input"
                },
            "value"
            ),
        ),
        metric=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Metric", "type": "Dropdown"
                },
                "value",
            ),
        ),
        method=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Method", "type": "Dropdown"
                },
                "value"
            ),
        ),
        resolution=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Resolution", "type": "Input"
                },
                "value"
            ),
        ),
    ),
)
def returnReClusterForm(
    userSessionId, refresh_clusterHistoryRecorder,
    dim_method, n_pcs, n_nei, min_dist, metric,
    method, resolution
):
    if userSessionId is None:
        raise PreventUpdate

    def initDropdown(withRecord=False):
        if withRecord:
            value = "selected"
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            optionList = sorted(annotationSeries.unique())
            options = returnDropdownOptions(optionList, ["selected"], [])
            disabled = False
            buttonDisabled = False
        else:
            value = False
            options = [dict(label="No Reference", value=False)]
            disabled = True
            buttonDisabled = True
        return [value, options, disabled], [buttonDisabled]

    dim_method = list(returnDropdown(["UMAP", "t-SNE", "PCA"], value=dim_method[0], sort=False))
    n_pcs = [int(n_pcs[0]) if n_pcs[0] else 50]
    n_nei = [int(n_nei[0]) if n_nei[0] else 15]
    min_dist = [float(min_dist[0]) if min_dist[0] else 0.5]
    metricOptions = [
        'cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan',
        'braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming',
        'jaccard', 'kulsinski', 'mahalanobis', 'minkowski', 'rogerstanimoto', 'russellrao',
        'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'
    ]
    metric = [
        metric[0] if metric[0] else 'euclidean',
        returnDropdownOptions(metricOptions),
    ]

    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
    record = False if clusterHistoryRecorder.refCol is None else True
    dropdown, button = initDropdown(withRecord=record)

    method = list(returnDropdown(["Leiden", "Louvain"], value=method[0], sort=False))
    # prefix = [not record]
    resolution = [0.5 if resolution[0] is None else dash.no_update]

    if userSessionId is None:
        raise PreventUpdate


    # return dropdown + prefix + dim_method + npcs + n_neighbors + min_dist + metric + method + resolution + button
    return (
        dropdown +
        dim_method + n_pcs + n_nei + min_dist + metric +
        method + resolution + button
    )


@callback(
    Output("refresh_UserSessionIDRecorder", "data"),
    inputs=dict(
        clusterValue=State(
            {
                "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                "label_name": "Cluster", "type": "Dropdown"
            },
            "value"
        ),
        dim_method=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "dimension_Method", "type": "Dropdown"
                },
                "value"
            ),
        ),
        n_pcs=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N Neighbors", "type": "Input"
                },
                "value"
            ),
        ),
        n_nei=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "N Neighbors", "type": "Input"
                },
                "value"
            ),
        ),
        min_dist=(
            State(
                {
                "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                "label_name": "Min Dist", "type": "Input"
                },
            "value"
            ),
        ),
        metric=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Metric", "type": "Dropdown"
                },
                "value",
            ),
        ),
        method=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Method", "type": "Dropdown"
                },
                "value"
            ),
        ),
        resolution=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Resolution", "type": "Input"
                },
                "value"
            ),
        ),
        actives=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Dimension Reduction", "type": "Button"
                },
                "active"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                    "label_name": "Cell Reclustering", "type": "Button"
                },
                "active"
            ),
        ),
        submit=Input(
            {
                "card_name": "Cell Reannotation", "form_name": "Re-cluster",
                "label_name": "Submit", "type": "Button"
            },
            "n_clicks"
        ),
    ),
    prevent_initial_call=True,
)
def reClusterAdata(
    clusterValue,
    dim_method, n_pcs, n_nei, min_dist, metric,
    method, resolution,
    actives, submit,
):
    PCAKwargs = {
        "n_components": n_pcs[0],
        "random_state": 4712,
    }

    neighborKwargs = {
        "n_neighbors": n_nei[0],
        "n_pcs": n_pcs[0],
        "metric": metric[0],
        "random_state": 4712,
    }

    umapKwargs = {
        "min_dist": min_dist[0],
        "random_state": 4712,
    }

    t_sneKwargs = {
        "n_pcs": n_pcs[0],
        "metric": metric[0],
        "random_state": 4712,
    }

    adata = cellClickManager.returnAdata()
    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
    if clusterValue == "selected":
        cellIDs = cellClickManager.selectedCellsRecorder.selectedCells
    else:
        cellIDs = clusterHistoryRecorder.returnCellIDs(clusterValue)
    subAdata = adata[cellIDs].copy()
    timeArray = time.localtime(time.time())
    sessionID = time.strftime("%Y%m%d%H%M%S", timeArray)
    cellClickManager.add_adata(adata=subAdata, ID=sessionID, to="CellClick")
    cellClickManager.load(ID=sessionID)

    if actives[0]:
        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
        adataProcessor.scDataPreprocessing(
            qc="Dimension Reduction", dimRedMethod=dim_method[0],
            PCAKwargs=PCAKwargs, neighborKwargs=neighborKwargs, umapKwargs=umapKwargs, t_sneKwargs=t_sneKwargs,

        )
    cellClickManager.refreshRecoder(
        recoder="clusterHistoryRecorder", method="init",
        refExisted=False, refCol=None,
        cluster_method=method[0], resolution=float(resolution[0]),
    )
    return sessionID



@callback(
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Merge Data",
            "label_name": "Ref Data", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Merge Data",
            "label_name": "Ref Data", "type": "Input"
        },
        "disabled"
    ),


    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Merge Data",
            "label_name": "Other Data", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Merge Data",
            "label_name": "Other Data", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Merge Data",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        cellClickAlert=Input("CellClickAlert", "children"),
    ),
)
def returnMergeData(userSessionId, cellClickAlert):
    if userSessionId is None:
        refDataValue = "None"
    else:
        refDataValue = userSessionId

    refDataDisabled = True

    datas = cellClickManager.CellClickID.copy()
    if len(datas) <= 1:  # include userSessionId is None
        otherDataValue = "None"
        otherDataOptions = returnDropdownOptions(["None"])
    else:
        datas.remove(refDataValue)
        otherDataValue = datas[0]
        otherDataOptions = returnDropdownOptions(datas)

    if (refDataValue != "None") and (otherDataValue != "None"):
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        otherClusterHistoryRecoder = cellClickManager.CellClick[otherDataValue].clusterHistoryRecorder
        if not (clusterHistoryRecorder and clusterHistoryRecorder.refCol):
            submitDisabled = True
        elif not (otherClusterHistoryRecoder and otherClusterHistoryRecoder.refCol):
            submitDisabled = True
        else:
            submitDisabled = False
    else:
        submitDisabled = True

    return refDataValue, refDataDisabled, otherDataValue, otherDataOptions, submitDisabled


@callback(
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Reannotation",
            "label_name": "Raw Name", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Reannotation",
            "label_name": "Raw Name", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Reannotation",
            "label_name": "Raw Name", "type": "Dropdown"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Reannotation",
            "label_name": "New Name", "type": "Input"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Cell Reannotation", "form_name": "Reannotation",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
    ),
)
def returnAnnotationForm(userSessionId, refresh_clusterHistoryRecorder):
    def initDropdown(withRecord=False):
        if withRecord:
            value = "selected"
            annotationSeries = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
            optionList = sorted(annotationSeries.unique())
            options = returnDropdownOptions(optionList, ["selected"], [])
            disabled = False
        else:
            value = False
            options = [dict(label="No Reference", value=False)]
            disabled = True
        return [value, options, disabled]

    if userSessionId is None:
        dropdown = [None, [], True]
        inputAndSubmit = [True, True]
    else:
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder

        record = False if clusterHistoryRecorder.refCol is None else True
        dropdown = initDropdown(withRecord=record)
        inputAndSubmit = [not record, not record]
    return dropdown + inputAndSubmit


# @callback(
#     Output(
#         {
#             "card_name": "Cell Reannotation", "form_name": "Visualization",
#             "label_name": "Cluster Name", "type": "Dropdown"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "card_name": "Cell Reannotation", "form_name": "Visualization",
#             "label_name": "Cluster Name", "type": "Dropdown"
#         },
#         "options"
#     ),
#     Output(
#         {
#             "card_name": "Cell Reannotation", "form_name": "Visualization",
#             "label_name": "Submit", "type": "Button"
#         },
#         "disabled"
#     ),
#     inputs=dict(
#         userSessionId=Input("User Session ID", "data"),
#         refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
#     ),
# )
# def returnVisualizationForm(userSessionId, refresh_clusterHistoryRecorder):
#     if userSessionId is None:
#         value, options, disabled = None, [], True
#     else:
#         clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
#         record = False if clusterHistoryRecorder.refCol is None else True
#         if record:
#             clusterSeries = clusterHistoryRecorder.returnAnnotation()
#             clusters = sorted(clusterSeries.unique())
#         else:
#             clusters = []
#         options = [
#             dict(value=cluster, label=cluster, disabled=not record) for cluster in ["selected", "all"] + clusters
#         ]
#         value = options[0]["value"]
#         disabled = not record
#     return value, options, disabled


# @callback(
#     Output(
#         {
#             "class": "visualization", "group": "graph",
#             "type": "Graph", "index": MATCH,
#         },
#         "figure"
#     ),
#     Output(
#         {
#             'class': "visualization", 'group': 'graph',
#             'type': 'Download', 'index': MATCH, "function": "Download",
#         },
#         "data"
#     ),
#     Output(
#         {
#             "class": "visualization", "group": "graph",
#             "type": "Dropdown", "index": MATCH, "dropDownIndex": 0,
#         },
#         "value"
#     ),
#     Output(
#         {
#             "class": "visualization", "group": "graph",
#             "type": "Dropdown", "index": MATCH, "dropDownIndex": 0,
#         },
#         "options"
#     ),
#     Output(
#         {
#             "class": "visualization", "group": "graph",
#             "type": "Dropdown", "index": MATCH, "dropDownIndex": 0,
#         },
#         "disabled"
#     ),
#     # Output(
#     #     {
#     #         "class": "visualization", "group": "graph",
#     #         "type": "Dropdown", "index": MATCH, "dropDownIndex": 1,
#     #     },
#     #     "value"
#     # ),
#     # Output(
#     #     {
#     #         "class": "visualization", "group": "graph",
#     #         "type": "Dropdown", "index": MATCH, "dropDownIndex": 1,
#     #     },
#     #     "options"
#     # ),
#     inputs=dict(
#         userSessionId=State('User Session ID', 'data'),
#         dataID=State(
#             {
#                 'class': 'visualization', 'group': 'graph',
#                 'type': "Label", 'function': "Data ID",
#                 'index': MATCH,
#             },
#             "children"
#         ),
#         refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
#         defaultParameters=State(
#             {
#                 "class": "visualization", "group": "graph",
#                 "type": "Store", "index": MATCH
#             },
#             "data"
#         ),
#         plotParameters=(
#             Input(
#                 {
#                     "class": "visualization", "group": "graph",
#                     "type": "Dropdown", "index": MATCH, "dropDownIndex": 0,
#                 },
#                 "value"
#             ),
#         ),
#         export=Input(
#             {
#                 'class': "visualization", 'group': 'graph',
#                 'type': 'Button', 'index': MATCH, "function": "Submit",
#             },
#             "n_clicks"
#         )
#     ),
# )
# def returnVisualizationGraph(
#         userSessionId, dataID, refresh_clusterHistoryRecorder, defaultParameters, plotParameters, export
# ):
#     clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
#     selectedCellsRecorder = cellClickManager.selectedCellsRecorder
#     adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
#
#     if cellClickManager.currentData != dataID:
#         (
#             figure, exportData,
#             clusterNameValue, clusterNameOptions, clusterNameDisabled,
#         ) = (
#             dash.no_update, dash.no_update,
#             dash.no_update, dash.no_update, True
#         )
#     else:
#         clusterNameValue = plotParameters[0]
#
#         if clusterNameValue is None:
#             # init visualization graph
#             clusterNameValue = defaultParameters["Cluster Name"]
#
#         # in graph, the ref col has been set
#         clusterSeries = clusterHistoryRecorder.returnAnnotation()
#         clusters = sorted(clusterSeries.unique())
#         clusterNameOptions = [
#             dict(value=cluster, label=cluster) for cluster in ["selected", "all"] + clusters
#         ]
#
#         annotationHistory = pd.DataFrame.from_dict(clusterHistoryRecorder.records)
#         annotationHistory.index = clusterHistoryRecorder.cellIDs
#         sortedCol = sorted(annotationHistory.columns, key=lambda col: int(col.split("_")[1]))
#         annotationHistory = annotationHistory[sortedCol]
#         if clusterNameValue == "selected":
#             selectedCells = selectedCellsRecorder.selectedCells
#             annotationHistory = annotationHistory.loc[selectedCells]
#         elif clusterNameValue == "all":
#             pass
#         else:
#             annotation = clusterHistoryRecorder.returnAnnotation()
#             selectedCells = annotation[annotation == clusterNameValue].index
#             annotationHistory = annotationHistory.loc[selectedCells]
#
#         figure = adataProcessor.returnSankeyFig(annotationHistory)
#         # exportDf = annotationHistory
#
#         if export:
#             adataProcessor.write_adata(path=os.path.join(tmpDir, "{}.h5ad".format(dataID)), annotation=annotationHistory)
#             exportData = dash.dcc.send_file(
#                 os.path.join(tmpDir, "{}.h5ad".format(dataID)),
#                 filename="{}.h5ad".format(dataID),
#                 type="h5ad",
#             )
#             # exportDf = dash.dcc.send_data_frame(exportDf.to_csv, "ClusterVisualization.csv")
#         else:
#             exportData = dash.no_update
#
#         clusterNameDisabled = False
#
#     return (
#         figure, exportData,
#         clusterNameValue, clusterNameOptions, clusterNameDisabled
#     )


@callback(
    Output(
        {"function": "Export", "type": "Download"},
        "data"
    ),
    Output(
        {"function": "Export", "type": "Button"},
        "disabled"
    ),
    inputs=dict(
        userSessionId=State('User Session ID', 'data'),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        export=Input(
            {"function": "Export", "type": "Button"},
            "n_clicks"
        )
    ),
)
def exportData(userSessionId, refresh_clusterHistoryRecorder, export):
    if userSessionId is None:
        return dash.no_update, True

    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr == "refresh_clusterHistoryRecorder":
        if clusterHistoryRecorder and clusterHistoryRecorder.refCol:
            return dash.no_update, False
        else:
            return dash.no_update, True


    adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor

    annotationHistory = pd.DataFrame.from_dict(clusterHistoryRecorder.records)
    annotationHistory.index = clusterHistoryRecorder.cellIDs
    sortedCol = sorted(annotationHistory.columns, key=lambda col: int(col.split("_")[1]))
    annotationHistory = annotationHistory[sortedCol]
    adataProcessor.write_adata(
        path=os.path.join(tmpDir, "{}.h5ad".format(userSessionId)),
        annotation=annotationHistory
    )
    exportData = dash.dcc.send_file(
        os.path.join(tmpDir, "{}.h5ad".format(userSessionId)),
        filename="{}.h5ad".format(userSessionId),
        type="h5ad",
    )

    return exportData, False
