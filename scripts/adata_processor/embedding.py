#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scanpy as sc

from __settings_layout import myColors
from scripts.utils import centerGraph, mappingColor, optFig, splitIndex


def get_marker_scatter(processor, use_rep, marker_gene):
    adata = processor.adata

    if use_rep != "spatial":
        df_embedding = pd.DataFrame(adata.obsm[use_rep][:, :2])
    else:
        scale_factor = processor.spatialAttr["scale_factor"]
        df_embedding = pd.DataFrame(np.multiply(adata.obsm["spatial"], scale_factor)[:, :2])
    df_embedding.index = adata.obs_names
    df_embedding.columns = ["DIM1", "DIM2"]
    df_embedding["Expression"] = sc.get.obs_df(adata, marker_gene)

    df_embedding.index = adata.obs_names
    df_embedding = df_embedding.sort_values(by="Expression")

    if use_rep != "spatial":
        fig = go.Figure()
    else:
        from scripts._utils import _check_img

        img, img_key = _check_img(
            spatial_data=processor.adata.uns["spatial"][processor.spatialAttr["library_id"]],
            img=None,
            img_key=processor.spatialAttr["img_key"],
        )
        fig = px.imshow(img)

    colorScale = plt.get_cmap("myCmpGra")
    colorScale = [colorScale(i) for i in range(colorScale.N)]
    colorScale = [(r, g, b) for r, g, b, _ in colorScale]
    colorScale = [
        [i / (len(colorScale) - 1), f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"]
        for i, (r, g, b) in enumerate(colorScale)
    ]

    fig.add_trace(
        go.Scatter(
            mode="markers",
            x=df_embedding["DIM1"],
            y=df_embedding["DIM2"],
            marker=dict(
                colorscale=colorScale if use_rep != "spatial" else "viridis",
                size=6000 / len(df_embedding) if use_rep != "spatial" else 4,
                showscale=True,
            ),
            marker_color=df_embedding["Expression"],
        ),
    )

    xMin, xMax, yMin, yMax = centerGraph(
        (df_embedding["DIM1"].min(), df_embedding["DIM1"].max()),
        (df_embedding["DIM2"].min(), df_embedding["DIM2"].max()),
    )
    use_rep = use_rep.upper()
    fig.update_layout(
        xaxis=dict(
            range=[xMin, xMax],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            ticks="",
            title="{}_1".format(use_rep),
        ),
        yaxis=dict(
            range=[yMin, yMax] if use_rep != "spatial".upper() else [yMax, yMin],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            ticks="",
            title="{}_2".format(use_rep),
        ),
        legend=dict(
            font=dict(size=10),
            itemsizing="constant",
        ),
        template="simple_white",
        margin=dict(
            l=50,
            r=50,
        ),
        title=dict(
            text=f"<i>{marker_gene}</i>",
            x=0.5,
        ),
        dragmode="lasso",
        hovermode="closest",
    )

    fig = optFig(fig, border=True if use_rep != "spatial".upper() else False)
    return fig, df_embedding


def get_fig_by_embedding(processor, use_rep, groupby, selectedCells=None, fixedCells=None, refAnnotation=None):
    adata = processor.adata
    if selectedCells is None:
        selectedCells = adata.obs_names

    if use_rep == "spatial" and "spatial" in adata.uns:
        scale_factor = processor.spatialAttr["scale_factor"]
        df_embedding = pd.DataFrame(np.multiply(adata.obsm["spatial"], scale_factor)[:, :2])
    else:
        df_embedding = pd.DataFrame(adata.obsm[use_rep][:, :2])
    df_embedding.index = adata.obs_names
    df_embedding.columns = ["DIM1", "DIM2"]
    df_embedding["customdata"] = adata.obs_names
    groupby = processor._normalize_groupby(groupby)
    if groupby == "none":
        df_embedding[groupby] = [""] * len(df_embedding)
    else:
        df_embedding[groupby] = adata.obs[groupby] if not isinstance(refAnnotation, pd.Series) else refAnnotation
    groupOrder = df_embedding[groupby].value_counts(ascending=False).index
    colorsDict = mappingColor(groupOrder, myColors)

    size = 6000 / len(df_embedding)
    embeddingDictSwitchDict = {
        "fixed": {
            "name": "fixed",
            "opacity": 1.0,
            "marker": dict(size=size, symbol="circle-open-dot"),
            "modifyName": "\n(fixed)",
        },
        "selected": {
            "name": "selected",
            "opacity": 1.0,
            "marker": dict(size=size, symbol="circle"),
            "modifyName": "\n(selected)",
        },
        "fixed_selected": {
            "name": "fixed_selected",
            "opacity": 1.0,
            "marker": dict(size=size, symbol="circle-dot"),
            "modifyName": "\n(fixed_selected)",
        },
        "not-fixed_not-selected": {
            "name": "not-fixed_not-selected",
            "opacity": 0.10,
            "marker": dict(size=size, symbol="circle-open"),
            "modifyName": "",
        },
        "not selected": {
            "name": "not selected",
            "opacity": 0.10,
            "marker": dict(size=size, symbol="circle-open"),
            "modifyName": "",
        },
        "": {
            "name": "",
            "opacity": 1.0,
            "marker": dict(size=size, symbol="circle"),
            "modifyName": "",
        },
    }

    refCol = splitIndex(df_embedding.index, [fixedCells, selectedCells])
    refValues = sorted(refCol.unique())
    embeddingList = []
    for refValue in refValues:
        df_selected = df_embedding.loc[refCol == refValue]
        embeddingDict = (
            embeddingDictSwitchDict[""] if len(refValues) == 1 else embeddingDictSwitchDict[refValue]
        ).copy()
        embeddingDict["embeddingDf"] = df_selected
        embeddingList.append(embeddingDict)

    if use_rep != "spatial":
        fig = go.Figure()
    else:
        from scripts._utils import _check_img

        img, img_key = _check_img(
            spatial_data=processor.adata.uns["spatial"][processor.spatialAttr["library_id"]],
            img=None,
            img_key=processor.spatialAttr["img_key"],
        )
        fig = px.imshow(img)

    for embeddingDict in embeddingList:
        embeddingDf = embeddingDict["embeddingDf"]
        group_info = embeddingDf[groupby].values

        for group in groupOrder:
            idx = group_info == group
            df_i = embeddingDf.loc[idx]

            marker = dict(embeddingDict["marker"])
            if use_rep == "spatial":
                marker["size"] = 4

            colors = [colorsDict[group]] * len(df_i)
            marker["color"] = colors
            fig.add_trace(
                go.Scatter(
                    mode="markers",
                    x=df_i["DIM1"],
                    y=df_i["DIM2"],
                    customdata=df_i["customdata"],
                    opacity=embeddingDict["opacity"],
                    marker=marker,
                    name=str(group) + embeddingDict["modifyName"],
                ),
            )

    xMin, xMax, yMin, yMax = centerGraph(
        (df_embedding["DIM1"].min(), df_embedding["DIM1"].max()),
        (df_embedding["DIM2"].min(), df_embedding["DIM2"].max()),
    )

    if use_rep.startswith("X_"):
        use_rep = re.sub("X_", "", use_rep)
    use_rep = use_rep.upper()

    fig.update_layout(
        xaxis=dict(
            range=[xMin, xMax],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            ticks="",
            title="{}_1".format(use_rep),
        ),
        yaxis=dict(
            range=[yMin, yMax] if use_rep != "spatial".upper() else [yMax, yMin],
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            ticks="",
            title="{}_2".format(use_rep),
        ),
        legend=dict(
            font=dict(size=10),
            itemsizing="constant",
        ),
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(
            l=50,
            r=50,
        ),
        dragmode="lasso",
        hovermode="closest",
    )

    plotDf = embeddingDf[["DIM1", "DIM2", groupby]]
    plotDf["selected"] = refCol

    fig = optFig(fig, border=True if use_rep != "spatial".upper() else False)
    return fig, plotDf
