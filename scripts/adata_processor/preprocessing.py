#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import plotly.express as px
import scanpy as sc
from scanpy._utils import _empty


def _safe_copy_dict(value):
    return {} if value is None else dict(value)


def preprocess_spatial(processor):
    from scripts._utils import _process_image, _check_spatial_data

    library_id, spatial_data = _check_spatial_data(processor.adata.uns, _empty)
    if library_id is not None:
        library_id, img_key, spot_size, scale_factor, crop_coord = _process_image(processor.adata)
        processor.spatialAttr["library_id"] = library_id
        processor.spatialAttr["img_key"] = img_key
        processor.spatialAttr["spot_size"] = spot_size
        processor.spatialAttr["scale_factor"] = scale_factor
        processor.spatialAttr["crop_coord"] = crop_coord
        processor.spatialAttr["circle_radius"] = 1.0 * scale_factor * spot_size * 0.5


def run_sc_data_preprocessing(
    processor,
    qc,
    layer=None,
    normalizeKwargs=None,
    log1P=None,
    hvgKwargs=None,
    dimRedMethod=None,
    PCAKwargs=None,
    neighborKwargs=None,
    umapKwargs=None,
    t_sneKwargs=None,
):
    adata = processor.adata
    normalizeKwargs = _safe_copy_dict(normalizeKwargs)
    hvgKwargs = _safe_copy_dict(hvgKwargs)
    PCAKwargs = _safe_copy_dict(PCAKwargs)
    neighborKwargs = _safe_copy_dict(neighborKwargs)
    umapKwargs = _safe_copy_dict(umapKwargs)
    t_sneKwargs = _safe_copy_dict(t_sneKwargs)

    if layer is None:
        layer = "X"

    if layer != "X" and layer not in adata.layers:
        raise ValueError("Error layer received : {}".format(layer))
    if layer != "X":
        adata.layers["CellClick_X"] = adata.X.copy()
        adata.X = adata.layers[layer]
    else:
        adata.layers["X"] = adata.X.copy()

    if qc == "Normalization":
        sc.pp.normalize_total(adata, **normalizeKwargs)
    elif qc == "log1P":
        if log1P:
            sc.pp.log1p(adata)
    elif qc == "HVG Detection":
        sc.pp.highly_variable_genes(adata, **hvgKwargs)
    elif qc == "Dimension Reduction":
        from sklearn.decomposition import TruncatedSVD
        from sklearn.preprocessing import StandardScaler

        if "highly_variable" in adata.var.columns:
            expr = adata[:, adata.var["highly_variable"]].X
        else:
            expr = adata.X
        expr = StandardScaler(with_mean=False).fit_transform(expr)
        maxScale = 10
        expr[expr > maxScale] = maxScale
        expr[expr < -maxScale] = -maxScale

        transformer = TruncatedSVD(**PCAKwargs)
        adata.obsm["X_pca"] = transformer.fit_transform(expr)

        if dimRedMethod == "PCA":
            pass
        elif dimRedMethod == "UMAP":
            sc.pp.neighbors(adata, **neighborKwargs)
            sc.tl.umap(adata, **umapKwargs)
        elif dimRedMethod in ["TSNE", "t-SNE"]:
            sc.tl.tsne(adata, **t_sneKwargs)
        else:
            raise ValueError("Unknown qc: {}".format(qc))
    else:
        raise ValueError("Unknown qc: {}".format(qc))

    processor.adata = adata
    processor.isPreprocess = qc


def set_metrics(processor):
    if processor.QC_metrics is None:
        adata = processor.adata

        if adata.var_names.str.startswith("MT-").sum() > 0:
            adata.var["mt"] = adata.var_names.str.startswith("MT-")
        elif adata.var_names.str.startswith("mt-").sum() > 0:
            adata.var["mt"] = adata.var_names.str.startswith("mt-")
        else:
            raise ValueError("No mt genes detected, please check it.")

        qc_metrics, gene_df = sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=False, log1p=False)
        processor.QC_metrics = (qc_metrics, gene_df)
    return processor.QC_metrics


def filter_adata(processor, cells_filtered, gene_filtered=None):
    cell_df = processor.QC_metrics[0]
    gene_df = processor.QC_metrics[1]
    cell_mask = ~cells_filtered if cells_filtered is not None else [True] * len(processor.adata)
    gene_mask = ~gene_filtered if gene_filtered is not None else gene_df["n_cells_by_counts"] >= 3

    processor.adata.raw = processor.adata
    processor.adata = processor.adata[cell_mask, gene_mask]
    processor.QC_metrics = (
        cell_df.loc[cell_mask],
        gene_df.loc[gene_mask],
    )
    processor.isPreprocess = "QC"


def build_qc_graph(processor, attribute, axis_min, axis_max, threshold_min, threshold_max):
    def violin_plot(data):
        y_axis = [axis_min[0], axis_max[0]]
        values = [threshold_min[0], threshold_max[0]]

        cells_filtered = (data < values[0]) | (data > values[1])
        df = pd.DataFrame(
            [
                data,
                cells_filtered,
            ],
            index=["values", "cell_filtered"],
        ).T
        fig = px.strip(
            df,
            x="cell_filtered",
            y="values",
            color="cell_filtered",
            color_discrete_map={True: "red", False: "blue"},
        )

        fig.update_layout(
            xaxis={
                "title": None,
                "showticklabels": True,
                "showline": False,
                "tickvals": [0, 1],
                "ticktext": ["Cells Kept", "Cells Filtered"],
            },
            yaxis={
                "title": attribute,
                "range": y_axis,
                "showticklabels": False,
                "showline": False,
            },
            margin={"l": 0, "b": 0, "t": 0, "r": 0},
            hovermode="closest",
            showlegend=False,
        )
        return fig, cells_filtered

    switch_dict = {
        "UMI Counts": violin_plot,
        "Gene Counts": violin_plot,
        "MT PCT": violin_plot,
    }
    attribute_map = {
        "UMI Counts": processor.QC_metrics[0]["total_counts"],
        "Gene Counts": processor.QC_metrics[0]["n_genes_by_counts"],
        "MT PCT": processor.QC_metrics[0]["pct_counts_mt"],
    }
    return switch_dict[attribute](data=attribute_map[attribute])

