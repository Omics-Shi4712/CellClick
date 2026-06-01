#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: some tools/function for CellMarker
@version: 1.0.0
@file: utils.py
@time: 2023/10/17 22:01
"""
import numpy as np
import pandas as pd

import plotly.graph_objects as go

from dash import html

from settings import projectDir


# return component based document json, usually used for string-like description
def returnStringComponent(obj):
    componentDict = {
        "a": html.A
    }

    if isinstance(obj, str):
        return obj
    elif isinstance(obj, dict):
        return componentDict[obj["component"]](**obj.get("kwargs", {}))
    elif isinstance(obj, list):
        return [returnStringComponent(subObj) for subObj in obj]
    else:
        raise ValueError("Unexpect object type received: {}".format(type(obj)))


# define the data type of dash_table type
def table_type(df_column):
    # Note - this only works with Pandas >= 1.0.0

    # https://dash.plotly.com/datatable/filtering
    if isinstance(df_column.dtype, pd.DatetimeTZDtype):
        return 'datetime',
    elif (isinstance(df_column.dtype, pd.StringDtype) or
          isinstance(df_column.dtype, pd.BooleanDtype) or
          isinstance(df_column.dtype, pd.CategoricalDtype) or
          isinstance(df_column.dtype, pd.PeriodDtype)):
        return 'text'
    elif (isinstance(df_column.dtype, pd.SparseDtype) or
          isinstance(df_column.dtype, pd.IntervalDtype) or
          isinstance(df_column.dtype, pd.Int8Dtype) or
          isinstance(df_column.dtype, pd.Int16Dtype) or
          isinstance(df_column.dtype, pd.Int32Dtype) or
          isinstance(df_column.dtype, pd.Int64Dtype)):
        return 'numeric'
    else:
        if df_column.dtype is np.dtype('object'):
            return "text"
        else:
            return "numeric"


def splitIndex(targetIndex, refs, refName=["fixed", "selected"]):
    # split target index/list into four parts based on two ref series/list
    # in CellMarker, the len of refSeries was limited as 2 and sorted as [fixed cells, selected cells]
    assert len(refs) == 2, """the length of refs should be 2"""

    resultCol = pd.Series(index=targetIndex)

    # some situation, it may show the selected/fixed cells in a subset adata object
    if refs[0]:
        refs[0] = list(set(targetIndex) & set(refs[0]))
    refs[1] = list(set(targetIndex) & set(refs[1]))

    if refs[0] is None:
        refs[0] = []
        resultCol = resultCol.fillna("not {}".format(refName[1]))
    else:
        resultCol = resultCol.fillna("not-{}_not-{}".format(refName[0], refName[1]))

    resultCol[refs[0]] = refName[0]
    resultCol[refs[1]] = refName[1]

    if refs[0]:
        resultCol[list(set(refs[0]) & set(refs[1]))] = "{}_{}".format(refName[0], refName[1])

    return resultCol


def mappingColor(categories, colors):
    """
    mapping colors for categories
    :param categories: list of categories
    :param colors: list of colors
    :return:
    """
    copyNum = int(len(categories) / len(colors)) + 1
    colors = colors * copyNum

    colorDict = {}
    for key, value in zip(categories, colors):
        colorDict[key] = value

    return colorDict


def centerGraph(xLim, yLim, limRatio=0.55):
    # set the range of embedding plot
    xRange = xLim[1] - xLim[0]
    xCenter = (xLim[1] + xLim[0]) / 2
    yRange = yLim[1] - yLim[0]
    yCenter = (yLim[1] + yLim[0]) / 2

    if xRange > yRange:
        xMin, xMax = xCenter - limRatio * xRange, xCenter + limRatio * xRange
        yMin, yMax = yCenter - limRatio * xRange, yCenter + limRatio * xRange
    else:
        xMin, xMax = xCenter - limRatio * yRange, xCenter + limRatio * yRange
        yMin, yMax = yCenter - limRatio * yRange, yCenter + limRatio * yRange
    return xMin, xMax, yMin, yMax


def optFig(figure, border=False, cut_off_x=False, cutt_off_x_kwargs={}):
    """
    to optimize plotly figure object
    :param figure: an object of plotly
    :return:
    """

    figure.update_layout(
        font=dict(
            family="Arial",
            size=14,
        ),
        title=dict(
            font=dict(
                family="Arial Black",
                size=16,
            ),
        )
    )

    if cut_off_x:
        func = cutt_off_x_kwargs.get("func", lambda x: x[:20] + "..." if len(x) > 20 else x)
        tickvals = figure.layout.xaxis.tickvals
        figure.update_xaxes(
            tickvals=tickvals, ticktext=[func(text) for text in tickvals],
        )

    if border:
        figure.update_layout(
            shapes=[
                # Top border
                go.layout.Shape(
                    type="line",
                    x0=0, y0=1, x1=1, y1=1,
                    xref="paper", yref="paper",
                    line=dict(color="black", width=2)
                ),
                # Right border
                go.layout.Shape(
                    type="line",
                    x0=1, y0=0, x1=1, y1=1,
                    xref="paper", yref="paper",
                    line=dict(color="black", width=2)
                ),
                # bottom border
                go.layout.Shape(
                    type="line",
                    x0=0, y0=0, x1=1, y1=0,
                    xref="paper", yref="paper",
                    line=dict(color="black", width=2)
                ),
                # left border
                go.layout.Shape(
                    type="line",
                    x0=0, y0=0, x1=0, y1=1,
                    xref="paper", yref="paper",
                    line=dict(color="black", width=2)
                ),
            ]
        )

    return figure


def resortObsm(obsm):
    def resort(l, key):
        a = []
        b = []
        key = key.lower()
        for e in l:
            if key in e.lower():
                a.append(e)
            else:
                b.append(e)
        return a + b

    embeddings = list(obsm)
    embeddings = resort(embeddings, "pca")
    embeddings = resort(embeddings, "tsne")
    embeddings = resort(embeddings, "t-sne")
    embeddings = resort(embeddings, "umap")
    return embeddings


def returnMarkerSource(marker_ref):
    import os

    markerSources = []
    for sourcedDir in marker_ref:
        markerSources.append(os.path.basename(sourcedDir))
    return markerSources


def returnMarkerFile(sourceName, analysis="Cluster Analysis", species=None):
    import os

    sourceDir = os.path.join(projectDir, "marker_ref/{}".format(sourceName))
    if analysis == "Cluster Analysis":
        if sourceName == "Other":
            return [(file.split(".")[0], os.path.join(sourceDir, file)) for file in os.listdir(sourceDir)]
        else:
            return [
                (file.split(".")[0], os.path.join(sourceDir, "Cluster Analysis", file)) for file in os.listdir(os.path.join(sourceDir, "Cluster Analysis"))
            ]
    else:
        return [sourceName, os.path.join(sourceDir, "Gene Analysis/{}.GeneWeight.mat".format(species))]
