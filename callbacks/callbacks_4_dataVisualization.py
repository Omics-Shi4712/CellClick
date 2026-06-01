#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_4_dataVisualization.py
@time: 2024/11/13 10:34
"""
import scanpy.get

from callbacks.callbacks_3_preprocessing import *


@callback(
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Embedding",
            "label_name": "Gene Name", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Embedding",
            "label_name": "Gene Name", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Embedding",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Embedding",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "options"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
    ),
)
def returnGeneEmbeddingForm(userSessionId):
    if userSessionId is None:
        (
            geneNameValue, geneNameOptions,
            embeddingValue, embeddingOptions,
        ) = (
            None, [],
            None, [],
        )
    else:
        adata = cellClickManager.returnAdata()

        geneNameValue, geneNameOptions = returnDropdown(list(adata.var.index))

        embeddings = resortObsm(adata.obsm.keys())
        embeddingValue, embeddingOptions = returnDropdown(embeddings, sort=False)
    return geneNameValue, geneNameOptions, embeddingValue, embeddingOptions


@callback(
    Output(
        {
            'class': 'geneEmbedding', 'group': 'graph',
            'type': 'Graph', 'index': MATCH,
        },
        "figure"
    ),
    Output(
        {
            'class': 'geneEmbedding', 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download"
        },
        "data"
    ),
    Output(
        {
            'class': 'geneEmbedding', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropDownIndex": ALL
        },
        "value"
    ),
    Output(
        {
            'class': 'geneEmbedding', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropDownIndex": ALL
        },
        "options"
    ),
    Output(
        {
            'class': 'geneEmbedding', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropDownIndex": ALL
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),  # for data change
        dataID=State(
            {
                'class': 'geneEmbedding', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "geneEmbedding", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        plotParameters=Input(
            {
                "class": "geneEmbedding", "group": "graph",
                "type": "Dropdown", "index": MATCH, "dropDownIndex": ALL  # It may be one or two dropdown
            },
            "value"
        ),
        exportClick=Input(
            {
                'class': 'geneEmbedding', 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit"
            },
            "n_clicks"
        ),
    )
)
def returnGeneEmbeddingGraph(userSessionId, dataID, defaultParameters, plotParameters, exportClick):
    if cellClickManager.currentData != dataID:
        figure, data,  = dash.no_update, dash.no_update
        values, options, disabled = [dash.no_update]*2, [dash.no_update]*2, [True]*2
    else:
        adata = cellClickManager.returnAdata()
        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor

        export = checkExport(dash.callback_context, index=0)
        if export:
            import scanpy as sc
            geneValue = plotParameters[0] if plotParameters[0] else defaultParameters["Gene Name"]

            exportDf = sc.get.obs_df(adata, keys=[geneValue])
            fileName = "GeneExpression.csv"

            figure, data, = dash.no_update, dcc.send_data_frame(exportDf.to_csv, fileName)
            values, options = [dash.no_update] * 2, [dash.no_update] * 2
        else:
            geneValue, embeddingValue = plotParameters
            if (not geneValue) or (not embeddingValue):
                geneValue = defaultParameters["Gene Name"]
                geneOptions = returnDropdownOptions(list(adata.var.index))

                embeddingValue = defaultParameters["Embedding"]
                embeddingOptions = returnDropdownOptions(resortObsm(adata.obsm.keys()), sort=False)
            else:
                geneOptions = dash.no_update
                embeddingOptions = dash.no_update

            values = [geneValue, embeddingValue]
            options = [geneOptions, embeddingOptions]

            figure, exportDf = adataProcessor.get_marker_scatter(use_rep=embeddingValue, marker_gene=geneValue)
            data = dash.no_update
        disabled = [False, False]
    return figure, data, values, options, disabled


@callback(
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Dot",
            "label_name": "Gene Name", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Dot",
            "label_name": "Gene Name", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Dot",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Gene Dot",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "options"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
    ),
)
def returnGeneDotForm(userSessionId, refresh_annotationTypeRecorder):
    if userSessionId is None:
        (
            geneNameValue, geneNameOptions,
            annotationValue, annotationOptions,
        ) = (
            None, [],
            None, [],
        )
    else:
        adata = cellClickManager.returnAdata()
        geneNameValue, geneNameOptions = returnDropdown(list(adata.var.index))

        annotationTypeRecorder = cellClickManager.annotationTypeRecorder
        annotationValue, annotationOptions = annotationTypeRecorder.returnTextAnnotation()
        annotationValue, annotationOptions = returnDropdown(annotationOptions, last=["none"], value=annotationValue)
    return geneNameValue, geneNameOptions, annotationValue, annotationOptions


@callback(
    Output(
        {
            'class': 'geneDot', 'group': 'graph',
            'type': 'Graph', 'index': MATCH,
        },
        "figure"
    ),
    Output(
        {
            'class': 'geneDot', 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download"
        },
        "data"
    ),
    Output(
        {
            'class': 'geneDot', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropDownIndex": ALL
        },
        "value"
    ),
    Output(
        {
            'class': 'geneDot', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropDownIndex": ALL
        },
        "options"
    ),
    Output(
        {
            'class': 'geneDot', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, "dropDownIndex": ALL
        },
        "disabled"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),  # for data change
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        dataID=State(
            {
                'class': 'geneDot', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "geneDot", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        plotParameters=Input(
            {
                "class": "geneDot", "group": "graph",
                "type": "Dropdown", "index": MATCH, "dropDownIndex": ALL  # It may be one or two dropdown
            },
            "value"
        ),
        exportClick=Input(
            {
                'class': 'geneDot', 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit"
            },
            "n_clicks"
        ),
    )
)
def returnGeneDotGraph(
        userSessionId, refresh_clusterHistoryRecorder,
        dataID, defaultParameters, plotParameters, exportClick
):
    if cellClickManager.currentData != dataID:
        figure, data,  = dash.no_update, dash.no_update
        values, options, disabled = [dash.no_update]*2, [dash.no_update]*2, [True]*2
    else:
        adata = cellClickManager.returnAdata()
        clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor


        export = checkExport(dash.callback_context, index=0)
        if export:
            import scanpy as sc
            geneValue = plotParameters[0] if plotParameters[0] else defaultParameters["Gene Name"]
            annotationValue = plotParameters[1] if plotParameters[1] else defaultParameters["Annotation"]

            exportDf = sc.get.obs_df(adata, keys=[geneValue, annotationValue])
            fileName = "GeneExpression.csv"

            figure, data, = dash.no_update, dcc.send_data_frame(exportDf.to_csv, fileName)
            values, options = [dash.no_update] * 2, [dash.no_update] * 2
        else:
            geneValue, annotationValue = plotParameters

            if not geneValue:
                geneValue = defaultParameters["Gene Name"]
                geneOptions = [
                    {"label": geneName, "value": geneName} for geneName in adata.var.index
                ]
            else:
                geneOptions = dash.no_update

            if not annotationValue:
                annotationValue = defaultParameters["Annotation"]

            annotationTypeRecorder = cellClickManager.annotationTypeRecorder
            cache, annotationOptions = annotationTypeRecorder.returnTextAnnotation()
            annotationOptions = returnDropdownOptions(annotationOptions)

            if clusterHistoryRecorder.refCol and annotationValue == clusterHistoryRecorder.refCol:
                group_by = clusterHistoryRecorder.returnAnnotation()
            else:
                group_by = annotationValue
            # get_dot_plot(self, var_names, groupby, clusters=[], selectedCells=[])

            figure, exportDf = adataProcessor.get_dot_plot(var_names=geneValue, groupby=group_by)
            data = dash.no_update
            values = [geneValue, annotationValue]
            options = [geneOptions, annotationOptions]

        disabled = [False, False]
    return figure, data, values, options, disabled


@callback(
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Cell Embedding",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Cell Embedding",
            "label_name": "Embedding", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Cell Embedding",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Visualization", "form_name": "Cell Embedding",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "options"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
    ),
)
def returnCellEmbeddingForm(userSessionId, refresh_annotationTypeRecorder):
    if userSessionId is None:
        (
            embeddingValue, embeddingOptions,
            annotationValue, annotationOptions,
        ) = (
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
    return embeddingValue, embeddingOptions, annotationValue, annotationOptions


@callback(
    Output(
        {
            'class': 'cellEmbedding', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
        },
        "value"
    ),
    Output(
        {
            'class': 'cellEmbedding', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
        },
        "options"
    ),
    Output(
        {
            'class': 'cellEmbedding', 'group': 'graph',
            'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
        },
        "disabled"
    ),
    Output(
        {
            "class": "cellEmbedding", "group": "graph",
            "type": "Graph", "index": MATCH,
        },
        "figure"
    ),
    Output(
        {
            'class': 'cellEmbedding', 'group': 'graph',
            'type': 'Download', 'index': MATCH, "function": "Download"
        },
        "data"
    ),
    inputs=dict(
        # when changing data, the two recorder will be updated
        # userSessionId=Input("User Session ID", "data"),
        refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
        refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
        dataID=State(
            {
                'class': 'cellEmbedding', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": "cellEmbedding", "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        plotParameters=(
                Input(
                    {
                        'class': 'cellEmbedding', 'group': 'graph',
                        'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': 0,
                    },
                    "value"
                ),
                Input(
                    {
                        'class': 'cellEmbedding', 'group': 'graph',
                        'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': 1,
                    },
                    "value"
                ),
                Input("refresh_selectedCellsRecorder", "data"),
                Input("refresh_fixedCellsRecorder", "data"),
                State("fixSelection", "active"),
        ),
        exportClick=Input(
            {
                'class': 'cellEmbedding', 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit"
            },
            "n_clicks"
        ),
    ),
)
def returnCellEmbeddingGraph(
        refresh_annotationTypeRecorder, refresh_clusterHistoryRecorder, dataID,
        defaultParameters, plotParameters,
        exportClick
):
    adata = cellClickManager.returnAdata()
    adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
    annotationTypeRecorder = cellClickManager.annotationTypeRecorder
    clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
    selectedCellsRecorder = cellClickManager.selectedCellsRecorder
    fixedCellsRecorder = cellClickManager.fixedCellsRecorder

    if cellClickManager.currentData != dataID:
        return (
            [dash.no_update, dash.no_update], [dash.no_update, dash.no_update], [True, True],
            dash.no_update, dash.no_update
        )
    else:
        if defaultParameters["Embedding"] is None or defaultParameters["Annotation"] is None:
            # default canvas, should not been updated
            raise PreventUpdate
        (
            embeddingValue, annotationValue,
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
            return (
                [embeddingValue, annotationValue], [embeddingOptions, annotationOptions], [False, False],
                figure, dcc.send_data_frame(exportDf.to_csv, fileName)
            )
        else:
            return (
                [embeddingValue, annotationValue], [embeddingOptions, annotationOptions], [False, False],
                figure, dash.no_update
            )


# @callback(
#     Output(
#         {
#             "card_name": "Data Visualization", "form_name": "Cell Stat",
#             "label_name": "x_Annotation", "type": "Dropdown"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "card_name": "Data Visualization", "form_name": "Cell Stat",
#             "label_name": "x_Annotation", "type": "Dropdown"
#         },
#         "options"
#     ),
#     Output(
#         {
#             "card_name": "Data Visualization", "form_name": "Cell Stat",
#             "label_name": "y_Annotation", "type": "Dropdown"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "card_name": "Data Visualization", "form_name": "Cell Stat",
#             "label_name": "y_Annotation", "type": "Dropdown"
#         },
#         "options"
#     ),
#     inputs=dict(
#         userSessionId=Input("User Session ID", "data"),
#         refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
#     ),
# )
# def returnCellStatForm(userSessionId, refresh_annotationTypeRecorder):
#     if userSessionId is None:
#         x_annotationValue, x_annotationOptions, = None, []
#         y_annotationValue, y_annotationOptions, = None, []
#     else:
#         adata = cellClickManager.returnAdata()
#
#         annotationTypeRecorder = cellClickManager.annotationTypeRecorder
#         x_annotationValue, x_annotationOptions = annotationTypeRecorder.returnTextAnnotation()
#         x_annotationValue, x_annotationOptions = returnDropdown(x_annotationOptions, last=["none"], value=x_annotationValue)
#         y_annotationValue, y_annotationOptions = returnDropdown(list(adata.obs.columns)+list(adata.var_names))
#     return x_annotationValue, x_annotationOptions, y_annotationValue, y_annotationOptions
#
#
# @callback(
#     Output(
#         {
#             'class': 'cellStat', 'group': 'graph',
#             'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
#         },
#         "value"
#     ),
#     Output(
#         {
#             'class': 'cellStat', 'group': 'graph',
#             'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
#         },
#         "options"
#     ),
#     Output(
#         {
#             'class': 'cellStat', 'group': 'graph',
#             'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': ALL,
#         },
#         "disabled"
#     ),
#     Output(
#         {
#             'class': 'cellStat', "group": "graph",
#             "type": "Graph", "index": MATCH,
#         },
#         "figure"
#     ),
#     Output(
#         {
#             'class': 'cellStat', 'group': 'graph',
#             'type': 'Download', 'index': MATCH, "function": "Download"
#         },
#         "data"
#     ),
#     inputs=dict(
#         refresh_annotationTypeRecorder=Input("refresh_annotationTypeRecorder", "data"),
#         refresh_clusterHistoryRecorder=Input("refresh_clusterHistoryRecorder", "data"),
#         dataID=State(
#             {
#                 'class': 'cellStat', 'group': 'graph',
#                 'type': "Label", 'function': "Data ID",
#                 'index': MATCH,
#             },
#             "children"
#         ),
#         defaultParameters=State(
#             {
#                 'class': 'cellStat', "group": "graph",
#                 "type": "Store", "index": MATCH
#             },
#             "data"
#         ),
#         plotParameters=(
#                 Input(
#                     {
#                         'class': 'cellStat', 'group': 'graph',
#                         'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': 0,
#                     },
#                     "value"
#                 ),
#                 Input(
#                     {
#                         'class': 'cellStat', 'group': 'graph',
#                         'type': 'Dropdown', 'index': MATCH, 'dropDownIndex': 1,
#                     },
#                     "value"
#                 ),
#                 Input("refresh_selectedCellsRecorder", "data"),
#                 Input("refresh_fixedCellsRecorder", "data"),
#                 State("fixSelection", "active"),
#         ),
#         exportClick=Input(
#             {
#                 'class': 'cellStat', 'group': 'graph',
#                 'type': 'Button', 'index': MATCH, "function": "Submit"
#             },
#             "n_clicks"
#         ),
#     ),
# )
# def returnCellStatGraph(
#     refresh_annotationTypeRecorder, refresh_clusterHistoryRecorder, dataID,
#     defaultParameters, plotParameters, exportClick
# ):
#     adata = cellClickManager.returnAdata()
#     adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
#     annotationTypeRecorder = cellClickManager.annotationTypeRecorder
#     clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
#     selectedCellsRecorder = cellClickManager.selectedCellsRecorder
#     fixedCellsRecorder = cellClickManager.fixedCellsRecorder
#     if cellClickManager.currentData != dataID:
#         return (
#             [dash.no_update, dash.no_update], [dash.no_update, dash.no_update], [True, True],
#             dash.no_update, dash.no_update
#         )
#     else:
#         (
#             x_AnnotationValue, y_AnnotationValue,
#             refresh_refresh_annotationTypeRecorder, refresh_fixedCellsRecorder,
#             active
#         ) = plotParameters
#
#         if x_AnnotationValue is None or y_AnnotationValue is None:
#             x_AnnotationValue, y_AnnotationValue = defaultParameters["x_Annotation"], defaultParameters["y_Annotation"]
#
#         cache, x_annotationOptions = annotationTypeRecorder.returnTextAnnotation()
#         x_annotationOptions = returnDropdownOptions(x_annotationOptions)
#         cache, y_annotationOptions = returnDropdown(list(adata.obs.columns) + list(adata.var_names))
#
#         selectedCells = selectedCellsRecorder.selectedCells
#         fixedCells = fixedCellsRecorder.fixedCells if active else None
#
#         import scanpy as sc
#         if x_AnnotationValue != y_AnnotationValue:
#             plotDf = sc.get.obs_df(adata, [x_AnnotationValue, y_AnnotationValue])
#         else:
#             plotDf = sc.get.obs_df(adata, [x_AnnotationValue])
#
#         if clusterHistoryRecorder:
#             refCol = clusterHistoryRecorder.refCol
#             if refCol and (x_AnnotationValue == refCol or y_AnnotationValue == refCol):
#                 plotDf[refCol] = clusterHistoryRecorder.returnAnnotation()
#
#         xType = annotationTypeRecorder.annotationTypeDict[x_AnnotationValue]
#         yType = annotationTypeRecorder.annotationTypeDict.get(y_AnnotationValue, "numeric")
#         switchDict = {
#             ("text", "numeric"): "Violin",
#             ("text", "text"): "Histogram",
#             # ("numeric", "numeric"): "Scatter", # not achieved
#         }
#         figure, exportDf = adataProcessor.returnCellStatFig(
#             plotDf, switchDict[(xType, yType)], "Selected", selectedCells, fixedCells
#         )
#
#         export = checkExport(dash.callback_context, index=0)
#         if export:
#             fileName = "Embedding.csv"
#             data = dcc.send_data_frame(exportDf.to_csv, fileName)
#         else:
#             data = dash.no_update
#
#         return (
#             [x_AnnotationValue, y_AnnotationValue], [x_annotationOptions, y_annotationOptions], [False, False],
#             figure, data
#         )
