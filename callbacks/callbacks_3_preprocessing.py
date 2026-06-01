#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_3_preprocessing.py
@time: 2024/7/25 14:32
"""
import dash

from callbacks.callbacks_2_dataSettings import *


@callback(
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'name': ALL, 'index': MATCH, "graphIndex": ALL,
        },
        'figure'
    ),
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
        },
        'min'
    ),
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
        },
        'max'
    ),
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
        },
        'value'
    ),
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
        },
        'tooltip'
    ),
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
        },
        'disabled'
    ),
    Output(
        {
            'class': 'QC', 'group': 'graph',
            'type': 'Input', 'index': MATCH, "inputIndex": ALL,
        },
        'value'
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        dataID=State(
            {
                'class': 'QC', 'group': 'graph',
                'type': "Label", 'function': "Data ID",
                'index': MATCH,
            },
            "children"
        ),
        defaultParameters=State(
            {
                "class": 'QC', "group": "graph",
                "type": "Store", "index": MATCH
            },
            "data"
        ),
        graphs=(
            Input(
                {
                    'class': 'QC', 'group': 'graph',
                    'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
                },
                'value'
            ),
            State(
                {
                    'class': 'QC', 'group': 'graph',
                    'type': 'RangeSlider', 'axis': 'y', 'name': ALL, 'index': MATCH, "graphIndex": ALL,
                },
                'id'
            ),
        ),
        exportClick=Input(
            {
                'class': 'QC', 'group': 'graph',
                'type': 'Button', 'index': MATCH, "function": "Submit"
            },
            "n_clicks"
        ),
    ),
)
def returnQCGraph(
    userSessionId,
    dataID,
    defaultParameters,
    graphs,
    exportClick,
):
    def initQCValues(qc_metric, attribute):
        switchDict = {
            "UMI Counts": [
                max(500, qc_metric['total_counts'].min()),
                min(50000, qc_metric['total_counts'].max())
            ],
            "Gene Counts": [
                max(200, qc_metric['n_genes_by_counts'].min()),
                min(6000, qc_metric['n_genes_by_counts'].max())
            ],
            "MT PCT":  [
                0, min(20, qc_metric['pct_counts_mt'].max())
            ] if qc_metric['pct_counts_mt'].max() > 1 else [
                0, min(0.2, qc_metric['pct_counts_mt'].max())
            ]
        }
        return  switchDict[attribute]

    def returnPlotParams(attribute):
        import math

        qc_metrics = adataProcessor.set_metrics()
        qc_metric = qc_metrics[0]

        digits = lambda x: math.pow(10, int(math.log(x, 10)))
        fun = lambda x: digits(x) * (int(x / digits(x))+1)
        mapDict = {
            "UMI Counts": [0, fun(qc_metric['total_counts'].max())],
            "Gene Counts": [0, fun(qc_metric['n_genes_by_counts'].max())],
            "MT PCT": [
                # -20 if qc_metric['pct_counts_mt'].max() > 1 else -0.2,
                # 120 if qc_metric['pct_counts_mt'].max() > 1 else 1.2,
                0 if qc_metric['pct_counts_mt'].max() > 1 else 0,
                100 if qc_metric['pct_counts_mt'].max() > 1 else 1,
            ]
        }

        for (minValue, maxValue), id in zip(graphs[0], graphs[1]):
            if id["name"] == attribute:
                if (minValue is None) or (maxValue is None):
                    # return mapDict[attribute] + initQCValues(qc_metric, attribute)
                    return mapDict[attribute] + mapDict[attribute]
                else:
                    return mapDict[attribute] + [minValue, maxValue]
            else:
                continue

    def returnGraph(attribute):
        sliderMin, sliderMax, minValue, maxValue = returnPlotParams(attribute)
        if dataID != userSessionId:
            sliderDisabled = True
        else:
            sliderDisabled = False
        figure, cells_filtered = adataProcessor.returnQCGraph(
            attribute, [sliderMin], [sliderMax], [minValue], [maxValue],
        )
        # figure = dash.no_update
        return figure, sliderMin, sliderMax, (minValue, maxValue), sliderDisabled, cells_filtered



    figures, sliderMins, sliderMaxs, plotValues, sliderDisableds, filteredCells = [], [], [], [], [], []
    attributes = defaultParameters["Attributes"]
    if dataID != cellClickManager.currentData:
        figures, sliderMins, sliderMaxs, plotValues = [[dash.no_update]*len(attributes)]*4
        sliderDisableds = [True]*len(attributes)
        filteredCells = [dash.no_update]*(len(attributes)+1)
    else:
        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
        cells_filtered_total = None

        for attribute in attributes:
            figure, sliderMin, sliderMax, plotValue, sliderDisabled, cells_filtered= returnGraph(attribute)
            figures.append(figure)
            sliderMins.append(sliderMin)
            sliderMaxs.append(sliderMax)
            plotValues.append(plotValue)
            sliderDisableds.append(sliderDisabled)
            filteredCells.append(cells_filtered.sum())
            if cells_filtered_total is None:
                cells_filtered_total = cells_filtered
            else:
                cells_filtered_total = cells_filtered_total | cells_filtered
        filteredCells.append(cells_filtered_total.sum())

        qc = checkExport(dash.callback_context, index=0)
        if qc:
            adataProcessor.filter_adata(cells_filtered_total)

    tooltips = [{"placement": "bottom", "always_visible": True}]*len(attributes)

    return figures, sliderMins, sliderMaxs, plotValues, tooltips, sliderDisableds, filteredCells


@callback(
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Normalization",
            "label_name": "Target Sum", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Normalization",
            "label_name": "Exclude Highly Expressed", "type": "Checklist"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Normalization",
            "label_name": "Log1P", "type": "Checklist"
        },
        "value"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        norParams=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Normalization",
                    "label_name": "Target Sum", "type": "Input"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Normalization",
                    "label_name": "Exclude Highly Expressed", "type": "Checklist"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Normalization",
                    "label_name": "Log1P", "type": "Checklist"
                },
                "value"
            ),
        ),
        submit=Input(
            {
                "card_name": "Preprocessing", "form_name": "Normalization",
                "label_name": "Submit", "type": "Button"
            },
            "n_clicks"
        ),
    )
)
def returnNormalizationForm(userSessionId, norParams, submit):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)

    if ctxIdStr is None or ctxIdStr == "":
        raise PreventUpdate
    elif ctxIdStr == "User Session ID":
        targetSumValue = 10000
        checkListValue1 = "Exclude Highly Expressed"
        checkListValue2 = "Log1P"
        return targetSumValue, checkListValue1, checkListValue2
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId["label_name"] == "Submit":
            targetSum, excludeHighlyExpressed, log1P = norParams
            normalizeKwargs = {
                "target_sum": targetSum,
                "exclude_highly_expressed": True if excludeHighlyExpressed else False,
            }
            adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
            adataProcessor.scDataPreprocessing(normalizeKwargs=normalizeKwargs, qc="Normalization")
            adataProcessor.scDataPreprocessing(log1P=log1P, qc="log1P")

            return dash.no_update, dash.no_update, dash.no_update
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))


@callback(
    Output(
        {
            "card_name": "Preprocessing", "form_name": "HVG Detection",
            "label_name": "Flavor", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "HVG Detection",
            "label_name": "Flavor", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "HVG Detection",
            "label_name": "Top Genes", "type": "Input"
        },
        "value"
    ),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        hvgParams=(
                State(
                    {
                        "card_name": "Preprocessing", "form_name": "HVG Detection",
                        "label_name": "Flavor", "type": "Dropdown"
                    },
                    "value"
                ),
                State(
                    {
                        "card_name": "Preprocessing", "form_name": "HVG Detection",
                        "label_name": "Top Genes", "type": "Input"
                    },
                    "value"
                ),
        ),
        submit=Input(
            {
                "card_name": "Preprocessing", "form_name": "HVG Detection",
                "label_name": "Submit", "type": "Button"
            },
            "n_clicks"
        ),
    )
)
def returnHVGDetectionForm(userSessionId, hvgParams, submit):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)

    if ctxIdStr is None or ctxIdStr == "":
        raise PreventUpdate
    elif ctxIdStr == "User Session ID":
        flavor = ["seurat", "cell_ranger", "seurat_v3", "seurat_v3_paper"]
        dropdownOptions = returnDropdownOptions(flavor)
        dropdownValue = "seurat"

        topGenes = 2000
        return dropdownValue, dropdownOptions, topGenes
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId["label_name"] == "Submit":
            flavor, n_top_genes = hvgParams
            hvgKwargs = {
                "n_top_genes": n_top_genes,
                "flavor": flavor,
            }
            adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
            adataProcessor.scDataPreprocessing(hvgKwargs=hvgKwargs, qc="HVG Detection")
            return dash.no_update, dash.no_update, dash.no_update
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))


@callback(
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Method", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Method", "type": "Dropdown"
        },
        "options"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "N PCs", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "N PCs", "type": ALL
        },
        "style"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "N Neighbors", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "N Neighbors", "type": ALL
        },
        "style"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Min Dist", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Min Dist", "type": ALL
        },
        "style"
    ),

    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Metric", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Metric", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Preprocessing", "form_name": "Dimension Reduction",
            "label_name": "Metric", "type": ALL
        },
        "style"
    ),
    inputs=dict(
        userSessionID=Input("User Session ID", "data"),
        methodValue=Input(
            {
                "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                "label_name": "Method", "type": "Dropdown"
            },
            "value"
        ),
        n_pcs=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "N PCs", "type": "Input"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "N PCs", "type": ALL
                },
                "style"
            ),
        ),
        n_nei=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "N Neighbors", "type": "Input"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "N Neighbors", "type": ALL
                },
                "style"
            ),
        ),
        min_dist=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "Min Dist", "type": "Input"
                },
                "value",
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "Min Dist", "type": ALL
                },
                "style",
            ),
        ),
        metric=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "Metric", "type": "Dropdown"
                },
                "value",
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                    "label_name": "Metric", "type": ALL
                },
                "style",
            ),
        ),
        submit=Input(
            {
                "card_name": "Preprocessing", "form_name": "Dimension Reduction",
                "label_name": "Submit", "type": "Button"
            },
            "n_clicks"
        ),
    ),
    # prevent_initial_call=True,
)
def returnDimensionReductionForm(
        userSessionID,
        methodValue, n_pcs, n_nei, min_dist, metric,
        submit
):

    def returnStyles(styles, display):
        styles = [{} if style is None else style for style in styles]
        for i in range(0, len(styles)):
            styles[i]["display"] = display
        return styles

    method = list(returnDropdown(["UMAP", "t-SNE", "PCA"], value=methodValue, sort=False))

    npcs = [int(n_pcs[0]) if n_pcs[0] else 50, returnStyles(n_pcs[1], "block")]
    n_neighbors = [
        int(n_nei[0]) if n_nei[0] else 15,
        returnStyles(n_nei[1], "block" if method[0] in ["UMAP"] else "none")
    ]
    min_dist = [
        float(min_dist[0]) if min_dist[0] else 0.5,
        returnStyles(min_dist[1], "block" if method[0] in ["UMAP"] else "none")
    ]

    metricOptions = [
        'cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan',
        'braycurtis', 'canberra', 'chebyshev', 'correlation', 'dice', 'hamming',
        'jaccard', 'kulsinski', 'mahalanobis', 'minkowski', 'rogerstanimoto', 'russellrao',
        'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'
    ]
    metric = [
        metric[0] if metric[0] else 'euclidean',
        returnDropdownOptions(metricOptions),
        returnStyles(metric[1], "block" if method[0] in ["UMAP", "t-SNE"] else "none")
    ]

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIdStr is None or ctxIdStr == "":
        raise PreventUpdate
    elif ctxIdStr == "User Session ID":
        return method + npcs + n_neighbors + min_dist + metric
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId["label_name"] == "Submit":
            PCAKwargs = {
                "n_components": npcs[0],
                "random_state": 4712,
            }

            neighborKwargs = {
                "n_neighbors": n_neighbors[0],
                "n_pcs": npcs[0],
                "metric": metric[0],
                "random_state": 4712,
            }

            umapKwargs = {
                "min_dist": min_dist[0],
                "random_state": 4712,
            }

            t_sneKwargs = {
                "n_pcs": npcs[0],
                "metric": metric[0],
                "random_state": 4712,
            }


            adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
            adataProcessor.scDataPreprocessing(
                qc="Dimension Reduction", dimRedMethod=method[0],
                PCAKwargs=PCAKwargs, neighborKwargs=neighborKwargs, umapKwargs=umapKwargs, t_sneKwargs=t_sneKwargs,

            )
            return method + npcs + n_neighbors + min_dist + metric
        elif ctxId["label_name"] == "Method":
            return method + npcs + n_neighbors + min_dist + metric
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))



@callback(
    Output("PreprocessingAlert", "children"),
    Output("PreprocessingAlert", "is_open"),
    inputs=dict(
        userSessionID=State("User Session ID", "data"),
        formSubmits=Input(
            {
                "card_name": "Preprocessing", "form_name": ALL,
                "label_name": "Submit", "type": "Button"
            },
            "n_clicks"
        ),
        QCSubmits=(
            State(
                {
                'class': 'QC', 'group': 'graph',
                'type': 'Button', 'index': ALL, "function": "Submit"
                },
                "id"
            ),
            Input(
                {
                'class': 'QC', 'group': 'graph',
                'type': 'Button', 'index': ALL, "function": "Submit"
                },
                "n_clicks"
            ),
        )
    ),
    prevent_initial_call=True,
)
def alertData(userSessionID, formSubmits, QCSubmits):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)

    preprocessingAlert = [None, False]
    if ctxIdStr == "":
        preprocessingAlert = [dash.no_update, False]
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId.get("form_name", False) == "QC":
            raise PreventUpdate
        elif ctxId.get("class", False) == "QC":
            ids, n_clicks = QCSubmits
            for id, n_click in zip(ids, n_clicks):
                if ctxId["index"] == id["index"] and n_click == 0:
                    raise PreventUpdate
        else:
            pass

        adataProcessor = cellClickManager.get(cellClickManager.currentData).adataProcessor
        while True:
            if adataProcessor.isPreprocess:
                if adataProcessor.isPreprocess == "Normalization": # followed by lop1P
                    continue
                preprocessingAlert = [
                    "{} has been done!".format(
                        adataProcessor.isPreprocess if adataProcessor.isPreprocess != "lop1P" else "Normalization"
                    ),
                    True
                ]
                adataProcessor.isPreprocess = None
                break
            else:
                time.sleep(1)
                continue

    return preprocessingAlert
