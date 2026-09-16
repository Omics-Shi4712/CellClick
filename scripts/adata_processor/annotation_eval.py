#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import cosg as cosg
import plotly.graph_objects as go
import scanpy as sc

from scripts.adata_processor.marker_analysis import _as_list, compute_cell_scores
from scripts.utils import mappingColor, optFig


def _safe_copy_dict(value):
    return {} if value is None else dict(value)


def _ordered_intersection(left, right):
    right_set = set(right)
    return [item for item in left if item in right_set]


def _benjamini_hochberg(p_values):
    """Adjust a set of p-values while controlling the false discovery rate."""
    p_values = np.asarray(p_values, dtype=float)
    if len(p_values) == 0:
        return p_values

    clean_p_values = np.where(np.isfinite(p_values), p_values, 1.0)
    order = np.argsort(clean_p_values)
    q_values = np.empty_like(clean_p_values)
    running_minimum = 1.0

    for rank in range(len(clean_p_values), 0, -1):
        index = order[rank - 1]
        adjusted_value = clean_p_values[index] * len(clean_p_values) / rank
        running_minimum = min(running_minimum, adjusted_value)
        q_values[index] = min(running_minimum, 1.0)

    return q_values


def _build_gene_frequency_series(geneWeight_full):
    if geneWeight_full is None or len(geneWeight_full) == 0:
        return pd.Series(dtype=float)
    return (geneWeight_full > 0).mean(axis=0).astype(float)


def _build_frequency_bins(gene_frequency, bin_edges=None):
    bin_edges = bin_edges or [0.0, 0.05, 0.10, 0.20, 0.40, 1.0]
    if len(gene_frequency) == 0:
        return pd.Series(dtype="Int64"), pd.Index([])
    labels = list(range(len(bin_edges) - 1))
    return pd.cut(
        gene_frequency,
        bins=bin_edges,
        labels=labels,
        include_lowest=True,
        duplicates="drop",
    ), pd.Index(bin_edges)


def _calc_reference_scores_from_marker_series(markerSeries, geneWeight_full):
    if markerSeries is None or len(markerSeries) == 0:
        return pd.Series(dtype=float), pd.DataFrame()

    common_columns = _ordered_intersection(geneWeight_full.columns, markerSeries.index)
    geneWeight = geneWeight_full[common_columns]
    if len(geneWeight.columns) == 0:
        return pd.Series(dtype=float), geneWeight

    marker_scores = markerSeries[geneWeight.columns]
    marker_score_sum = marker_scores.sum()
    if marker_score_sum <= 0:
        return pd.Series(dtype=float), geneWeight

    scores = np.multiply(
        geneWeight.values.dot(marker_scores > 0),
        (geneWeight > 0).values.dot(marker_scores / marker_score_sum),
    )
    scores = pd.Series(scores, index=geneWeight.index)
    return scores.sort_values(ascending=False), geneWeight


def _sample_matched_background_genes(markerSeries, geneFrequency, geneFrequencyBins, rng):
    target_size = len(markerSeries)
    if target_size == 0 or len(geneFrequency) == 0:
        return []

    sampled = []
    used = set()
    marker_bins = geneFrequencyBins.reindex(markerSeries.index).dropna()
    target_counts = marker_bins.value_counts().sort_index()

    for bin_id, count in target_counts.items():
        pool = geneFrequencyBins.index[geneFrequencyBins == bin_id].tolist()
        pool = [gene for gene in pool if gene not in used]
        if len(pool) == 0:
            continue
        take = min(int(count), len(pool))
        if take <= 0:
            continue
        chosen = rng.choice(pool, size=take, replace=False).tolist()
        sampled.extend(chosen)
        used.update(chosen)

    if len(sampled) < target_size:
        remaining_pool = [gene for gene in geneFrequency.index if gene not in used]
        remaining = target_size - len(sampled)
        if len(remaining_pool) > 0 and remaining > 0:
            take = min(remaining, len(remaining_pool))
            chosen = rng.choice(remaining_pool, size=take, replace=False).tolist()
            sampled.extend(chosen)
            used.update(chosen)

    if len(sampled) > target_size:
        sampled = sampled[:target_size]

    return sampled


def _build_null_summary(observed_scores, null_scores, candidate_labels):
    observed_values = observed_scores.reindex(candidate_labels).fillna(0.0).values
    if null_scores.size == 0:
        p_values = np.ones(len(candidate_labels), dtype=float)
    else:
        p_values = (1.0 + (null_scores >= observed_values).sum(axis=0)) / (null_scores.shape[0] + 1.0)
    q_values = _benjamini_hochberg(p_values)

    return pd.DataFrame(
        {
            "candidate_reference_cell_type": candidate_labels,
            "observed_score": observed_values,
            "p_value": p_values,
            "q_value": q_values,
        }
    )


def MarkerGeneScores_cal(
    processor,
    cellIDs,
    cellCluster,
    annotationSeries,
    marker_ref_path,
    markerGeneUsed,
    showNum=10,
    cosgParams=None,
    return_details=False,
    n_permutations=500,
    random_state=0,
    frequency_bin_edges=None,
):
    adata = processor.adata
    cosgParams = _safe_copy_dict(cosgParams) or dict(mu=1, remove_lowly_expressed=True)
    if cellCluster not in annotationSeries.values:
        annotationSeries = annotationSeries.cat.add_categories(cellCluster)
    adata.obs["group_by"] = annotationSeries
    adata.obs.loc[cellIDs, "group_by"] = cellCluster

    cosgParams["n_genes_user"] = markerGeneUsed
    cosg.cosg(
        adata,
        groupby="group_by",
        key_added="cosg",
        reference="rest",
        **cosgParams
    )
    markerSeries = pd.Series(
        adata.uns["cosg"]["scores"][cellCluster],
        index=adata.uns["cosg"]["names"][cellCluster],
    )

    geneWeight_full = processor._load_marker_weight(marker_ref_path)
    scores, geneWeight = _calc_reference_scores_from_marker_series(markerSeries, geneWeight_full)
    background_info = {
        "n_permutations": int(n_permutations),
        "random_state": int(random_state),
        "frequency_bin_edges": list(frequency_bin_edges or [0.0, 0.05, 0.10, 0.20, 0.40, 1.0]),
        "sample_size": int(len(markerSeries)),
        "sampling_mode": "matched_marker_set_permutation",
    }

    if len(geneWeight.columns) == 0:
        return {
            "scores": pd.Series(dtype=float),
            "markerSeries": markerSeries,
            "geneWeight": geneWeight,
            "geneWeightFull": geneWeight_full,
            "score_details": pd.DataFrame(),
            "top_candidate_summary": {},
            "background": background_info,
        }

    scores = scores.sort_values(ascending=False)
    top_scores = scores.head(showNum)

    if not return_details:
        if len(top_scores) > 0:
            top_label = str(top_scores.index[0])
            top_candidate_summary = {
                "candidate_reference_cell_type": top_label,
                "observed_score": float(top_scores.iloc[0]),
                "rank": 1,
            }
        else:
            top_candidate_summary = {}
        return {
            "scores": top_scores,
            "markerSeries": markerSeries,
            "geneWeight": geneWeight,
            "geneWeightFull": geneWeight_full,
            "score_details": pd.DataFrame(),
            "top_candidate_summary": top_candidate_summary,
            "background": background_info,
        }

    geneFrequency = _build_gene_frequency_series(geneWeight_full)
    geneFrequencyBins, bin_edges = _build_frequency_bins(geneFrequency, bin_edges=frequency_bin_edges)
    rng = np.random.default_rng(random_state)
    null_matrix = []
    candidate_labels = list(top_scores.index)
    marker_values = markerSeries.sort_values(ascending=False).values
    if len(marker_values) == 0:
        marker_values = markerSeries.values

    for _ in range(int(n_permutations)):
        background_genes = _sample_matched_background_genes(markerSeries, geneFrequency, geneFrequencyBins, rng)
        if len(background_genes) == 0:
            continue

        sampled_values = marker_values[:len(background_genes)]
        if len(sampled_values) < len(background_genes):
            sampled_values = np.resize(sampled_values, len(background_genes))
        background_scores = pd.Series(
            rng.permutation(sampled_values),
            index=background_genes,
        )
        perm_scores, _ = _calc_reference_scores_from_marker_series(background_scores, geneWeight_full)
        null_matrix.append(perm_scores.reindex(candidate_labels).fillna(0.0).values)

    null_matrix = np.asarray(null_matrix, dtype=float) if len(null_matrix) > 0 else np.empty((0, len(candidate_labels)))
    score_details = _build_null_summary(top_scores, null_matrix, candidate_labels)
    score_details.insert(1, "rank", np.arange(1, len(score_details) + 1))
    score_details = score_details.set_index("candidate_reference_cell_type", drop=False)

    overlap_num = []
    full_ref_gene_count = []
    used_ref_gene_count = []
    for candidate in candidate_labels:
        if candidate in geneWeight_full.index:
            ref_gene_mask_full = geneWeight_full.loc[candidate] > 0
            full_ref_gene_count.append(int(ref_gene_mask_full.sum()))
            overlap_num.append(int(ref_gene_mask_full.reindex(markerSeries.index).fillna(False).sum()))
        else:
            full_ref_gene_count.append(0)
            overlap_num.append(0)
        used_ref_gene_count.append(int((geneWeight.loc[candidate] > 0).sum()) if candidate in geneWeight.index else 0)

    score_details["overlap_num"] = overlap_num
    score_details["full_ref_gene_count"] = full_ref_gene_count
    score_details["used_ref_gene_count"] = used_ref_gene_count
    score_details["marker_gene_count"] = int(len(markerSeries))

    top_candidate_summary = score_details.iloc[0].to_dict() if len(score_details) > 0 else {}

    return {
        "scores": top_scores,
        "markerSeries": markerSeries,
        "geneWeight": geneWeight,
        "geneWeightFull": geneWeight_full,
        "score_details": score_details,
        "top_candidate_summary": top_candidate_summary,
        "background": {
            "n_permutations": int(n_permutations),
            "random_state": int(random_state),
            "frequency_bin_edges": list(bin_edges),
            "sample_size": int(len(markerSeries)),
            "sampling_mode": "matched_marker_set_permutation",
        },
    }


def build_marker_gene_score_plot(
    processor,
    cellIDs,
    cellCluster,
    annotationSeries,
    marker_ref_path,
    markerGeneUsed,
    showNum=10,
    cosgParams=None,
):
    marker_gene_scores = MarkerGeneScores_cal(
        processor,
        cellIDs,
        cellCluster,
        annotationSeries,
        marker_ref_path,
        markerGeneUsed,
        showNum=showNum,
        cosgParams=cosgParams,
    )
    scores = marker_gene_scores["scores"]
    markerSeries = marker_gene_scores["markerSeries"]
    geneWeight = marker_gene_scores["geneWeight"]
    geneWeight_full = marker_gene_scores["geneWeightFull"]
    if len(geneWeight.columns) == 0 or len(scores) == 0:
        return go.Figure(), pd.DataFrame(columns=["tissue", "cell type", "scores", "index", "color"])

    plotDf = pd.DataFrame(
        [
            [source.split("_")[0] for source in scores.index],
            [source.split("_")[1] for source in scores.index],
            list(scores),
        ],
        index=["tissue", "cell type", "scores"],
    ).T
    plotDf["index"] = scores.index

    local_colors = [
        "#FF0000", "#00FF00",
        "#00FFFF", "#FF00FF",
        "#FFA500",
        "#008080", "#FFC0CB",
        "#A52A2A", "#808000", "#FF7F50", "#000080", "#40E0D0",
        "#FFD700", "#F5F5DC", "#D2B48C", "#FA8072", "#87CEEB",
    ]
    colorsDict = mappingColor(plotDf["tissue"].unique(), local_colors)
    plotDf["color"] = plotDf["tissue"].apply(lambda x: colorsDict[x])
    plotDf = plotDf.iloc[::-1]

    figure = go.Figure()
    checkDf = plotDf.drop_duplicates("tissue", keep="last")
    annotations = []
    for index in plotDf.index:
        subPlotDf = plotDf.loc[[index]]
        tissue = plotDf.loc[index, "tissue"]
        figure.add_trace(
            go.Bar(
                x=subPlotDf["scores"],
                y=subPlotDf["index"],
                orientation="h",
                marker=dict(color=subPlotDf["color"]),
                hovertext=(
                    "tissue: " + subPlotDf["tissue"]
                    + "<br>cell type: " + subPlotDf["cell type"]
                    + "<br>scores: " + subPlotDf["scores"].astype(str)
                ),
                hoverinfo="text",
                name=tissue,
                showlegend=True if index in checkDf.index else False,
            ),
        )
        annotations.append(
            dict(
                x=0.01 * (plotDf["scores"].max()),
                y=subPlotDf["index"].values[0],
                text=subPlotDf["cell type"].values[0],
                font=dict(size=12),
                xanchor="left",
                showarrow=False,
            )
        )
    for annotation in annotations:
        figure.add_annotation(annotation)

    figure.update_layout(
        title=dict(
            text=cellCluster,
            x=0.5,
            xanchor="center",
        ),
        yaxis=dict(
            tickvals=[""] * len(plotDf),
            title="",
        ),
        xaxis=dict(
            title="Marker Gene Score",
        ),
        legend=dict(
            font=dict(size=10),
            itemsizing="constant",
            traceorder="reversed",
        ),
    )
    figure = optFig(figure)

    overlapDf = []
    for markerSource in scores.index:
        overlapRefGenes = geneWeight.columns[geneWeight.loc[markerSource] > 0]
        if markerSource in geneWeight_full.index:
            refGenes = geneWeight_full.columns[geneWeight_full.loc[markerSource] > 0]
        else:
            refGenes = overlapRefGenes
        markerGenes = list(markerSeries.index)

        def sort_genes(genes, marker_source):
            geneScores = pd.Series(
                np.multiply(geneWeight.loc[marker_source], markerSeries[geneWeight.columns]),
                index=geneWeight.columns,
            )
            geneSort = list(geneScores.sort_values(ascending=False).index)

            cosgSort = []
            markerSort = []
            for gene in genes:
                if gene in geneSort:
                    markerSort.append(gene)
                else:
                    cosgSort.append(gene)

            cosgSort = sorted(cosgSort, key=lambda x: list(markerSeries.index).index(x))
            markerSort = sorted(markerSort, key=lambda x: geneSort.index(x))
            return markerSort + cosgSort

        def sort_ref_genes(genes, marker_source):
            if marker_source not in geneWeight_full.index:
                return sorted(genes)
            geneScores = geneWeight_full.loc[marker_source, list(genes)]
            return list(geneScores.sort_values(ascending=False).index)

        overlapGenes = list(set(markerGenes) & set(overlapRefGenes))
        cosgGenes = list(set(markerGenes) - set(overlapRefGenes))
        overlapDf.append(
            [
                markerSource,
                ", ".join(sort_genes(markerGenes, markerSource)),
                ", ".join(sort_ref_genes(refGenes, markerSource)),
                scores[markerSource],
                len(overlapGenes),
                ", ".join(sort_genes(overlapGenes, markerSource)),
                ", ".join(sort_genes(cosgGenes, markerSource)),
            ]
        )

    overlapDf = pd.DataFrame(
        overlapDf,
        columns=[
            "refCellType", "markerGenes", "refGenes", "score",
            "overlapNum", "Overlap Genes", "COSG Unique Genes",
        ],
    )
    overlapDf.index = overlapDf["refCellType"]
    return figure, overlapDf


def return_color_dot_plot(processor, cellCluster, groupBySeries, overlapDf, cellType):
    adata = processor.adata
    adata.obs["group_by"] = groupBySeries
    markerGenes = overlapDf.loc[cellType, "markerGenes"].split(", ")

    overlapGenes = overlapDf.loc[cellType, "Overlap Genes"].split(", ")
    showGenes = markerGenes
    geneSort = markerGenes

    if len(showGenes) == 0:
        return go.Figure(), pd.DataFrame()

    figure, plotDf = processor.get_dot_plot(var_names=geneSort, groupby="group_by")

    annotations = []
    for gene, index in zip(geneSort, range(0, len(geneSort))):
        if gene in overlapGenes:
            annotations.append(
                dict(
                    x=index,
                    y=-0.01,
                    text=gene,
                    xref="x",
                    yref="paper",
                    xanchor="center",
                    yanchor="top",
                    showarrow=False,
                    font=dict(color="red", size=12),
                    textangle=-90,
                )
            )
        else:
            annotations.append(
                dict(
                    x=index,
                    y=-0.01,
                    text=gene,
                    xref="x",
                    yref="paper",
                    xanchor="center",
                    yanchor="top",
                    showarrow=False,
                    font=dict(color="blue", size=12),
                    textangle=-90,
                )
            )
    figure.update_layout(
        xaxis=dict(
            tickvals=list(range(0, len(geneSort))),
            ticktext=[""] * len(geneSort),
        ),
        annotations=annotations,
    )
    figure = optFig(figure)
    return figure, plotDf


def build_cell_score_plot(
    processor,
    cellIDs,
    annotation,
    markerDict,
    title,
    layer=None,
    use_raw=False,
    showNum=5,
    geneUsed=5,
    markerUsed=5,
):
    adata = processor.adata
    if isinstance(annotation, str) and annotation == "selected":
        adata.obs["group_by"] = "not selected"
        adata.obs.loc[cellIDs, "group_by"] = "selected"
        groupby = "group_by"
        cluster = "selected"
    else:
        adata.obs["group_by"] = annotation
        groupby = "group_by"
        cluster = cellIDs

    if len(adata) > 100:
        min_cells = 50
    else:
        min_cells = int(len(adata) * 0.5)
    sc.pp.filter_genes(adata, min_cells=min_cells)

    markerDict = {
        key: [gene for gene in _as_list(markerDict[key]) if gene in adata.var_names]
        for key in markerDict
    }
    markerDict = {key: genes for key, genes in markerDict.items() if len(genes) > 0}

    cosg.cosg(
        adata,
        groupby=groupby,
        n_genes_user=markerUsed,
        reference="rest",
        remove_lowly_expressed=True,
        expressed_pct=0.2,
    )
    marker_cosg = pd.Series(
        adata.uns["rank_genes_groups"]["scores"][cluster],
        index=adata.uns["rank_genes_groups"]["names"][cluster],
    )
    gene_i = marker_cosg.index

    total_genes = list(set([gene for genes in markerDict.values() for gene in genes]))
    cosgAdata = adata[:, total_genes].copy()
    cosg.cosg(
        cosgAdata,
        groupby=groupby,
        n_genes_user=len(total_genes),
        reference="rest",
        remove_lowly_expressed=False,
    )
    marker_cosg = pd.concat(
        [
            marker_cosg,
            pd.Series(
                cosgAdata.uns["rank_genes_groups"]["scores"][cluster],
                index=cosgAdata.uns["rank_genes_groups"]["names"][cluster],
            ),
        ]
    )
    marker_cosg = marker_cosg[~marker_cosg.index.duplicated(keep="first")]

    gene_score_frames = []
    for key in markerDict:
        gene_j = list(set(markerDict[key]))

        if geneUsed:
            gene_j = sorted(gene_j, key=lambda x: list(marker_cosg.index).index(x))[:geneUsed]
            markerDict[key] = gene_j

        gene_score = compute_cell_scores(
            processor,
            gene_i,
            gene_j,
            use_rep=None,
            groupby=groupby,
            cluster=cluster,
            cosg_scores=marker_cosg,
        )
        gene_score_frames.append(
            pd.DataFrame([gene_score, [key] * len(gene_score)], index=["score", "cluster"]).T
        )

    plotDf = pd.concat(gene_score_frames, ignore_index=True) if gene_score_frames else pd.DataFrame(columns=["score", "cluster"])
    plotOrder = (
        plotDf.groupby("cluster").apply(lambda subDf: subDf["score"].median()).sort_values(ascending=False).index
        if len(plotDf) > 0 else []
    )
    plotDf["score"] = plotDf["score"].astype(float)

    figure = go.Figure()
    for cluster_name in plotOrder:
        figure.add_trace(
            go.Violin(
                x=[cluster_name] * (plotDf["cluster"] == cluster_name).sum(),
                y=plotDf.loc[plotDf["cluster"] == cluster_name, "score"],
                name=cluster_name,
                box_visible=True,
            )
        )

    figure.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
        ),
        legend=dict(
            font=dict(size=10),
            itemsizing="constant",
        ),
        xaxis=dict(
            tickangle=-45,
            tickvals=plotOrder,
        ),
        yaxis=dict(
            title="Cell Scores",
        ),
    )

    figure = optFig(
        figure,
        cut_off_x=True,
        cutt_off_x_kwargs=dict(func=lambda x: x[:25] + "..." if len(x) > 25 else x),
    )
    return figure, plotDf, marker_cosg
