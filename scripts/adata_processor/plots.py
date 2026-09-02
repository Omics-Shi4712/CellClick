#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import plotly.graph_objects as go

from __settings_layout import pos_cmap_dash, myColors
from scripts.utils import mappingColor, optFig, splitIndex


def return_dot_color_and_size(
    adata,
    var_names,
    groupby,
    expression_cutoff=0.0,
    mean_only_expressed=False,
    standard_scale=None,
):
    from scanpy.plotting._anndata import _prepare_dataframe

    categories, obs_tidy = _prepare_dataframe(adata, var_names, groupby)

    obs_bool = obs_tidy > expression_cutoff
    dot_size_df = obs_bool.groupby(level=0).sum() / obs_bool.groupby(level=0).count()

    mean_only_expressed = True
    if mean_only_expressed:
        dot_color_df = obs_tidy.mask(~obs_bool).groupby(level=0).mean().fillna(0)
    else:
        dot_color_df = obs_tidy.groupby(level=0).mean()

    if standard_scale == "group":
        dot_color_df = dot_color_df.sub(dot_color_df.min(1), axis=0)
        dot_color_df = dot_color_df.div(dot_color_df.max(1), axis=0).fillna(0)
    elif standard_scale == "var":
        dot_color_df -= dot_color_df.min(0)
        dot_color_df = (dot_color_df / dot_color_df.max(0)).fillna(0)

    return dot_color_df, dot_size_df


def return_dotplot(dot_color_df, dot_size_df, groupby, groupOrder):
    dot_size_df = dot_size_df.copy()
    dot_color_df = dot_color_df.copy()

    dot_size_df[groupby] = dot_size_df.index
    dot_size_melt = dot_size_df.melt(id_vars=[groupby])

    dot_color_df[groupby] = dot_color_df.index
    dot_color_melt = dot_color_df.melt(id_vars=[groupby])

    data = go.Scatter(
        x=dot_color_melt["variable"],
        y=dot_color_melt[groupby],
        mode="markers",
        marker=dict(
            size=dot_size_melt["value"] * 25,
            color=dot_color_melt["value"],
            showscale=True,
            opacity=1,
            colorscale=pos_cmap_dash,
        ),
        text=dot_size_melt["value"] * 100,
        hovertemplate="<b>Gene: %{x}</b><br>"
        + "Group: %{y}<br>"
        + "Average expression: %{marker.color:,.2f}<br>"
        + "Fraction: %{text:,.2f}%"
        + "<extra></extra>",
    )

    fig = go.Figure(data=data)
    fig.update_xaxes(
        type="category",
        tickangle=-90,
        ticklen=5,
        tickcolor="white",
        ticks="outside",
        tickmode="array",
        tickvals=dot_color_melt["variable"].unique(),
        ticktext=[f"<i>{gene}</i>" for gene in dot_color_melt["variable"].unique()],
    )
    fig.update_yaxes(
        type="category",
        title_text="",
        ticklen=5,
        tickcolor="white",
        ticks="outside",
        categoryorder="array",
        categoryarray=list(groupOrder),
    )
    fig.update_layout(
        autosize=True,
        plot_bgcolor="rgba(0, 0, 0, 0)",
    )

    plotDf = pd.concat([dot_size_melt[[groupby, "variable", "value"]], dot_color_melt[["value"]]], axis=1)
    plotDf.columns = ["Group", "Gene", "Fraction(%)", "Average Expression"]
    plotDf["Fraction(%)"] = plotDf["Fraction(%)"] * 100

    fig = optFig(fig, border=True)
    return fig, plotDf


def return_heatmap_plot(dot_color_df, var_groups, groupby):
    if var_groups is None:
        data = go.Heatmap(
            x=dot_color_df.columns,
            y=dot_color_df.index,
            z=dot_color_df,
            colorscale=pos_cmap_dash,
        )
    else:
        data = go.Heatmap(
            x=[var_groups, dot_color_df.columns],
            y=dot_color_df.index,
            z=dot_color_df,
            colorscale=pos_cmap_dash,
        )
    fig = go.Figure(data=data)
    fig.update_yaxes(title_text=groupby)
    fig.update_layout(xaxis=dict(tickangle=-90))
    fig.update_layout(autosize=True)

    fig = optFig(fig)
    return fig, dot_color_df


def return_cell_stat_fig(plotDf, histType, colorBy, selectedCells, fixedCells=None):
    plotDf = plotDf.copy()
    plotDf["CellClick_Category"] = splitIndex(plotDf.index, [fixedCells, selectedCells])
    plotDf["CellClick_CellIDs"] = plotDf.index

    plotX = plotDf.columns[0]
    plotY = plotDf.columns[1]
    hueCol = "CellClick_Category"

    if histType == "Histogram":
        x_axis = sorted(plotDf[plotX].unique())
        y_axis = sorted(plotDf[plotY].unique())
        hues = sorted(plotDf[hueCol].unique())

        colors = mappingColor(y_axis, myColors)
        selectedMapping = {
            "no-highlight": ["not-fixed_not-selected", "not selected"],
            "highlight": ["", "fixed", "fixed_selected", "selected"],
        }

        if len(hues) == 1:
            marker = {
                "no-highlight": dict(opacity=1),
                "highlight": dict(opacity=1),
            }
        else:
            marker = {
                "no-highlight": dict(opacity=0.25),
                "highlight": dict(opacity=1),
            }

        figure = go.Figure(
            layout=go.Layout(
                barmode="relative",
                yaxis_showticklabels=False,
                yaxis_showgrid=False,
                yaxis2=go.layout.YAxis(
                    visible=False,
                    matches="y",
                    overlaying="y",
                    anchor="x",
                ),
                legend=dict(
                    font=dict(size=10),
                    itemsizing="constant",
                    x=1.05,
                    y=1,
                    xanchor="left",
                    yanchor="top",
                ),
                hovermode="x",
            )
        )
        legend = []
        for i, trace_type in enumerate(selectedMapping):
            selectDf = plotDf.loc[plotDf[hueCol].isin(selectedMapping[trace_type])]
            for col in y_axis:
                colDf = selectDf.loc[selectDf[plotY] == col]
                barDf = colDf.value_counts(plotX)[x_axis]
                barDf = barDf[barDf > 0]
                if len(barDf) == 0:
                    continue

                figure.add_bar(
                    x=barDf.index,
                    y=barDf,
                    yaxis=f"y{i + 1}",
                    offsetgroup=str(i),
                    offset=(i - 1) * 1 / 3,
                    width=1 / 3,
                    legendgroup=col,
                    legendgrouptitle_text="",
                    name=col,
                    showlegend=False if col in legend else True,
                    marker_color=colors[col],
                    marker_line=dict(width=2, color="#333"),
                    hovertemplate="%{y}<extra></extra>",
                    marker=marker[trace_type],
                    customdata=[
                        "{}@4712@{}@4712{}@4712@{}".format(plotX, plotY, trace_type, col)
                    ]
                    * len(barDf),
                )
                if col not in legend:
                    legend.append(col)
        figure.update_xaxes(categoryorder="array", categoryarray=x_axis)
    else:
        category_orders = {
            hueCol: sorted(plotDf[hueCol].unique())
        }
        figure = go.Figure()
        for name in category_orders[hueCol]:
            figure.add_trace(
                go.Box(
                    x=plotDf.loc[plotDf[hueCol] == name, plotX],
                    y=plotDf.loc[plotDf[hueCol] == name, plotY],
                    name=name,
                )
            )
        figure.update_layout(
            yaxis=dict(title=dict(text=plotY)),
        )

    figure.update_layout(
        dragmode="select",
    )
    figure = optFig(figure)
    return figure, plotDf


def return_sankey_fig(historyDf):
    def cluster_record_level_check(clusterDf, columns):
        checkSeries = clusterDf.T.apply(
            lambda row: not (row[columns[0]] == row[columns[1]] or row[columns[1]] == row[columns[2]])
        )
        return False if checkSeries.sum() == 0 else True

    plotCols = list(historyDf.columns)
    for colIndex in range(1, len(historyDf.columns) - 1):
        clusterDf = historyDf[historyDf.columns[colIndex - 1: colIndex + 2]]
        if cluster_record_level_check(clusterDf, clusterDf.columns):
            continue
        plotCols.remove(historyDf.columns[colIndex])

    historyDf = historyDf[plotCols]
    sourceList = []
    targetList = []
    valueList = []
    label = [
        list(historyDf[historyDf.columns[0]].value_counts(ascending=False).index)
    ]
    labelCount = [len(label[0])]
    for i in range(0, len(historyDf.columns) - 1):
        subCols = historyDf.columns[i: i + 2]
        subDataFrame = historyDf[subCols]
        sourceTarget = subDataFrame.value_counts()

        sourceRef = label[i]
        sourceOffset = labelCount[i] - len(sourceRef)

        targetRef = list(historyDf[subCols[1]].value_counts(ascending=False).index)
        targetOffset = labelCount[i]

        for sourceTargetIndex, sourceTargetValue in zip(sourceTarget.index, sourceTarget):
            source = sourceTargetIndex[0]
            sourceIndex = sourceOffset + sourceRef.index(source)
            sourceList.append(sourceIndex)

            target = sourceTargetIndex[1]
            targetIndex = targetOffset + targetRef.index(target)
            targetList.append(targetIndex)

            valueList.append(sourceTargetValue)

        label += [targetRef]
        labelCount.append(labelCount[i] + len(targetRef))

    labelList = []
    for subLabelList in label:
        labelList += subLabelList

    fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labelList,
                    color="blue",
                ),
                link=dict(
                    source=sourceList,
                    target=targetList,
                    value=valueList,
                ),
            )
        ]
    )
    fig = optFig(fig)
    return fig
