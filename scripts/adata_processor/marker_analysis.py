#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy import sparse

import cosg as cosg


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, pd.Index, np.ndarray)):
        return list(value)
    return [value]


def _safe_copy_dict(value):
    return {} if value is None else dict(value)


def return_gene_similarity(processor, gene_i, gene_j, use_rep=None, min_exp_pct=0.05, groupby=None, weighted=False, **kwargs):
    adata = processor.adata
    if "weightGroup" in kwargs:
        weighted = kwargs.pop("weightGroup")
    if kwargs:
        raise TypeError("Unexpected keyword arguments: {}".format(", ".join(kwargs.keys())))

    gene_i = _as_list(gene_i)
    gene_j = _as_list(gene_j)

    if use_rep:
        if use_rep == "X":
            cellxgene_i = adata[:, gene_i].X
            cellxgene_j = adata[:, gene_j].X
        else:
            cellxgene_i = adata[:, gene_i].layers[use_rep]
            cellxgene_j = adata[:, gene_j].layers[use_rep]
    else:
        cellxgene_i = adata[:, gene_i].X
        cellxgene_j = adata[:, gene_j].X

    if sparse.issparse(cellxgene_j):
        get_nonzeros = lambda X: X.getnnz(axis=0)
    else:
        get_nonzeros = lambda X: np.count_nonzero(X, axis=0)

    if min_exp_pct:
        n_cells_expressed = get_nonzeros(cellxgene_j)
        n_cells_i = cellxgene_j.shape[0]
        gene_mask = n_cells_expressed > n_cells_i * min_exp_pct
    else:
        gene_mask = [True] * cellxgene_j.shape[1]
    cellxgene_j = cellxgene_j[:, gene_mask]

    from sklearn.metrics.pairwise import cosine_similarity

    gene_cosine_sim = cosine_similarity(X=cellxgene_i.T, Y=cellxgene_j.T, dense_output=True)

    if weighted and groupby and len(adata.obs[groupby].unique()) > 1:
        from scanpy.preprocessing._utils import _get_mean_var

        i_mean = None
        j_mean = None
        group_info = adata.obs[groupby]
        groups_order = np.unique(group_info)
        for group_i in groups_order:
            cell_mask = group_info == group_i
            group_cellxgene = cellxgene_i[cell_mask, :]
            mean, var = _get_mean_var(group_cellxgene)
            i_mean = mean if i_mean is None else np.vstack([i_mean, mean])
            mean, var = _get_mean_var(cellxgene_j[cell_mask, :])
            j_mean = mean if j_mean is None else np.vstack([j_mean, mean])
        group_cosine_sim = cosine_similarity(X=i_mean.T, Y=j_mean.T, dense_output=True)
    else:
        group_cosine_sim = np.array([[1]] * cellxgene_i.shape[1])

    cosine_sim = pd.DataFrame(np.multiply(gene_cosine_sim, group_cosine_sim), index=gene_i, columns=gene_j)
    return cosine_sim


def return_gene_similarity_graph(processor, gene, annotationSeries, showNum=10):
    adata = processor.adata
    adata.obs["group_by"] = annotationSeries
    results = return_gene_similarity(
        processor,
        gene,
        adata.var_names,
        use_rep=None,
        min_exp_pct=0.05,
        weighted=True,
        groupby="group_by",
    )
    results = results.iloc[:showNum]
    dot_color_df, dot_size_df = processor.returnDotColorAndSize(
        processor.adata, results.index, groupby="group_by", standard_scale="var"
    )

    sorted_counts = True
    if sorted_counts:
        groupOrder = list(adata.obs["group_by"].value_counts(ascending=False).index)[::-1]
    else:
        groupOrder = sorted(adata.obs["group_by"].unique())

    return processor.returnDotplot(dot_color_df, dot_size_df, "group_by", groupOrder)


def return_marker_df(processor, groupby, key_added, **kwargs):
    adata = processor.adata
    groupby = processor._normalize_groupby(groupby)

    cosg.cosg(adata, groupby=groupby, key_added=key_added, **kwargs)
    adata.uns["{}_annotation".format(key_added)] = adata.obs[groupby].copy()
    return pd.DataFrame(adata.uns[key_added]["names"])


def get_marker_gene_plot_for_groups(processor, groupA, groupB, groupValue, graphType, groupBy="group_by", markerGeneUsed=3):
    adata = processor.adata
    if isinstance(groupB, list):
        subset_mask = adata.obs_names.isin(groupA + groupB)
        adata = adata[subset_mask].copy()
        adata.obs[groupBy] = [groupValue[0]] * len(adata)
        adata.obs.loc[adata.obs_names.isin(groupB), "group_by"] = groupValue[1]
    elif isinstance(groupB, pd.Series):
        if len(groupA) > 0:
            adata = adata[adata.obs_names.isin(groupA), :].copy()
        else:
            adata = adata.copy()
        adata.obs[groupBy] = groupB.reindex(adata.obs_names).copy()
    else:
        raise TypeError("Unexpected type of groupB was received: {}".format(type(groupB)))

    adata.obs[groupBy] = adata.obs[groupBy].astype("category").cat.set_categories(
        sorted(adata.obs[groupBy].unique())
    )
    cosg.cosg(
        adata,
        groupby=groupBy,
        key_added="cosg",
        mu=1,
        use_raw=False,
        remove_lowly_expressed=True,
        n_genes_user=50,
    )

    sorted_counts = False
    if sorted_counts:
        groupOrder = list(adata.obs["group_by"].value_counts(ascending=False).index)[::-1]
    else:
        groupOrder = sorted(adata.obs["group_by"].unique())[::-1]
    marker_df = pd.DataFrame(adata.uns["cosg"]["names"])[groupOrder]
    markerGeneNameList = marker_df.values[:markerGeneUsed].reshape((1, -1), order="F")[0][::-1]

    if len(adata.obs[groupBy].unique()) > 2:
        standard_scale = "var"
    else:
        standard_scale = None

    dot_color_df, dot_size_df = processor.returnDotColorAndSize(
        adata,
        markerGeneNameList,
        groupBy,
        standard_scale=standard_scale,
    )
    if graphType == "Dot":
        return processor.returnDotplot(dot_color_df, dot_size_df, groupBy, groupOrder)
    if graphType == "Heatmap":
        return processor.returnHeatmapPlot(
            dot_color_df,
            var_groups=None,
            groupby=groupBy,
        )
    raise ValueError("Unexpected graph type received: {}".format(graphType))


def get_marker_gene_plot(processor, groupBy, markerGeneUsed=5, cosgParams=None):
    cosgParams = _safe_copy_dict(cosgParams) or dict(mu=1, remove_lowly_expressed=True, n_genes_user=50)
    if isinstance(groupBy, (str, float)):
        marker_df = return_marker_df(processor, groupby=groupBy, key_added="cosg")
    else:
        processor.adata.obs["group_by"] = groupBy
        marker_df = return_marker_df(processor, groupby="group_by", key_added="cosg", **cosgParams)
        groupBy = "group_by"

    markerGeneNameList = marker_df.values[:markerGeneUsed].reshape((1, -1), order="F")[0]
    dot_color_df, dot_size_df = processor.returnDotColorAndSize(processor.adata, markerGeneNameList, groupBy)
    groupOrder = list(processor.adata.obs[groupBy].value_counts(ascending=False).index)[::-1]
    return processor.returnDotplot(dot_color_df, dot_size_df, groupBy, groupOrder)


def compute_expression_component_scores(adata, gene_i, gene_j, use_rep=None):
    if use_rep:
        if use_rep == "X":
            cellxgene_i = adata[:, gene_i].X
            cellxgene_j = adata[:, gene_j].X
        else:
            cellxgene_i = adata[:, gene_i].layers[use_rep]
            cellxgene_j = adata[:, gene_j].layers[use_rep]
    else:
        cellxgene_i = adata[:, gene_i].X
        cellxgene_j = adata[:, gene_j].X

    def return_none_zero_counts(X, axis):
        if sparse.issparse(X):
            get_nonzeros = lambda X, axis: X.getnnz(axis)
        else:
            get_nonzeros = lambda X, axis: np.count_nonzero(X, axis)
        return get_nonzeros(X, axis)

    cell_mask_i = return_none_zero_counts(cellxgene_i, axis=1) > 0
    cell_mask_j = return_none_zero_counts(cellxgene_j, axis=1) > 0
    cell_mask = cell_mask_i | cell_mask_j
    cellxgene_i = cellxgene_i[cell_mask]
    cellxgene_j = cellxgene_j[cell_mask]

    def _sparse_nanmean(X, axis):
        if not sparse.issparse(X):
            raise TypeError("X must be a sparse matrix")

        Z = X.copy()
        Z.data = np.isnan(Z.data)
        Z.eliminate_zeros()
        n_elements = Z.shape[axis] - Z.sum(axis)

        Y = X.copy()
        Y.data[np.isnan(Y.data)] = 0
        Y.eliminate_zeros()

        s = Y.sum(axis, dtype="float64")
        m = s / n_elements
        return m

    def _nan_means(x, axis, dtype=None):
        if sparse.issparse(x):
            return np.array(_sparse_nanmean(x, axis=axis)).flatten()
        return np.nanmean(x, axis=axis, dtype=dtype)

    i_mean = _nan_means(cellxgene_i, axis=1)
    if sparse.issparse(cellxgene_j):
        cellxgene_j = cellxgene_j.todense()

    def custom_sigmoid(x, y, k=0.5, scale=1):
        return scale * (1 / (1 + np.exp(-k * (x - y))))

    return pd.DataFrame(
        custom_sigmoid(cellxgene_j, np.array([i_mean] * cellxgene_j.shape[1]).T),
        index=adata.obs_names[cell_mask],
        columns=gene_j,
    )


def compute_cell_scores(processor, gene_i, gene_j, use_rep=None, groupby=None, cluster=None, cosg_scores=None):
    adata = processor.adata
    marker_scores = return_gene_similarity(
        processor,
        gene_i,
        gene_j,
        groupby=groupby,
        weighted=True,
        min_exp_pct=None,
    )

    if cosg_scores is None:
        cosgAdata = adata[:, list(set(gene_i + gene_j))].copy()
        cosg.cosg(
            cosgAdata,
            groupby=groupby,
            n_genes_user=len(set(gene_i + gene_j)),
            reference="rest",
            remove_lowly_expressed=False,
        )
        cosg_scores = pd.Series(
            cosgAdata.uns["rank_genes_groups"]["scores"][cluster],
            index=cosgAdata.uns["rank_genes_groups"]["names"][cluster],
        )
    cosg_i = cosg_scores[gene_i]
    cosg_j = cosg_scores[gene_j]

    marker_scores = cosg_j.index.map(
        lambda x: 1 if x in cosg_i.index else marker_scores[x].sum() * (cosg_j[x] / cosg_i.sum())
    )

    exp_scores = compute_expression_component_scores(
        adata[adata.obs[groupby] == cluster],
        gene_i,
        gene_j,
        use_rep=use_rep,
    )
    for col in exp_scores:
        if col in gene_i:
            exp_scores[col] = [1] * len(exp_scores)

    return (exp_scores.values.dot(marker_scores.values)) / len(gene_j)
