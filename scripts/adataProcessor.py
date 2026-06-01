#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: preprocessing and visualization for adata in CellMarker
@version: 1.0.0
@file: adataProcessor.py
@time: 2023/11/7 17:07
"""
import re

import dash
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import sparse

import plotly.express as px
import plotly.graph_objects as go

import scanpy as sc
from scanpy._utils import _empty
import cosg as cosg

from __settings_layout import pos_cmap_dash, myColors
from scripts.utils import table_type, splitIndex, mappingColor, centerGraph, optFig


class AdataProcessor(object):
    """
    preprocessing and visualization for adata in CellMarker
    And
    """

    def __init__(self, adata):
        self.adata = adata
        self.spatialAttr = {}
        self.preprocess()
        self.QC_metrics = None
        self.isPreprocess = None # status for preprocessing

    # preprocess for spatial adata
    def preprocess(self):
        from scripts._utils import _process_image, _check_spatial_data

        library_id, spatial_data = _check_spatial_data(self.adata.uns, _empty)
        if library_id is not None:
            library_id, img_key, spot_size, scale_factor, crop_coord = _process_image(self.adata)
            self.spatialAttr["library_id"] = library_id
            self.spatialAttr["img_key"] = img_key
            self.spatialAttr["spot_size"] = spot_size
            self.spatialAttr["scale_factor"] = scale_factor
            self.spatialAttr["crop_coord"] = crop_coord
            self.spatialAttr["circle_radius"] = 1.0 * scale_factor * spot_size * 0.5

    def scDataPreprocessing(
        self, qc, layer=None,
        normalizeKwargs=None, log1P=None, hvgKwargs=None,
        dimRedMethod=None, PCAKwargs=None, neighborKwargs=None, umapKwargs=None, t_sneKwargs=None,
    ):
        adata = self.adata

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
            from sklearn.preprocessing import StandardScaler
            from sklearn.decomposition import TruncatedSVD

            if "highly_variable" in adata.var.columns:
                expr = adata[:, adata.var["highly_variable"]].X
            else:
                expr = adata.X
            expr = StandardScaler(with_mean=False).fit_transform(expr)
            maxScale = 10
            expr[expr > maxScale] = maxScale
            expr[expr < -maxScale] = -maxScale

            transformer = TruncatedSVD(**PCAKwargs)
            adata.obsm['X_pca'] = transformer.fit_transform(expr)

            if dimRedMethod == "PCA":
                pass
            elif dimRedMethod == "UMAP":
                sc.pp.neighbors(adata, **neighborKwargs)
                sc.tl.umap(adata, **umapKwargs)
            elif dimRedMethod == "TSNE":
                sc.tl.tsne(adata, **t_sneKwargs)
            else:
                raise ValueError("Unknown qc: {}".format(qc))
        else:
            raise ValueError("Unknown qc: {}".format(qc))

        self.adata = adata
        self.isPreprocess = qc

    def set_metrics(self):
        if self.QC_metrics is None:

            adata = self.adata

            if adata.var_names.str.startswith("MT-").sum() > 0:
                adata.var["mt"] = adata.var_names.str.startswith("MT-")
            elif adata.var_names.str.startswith("mt-").sum() > 0:
                adata.var["mt"] = adata.var_names.str.startswith("mt-")
            else:
                raise ValueError("No mt genes detected, please check it.")

            qc_metrics, gene_df = sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=False, log1p=False)

            # import scrublet as scr
            # scrub = scr.Scrublet(adata.X)
            # doublet_scores, predicted_doublets = scrub.scrub_doublets(verbose=False)
            # qc_metrics["doublet_scores"] = doublet_scores
            # qc_metrics["predicted_doublets"] = predicted_doublets
            self.QC_metrics = (qc_metrics, gene_df)
        return self.QC_metrics

    def filter_adata(
            self, cells_filtered, gene_filtered=None
            # gene_counts_x_value, gene_counts_y_value, mtPCT_y_value,
            # cells_per_gene_x_value, cells_per_gene_y_value
    ):
        cell_df = self.QC_metrics[0]
        gene_df = self.QC_metrics[1]
        cell_mask = ~cells_filtered if cells_filtered is not None else [True]*len(self.adata)
        gene_mask = ~gene_filtered if gene_filtered is not None else gene_df["n_cells_by_counts"] >= 3
        # gene_mask = (
        #         gene_df["n_cells_by_counts"] >= cells_per_gene_x_value[0] &
        #         gene_df["n_cells_by_counts"] <= cells_per_gene_x_value[1] &
        #         gene_df["total_counts"] >= cells_per_gene_y_value[0] &
        #         gene_df["total_counts"] <= cells_per_gene_y_value[1]
        # )
        self.adata.raw = self.adata
        self.adata = self.adata[cell_mask, gene_mask]
        self.QC_metrics = (
            cell_df.loc[cell_mask],
            gene_df.loc[gene_mask]
        )
        self.isPreprocess = "QC"

    def returnQCGraph(self, attribute, axis_min, axis_max, threshold_min, threshold_max):
        def violinPlot(data):
            y_axis = [axis_min[0], axis_max[0]]
            values = [threshold_min[0], threshold_max[0]]

            cells_filtered = (data < values[0]) | (data > values[1])
            df = pd.DataFrame(
                [
                    data, cells_filtered
                ], index=["values", "cell_filtered"]
            ).T
            fig = px.strip(
                df, x="cell_filtered", y="values", color="cell_filtered",
                color_discrete_map={True: "red", False: "blue"},
            )

            fig.update_layout(
                xaxis={
                    'title': None, 'showticklabels': True, 'showline': False,
                    "tickvals": [0, 1], "ticktext": ["Cells Kept", "Cells Filtered"],
                    # "rangeslider": dict(visible=True),
                },
                yaxis={
                    'title': attribute, 'range': y_axis, 'showticklabels': False, 'showline': False
                },
                margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
                hovermode='closest', showlegend=False
            )
            return fig, cells_filtered

        switchDict = {
            "UMI Counts": violinPlot,
            "Gene Counts": violinPlot,
            "MT PCT": violinPlot,
        }
        attributeMap = {
            "UMI Counts": self.QC_metrics[0]['total_counts'],
            "Gene Counts": self.QC_metrics[0]['n_genes_by_counts'],
            "MT PCT": self.QC_metrics[0]['pct_counts_mt'],
        }
        return switchDict[attribute](data=attributeMap[attribute])

    def returnGeneSimilarity(self, gene_i, gene_j, use_rep=None, min_exp_pct=0.05, groupby=None, weighted=False):
        adata = self.adata
        # i the marker identified by COSG(index of results), j: the marker from reference(columns of results)
        if isinstance(gene_i, str):
            gene_i = [gene_i]
        else:
            gene_i = list(gene_i)

        if isinstance(gene_j, str):
            gene_j = [gene_j]
        else:
            gene_j = list(gene_j)

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

        if weighted and groupby and len(adata.obs[groupby].unique())>1:
            from scanpy.preprocessing._utils import _get_mean_var
            i_mean = None
            j_mean = None
            group_info = adata.obs[groupby].copy()
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

    def returnGeneSimilarityGraph(self, gene, annotationSeries, showNum=10):
        adata = self.adata
        adata.obs["group_by"] = annotationSeries
        results = self.returnGeneSimilarity(
            gene, adata.var_names, use_rep=None, min_exp_pct=0.05, weightGroup=True, groupby="group_by"
        )
        results = results[: showNum]
        dot_color_df, dot_size_df = self.returnDotColorAndSize(
            self.adata, results.index, groupby="group_by", standard_scale="var"
        )

        sorted_counts = True
        if sorted_counts:
            groupOrder = list(adata.obs["group_by"].value_counts(ascending=False).index)[::-1]
        else:
            groupOrder = sorted(adata.obs["group_by"].unique())

        return self.returnDotplot(dot_color_df, dot_size_df, "group_by", groupOrder)

    def returnMarkerDf(self, groupby, key_added, **kwargs):
        adata = self.adata
        if isinstance(groupby, pd.Series):
            adata.obs["group_by"] = groupby
            groupby = "group_by"

        cosg.cosg(adata, groupby=groupby, key_added=key_added, **kwargs)
        adata.uns["{}_annotation".format(key_added)] = adata.obs[groupby].copy()
        return pd.DataFrame(adata.uns[key_added]['names'])

    @staticmethod
    def returnDotColorAndSize(
        adata, var_names,
        groupby, expression_cutoff=0.0, mean_only_expressed=False,
        standard_scale=None
    ):
        from scanpy.plotting._anndata import _prepare_dataframe
        categories, obs_tidy = _prepare_dataframe(adata, var_names, groupby)

        # 1. compute fraction of cells having value > expression_cutoff
        # transform obs_tidy into boolean matrix using the expression_cutoff
        obs_bool = obs_tidy > expression_cutoff

        # compute the sum per group which in the boolean matrix this is the number
        # of values > expression_cutoff, and divide the result by the total number of
        # values in the group (given by `count()`)
        dot_size_df = (
                obs_bool.groupby(level=0).sum() / obs_bool.groupby(level=0).count()
        )

        # https://github.com/theislab/scanpy/blob/43379e038c5db3f917f45cc69889de0dcb6caa35/scanpy/plotting/_dotplot.py
        mean_only_expressed = True # for Wang's idea
        if mean_only_expressed:
            dot_color_df = (
                obs_tidy.mask(~obs_bool).groupby(level=0).mean().fillna(0)
            )
        else:
            dot_color_df = obs_tidy.groupby(level=0).mean()

        if standard_scale == 'group':
            dot_color_df = dot_color_df.sub(dot_color_df.min(1), axis=0)
            dot_color_df = dot_color_df.div(dot_color_df.max(1), axis=0).fillna(0)
        elif standard_scale == 'var':
            dot_color_df -= dot_color_df.min(0)
            dot_color_df = (dot_color_df / dot_color_df.max(0)).fillna(0)
        elif standard_scale is None:
            pass
        else:
            pass
        return dot_color_df, dot_size_df

    @staticmethod
    def returnDotplot(dot_color_df, dot_size_df, groupby, groupOrder):

        # Above, generate dot_color_df
        dot_size_df[groupby] = dot_size_df.index
        dot_size_melt = dot_size_df.melt(id_vars=[groupby])

        dot_color_df[groupby] = dot_color_df.index
        dot_color_melt = dot_color_df.melt(id_vars=[groupby])

        data = go.Scatter(
            x=dot_color_melt['variable'],
            y=dot_color_melt[groupby],
            mode='markers',
            marker=dict(
                size=dot_size_melt['value'] * 25, color=dot_color_melt['value'],
                showscale=True, opacity=1,
                colorscale=pos_cmap_dash
            ),

            text=dot_size_melt['value'] * 100,
            hovertemplate=
            "<b>Gene: %{x}</b><br>" +
            "Group: %{y}<br>" +
            "Average expression: %{marker.color:,.2f}<br>" +
            "Fraction: %{text:,.2f}%" +
            "<extra></extra>",
        )

        fig = go.Figure(data=data)

        fig.update_xaxes(
            type='category', tickangle=-90, ticklen=5, tickcolor='white', ticks='outside',
            # categoryorder='array', categoryarray=list(groupOrder)
            tickmode='array',
            tickvals=dot_color_melt['variable'].unique(),
            ticktext=[
                f"<i>{g}</i>"
                for g in dot_color_melt['variable'].unique()
            ]
        )
        fig.update_yaxes(
            type='category', title_text="", ticklen=5, tickcolor='white', ticks='outside',
            categoryorder='array', categoryarray=list(groupOrder)
        )

        fig.update_layout(
            autosize=True,
            plot_bgcolor='rgba(0, 0, 0, 0)'
        )


        plotDf = pd.concat([dot_size_melt[[groupby, 'variable', 'value']], dot_color_melt[["value"]]], axis=1)
        plotDf.columns = ["Group", "Gene", "Fraction(%)", "Average Expression"]
        plotDf["Fraction(%)"] = plotDf["Fraction(%)"] * 100

        fig = optFig(fig, border=True)
        return fig, plotDf

    # Show scatter plots for one given gene
    def get_marker_scatter(self, use_rep, marker_gene):
        adata = self.adata

        # also need to change the order of coordinates
        # For pca only use the first two dimensions, can extend this function in future
        if use_rep != "spatial":
            df_embedding = pd.DataFrame(adata.obsm[use_rep][:, :2])
        else:
            scale_factor = self.spatialAttr["scale_factor"]
            df_embedding = pd.DataFrame(np.multiply(adata.obsm["spatial"], scale_factor)[:, :2])
        df_embedding.index = adata.obs_names
        df_embedding.columns = ['DIM1', 'DIM2']
        df_embedding["Expression"] = sc.get.obs_df(adata, marker_gene)

        df_embedding.index = adata.obs_names
        # Higher values plotted on top, null values on bottom
        df_embedding = df_embedding.sort_values(by="Expression")

        if use_rep != "spatial":
            fig = go.Figure()
        else:
            from scripts._utils import _check_img
            img, img_key = _check_img(
                spatial_data=self.adata.uns["spatial"][self.spatialAttr["library_id"]],
                img=None,
                img_key=self.spatialAttr["img_key"]
            )
            fig = px.imshow(img)
            # if img is None:
            #     fig = go.Figure()
            # else:
            #     fig = px.imshow(img)

        # import matplotlib as plt
        colorScale = plt.get_cmap("myCmpGra")
        colorScale = [colorScale(i) for i in range(colorScale.N)]

        # Convert RGBA to RGB and normalize to [0, 1]
        colorScale = [(r, g, b) for r, g, b, _ in colorScale]
        # Step 3: Create a Plotly colorscale
        colorScale = [[i / (len(colorScale) - 1), f'rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})'] for
                      i, (r, g, b)
                      in enumerate(colorScale)]

        fig.add_trace(
            go.Scatter(
                mode='markers',
                x=df_embedding["DIM1"],
                y=df_embedding["DIM2"],
                marker=dict(
                    colorscale=colorScale if use_rep != "spatial" else "viridis",
                    size=6000 / len(df_embedding) if use_rep != "spatial" else 4,
                    showscale=True,
                ),
                marker_color=df_embedding["Expression"],  # expr_df[marker_gene],
                # color_continuous_scale=pos_cmap_dash,
            ),
        )

        xMin, xMax, yMin, yMax = centerGraph(
            (df_embedding['DIM1'].min(), df_embedding['DIM1'].max()),
            (df_embedding['DIM2'].min(), df_embedding['DIM2'].max()),
        )
        use_rep = use_rep.upper()
        fig.update_layout(
            xaxis=dict(
                range=[xMin, xMax],
                showticklabels=False, showgrid=False, zeroline=False, ticks="", title="{}_1".format(use_rep)
            ),
            yaxis=dict(
                range=[yMin, yMax] if use_rep != "spatial".upper() else [yMax, yMin],
                showticklabels=False, showgrid=False, zeroline=False, ticks="", title="{}_2".format(use_rep)
            ),
            legend=dict(
                font=dict(
                    size=10  # Set the font size of the legend
                ),
                itemsizing='constant'  # Ensure legend items are sized consistently
            ),
            # title='UMAP visualization',
            template="simple_white",
            margin=dict(
                l=50,
                r=50,
                # b=50,
                # t=50,
                # pad=4
            ),
            title=dict(
                text=f"<i>{marker_gene}</i>",
                x=0.5,
            ),
            # autosize=True,
            dragmode='lasso',
            hovermode='closest',
        )

        fig = optFig(fig, border=True if use_rep != "spatial".upper() else False)

        return fig, df_embedding

    # Refer to: https://github.com/theislab/scanpy/blob/256f5944cd03fc0b8b510d607502d7170f8e5813/scanpy/plotting/_anndata.pyabs
    # Refer to: https://github.com/theislab/scanpy/blob/43379e038c5db3f917f45cc69889de0dcb6caa35/scanpy/plotting/_dotplot.py
    def get_dot_plot(self, var_names, groupby, clusters=[], selectedCells=[]):
        adata = self.adata
        if isinstance(groupby, pd.Series):
            adata.obs["group_by"] = groupby
            groupby = "group_by"

        if selectedCells is None:  # no select cells
            selectedSeries = pd.Series([False] * len(adata.obs), index=adata.obs_names)
        elif len(selectedCells) == 0:  # select all cells
            selectedSeries = pd.Series([True] * len(adata.obs), index=adata.obs_names)
        else:
            selectedSeries = adata.obs_names.isin(selectedCells)
        selectedSeries = selectedSeries | adata.obs[groupby].isin(clusters)
        adata = adata[selectedSeries]

        if len(adata.obs[groupby].unique()) > 2:
            standard_scale = "var"
        else:
            standard_scale = None

        dot_color_df, dot_size_df = self.returnDotColorAndSize(
            adata, var_names, groupby,
            standard_scale=standard_scale
        )

        sorted_counts = False
        if sorted_counts:
            groupOrder = list(adata.obs[groupby].value_counts(ascending=False).index)[::-1]
        else:
            groupOrder =  sorted(adata.obs[groupby].unique(), reverse=True)

        return self.returnDotplot(dot_color_df, dot_size_df, groupby, groupOrder)

    def get_fig_by_embedding(self, use_rep, groupby, selectedCells=None, fixedCells=None, refAnnotation=None):
        adata = self.adata
        if selectedCells is None:
            selectedCells = adata.obs_names

        ### For pca only use the first two dimensions, can extend this function in future
        # if use_rep != self.spatialAttr.get("key", None):
        if use_rep == "spatial" and "spatial" in adata.uns:
            scale_factor = self.spatialAttr["scale_factor"]
            df_embedding = pd.DataFrame(np.multiply(adata.obsm["spatial"], scale_factor)[:, :2])
        else:
            df_embedding = pd.DataFrame(adata.obsm[use_rep][:, :2])
        df_embedding.index = adata.obs_names
        df_embedding.columns = ['DIM1', 'DIM2']
        df_embedding['customdata'] = adata.obs_names
        if groupby == "none":
            df_embedding[groupby] = [""] * len(df_embedding)
        else:
            df_embedding[groupby] = adata.obs[groupby] if not isinstance(refAnnotation, pd.Series) else refAnnotation
        groupOrder = df_embedding[groupby].value_counts(ascending=False).index
        colorsDict = mappingColor(groupOrder, myColors)

        size = 6000/len(df_embedding) # default
        # size = 1200 / len(df_embedding)  # _default
        # size = 20000/len(df_embedding)
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
                "modifyName": "",  # similar dict with "selected" except name and modifyName key-value pair
            }
        }

        refCol = splitIndex(df_embedding.index, [fixedCells, selectedCells])
        refValues = sorted(refCol.unique())
        embeddingList = []
        for refValue in refValues:
            df_selected = df_embedding.loc[refCol == refValue]

            embeddingDict = embeddingDictSwitchDict[""] if len(refValues) == 1 else embeddingDictSwitchDict[refValue]
            embeddingDict["embeddingDf"] = df_selected
            embeddingList.append(embeddingDict)

        # Create figure
        if use_rep != "spatial":
            fig = go.Figure()
        else:
            from scripts._utils import _check_img
            img, img_key = _check_img(
                spatial_data=self.adata.uns["spatial"][self.spatialAttr["library_id"]],
                img=None,
                img_key=self.spatialAttr["img_key"]
            )
            fig = px.imshow(img)

        for embeddingDict in embeddingList:
            embeddingDf = embeddingDict["embeddingDf"]
            group_info = embeddingDf[groupby].values
            # group_order = np.unique(embeddingDf[groupby])

            for group in groupOrder:
                idx = group_info == group
                df_i = embeddingDf.loc[idx]

                # an easy method to define the size of spatial scatter
                marker = embeddingDict["marker"]
                if use_rep == "spatial":
                    marker["size"] = 4

                colors = [colorsDict[group]] * len(df_i)
                marker["color"] = colors
                fig.add_trace(
                    go.Scatter(
                        mode='markers',
                        x=df_i['DIM1'], y=df_i['DIM2'],
                        customdata=df_i["customdata"], opacity=embeddingDict["opacity"],
                        marker=marker,
                        # group should be str type
                        name=str(group) + embeddingDict["modifyName"],
                        # name=str(group),
                    ),
                )

        xMin, xMax, yMin, yMax = centerGraph(
            (df_embedding['DIM1'].min(), df_embedding['DIM1'].max()),
            (df_embedding['DIM2'].min(), df_embedding['DIM2'].max()),
        )

        if use_rep.startswith("X_"):
            use_rep = re.sub("X_", "", use_rep)
        use_rep = use_rep.upper()

        fig.update_layout(
            xaxis=dict(
                range=[xMin, xMax],
                showticklabels=False, showgrid=False, zeroline=False, ticks="", title="{}_1".format(use_rep)
            ),
            yaxis=dict(
                range=[yMin, yMax] if use_rep != "spatial".upper() else [yMax, yMin],
                showticklabels=False, showgrid=False, zeroline=False, ticks="", title="{}_2".format(use_rep)
            ),
            legend=dict(
                font=dict(
                    size=10  # Set the font size of the legend
                ),
                itemsizing='constant'  # Ensure legend items are sized consistently
            )
        )

        fig.update_layout(
            # title='UMAP visualization',
            template="plotly_white",
            margin=dict(
                l=50,
                r=50,
                # b=50,
                # t=50,
                # pad=4
            ),
            # autosize=True,
            dragmode='lasso',
            hovermode='closest',
        )

        plotDf = embeddingDf[['DIM1', 'DIM2', groupby]]
        plotDf["selected"] = refCol

        fig = optFig(fig, border=True if use_rep != "spatial".upper() else False)
        return fig, plotDf

    def get_marker_gene_plot_for_groups(self, groupA, groupB, groupValue, graphType, groupBy="group_by",
                                        markerGeneUsed=3):
        # set there is no overlap for groupA and group B
        adata = self.adata.copy()
        if isinstance(groupB, list):
            adata = adata[adata.obs_names.isin(groupA + groupB), :]
            adata.obs[groupBy] = [groupValue[0]] * len(adata)
            adata.obs.loc[adata.obs_names.isin(groupB), "group_by"] = groupValue[1]
        elif isinstance(groupB, pd.Series):
            if len(groupA) > 0:
                adata = adata[adata.obs_names.isin(groupA), :]
            adata.obs[groupBy] = groupB.copy()
        else:
            raise TypeError("Unexpected type of groupB was received: {}".format(type(groupB)))

        adata.obs[groupBy] = adata.obs[groupBy].astype("category").cat.set_categories(
            sorted(adata.obs[groupBy].unique())
        )
        cosg.cosg(
            adata, groupby=groupBy, key_added='cosg', mu=1,
            use_raw=False,
            remove_lowly_expressed=True, n_genes_user=50
        )

        sorted_counts = False
        if sorted_counts:
            groupOrder = list(adata.obs["group_by"].value_counts(ascending=False).index)[::-1]
        else:
            groupOrder = sorted(adata.obs["group_by"].unique())[::-1]
        marker_df = pd.DataFrame(adata.uns['cosg']['names'])[groupOrder]
        markerGeneNameList = marker_df.values[:markerGeneUsed].reshape((1, -1), order="F")[0][::-1]

        if len(adata.obs[groupBy].unique()) > 2:
            standard_scale = 'var'
        else:
            standard_scale = None

        dot_color_df, dot_size_df = self.returnDotColorAndSize(
            adata, markerGeneNameList, groupBy,
            standard_scale=standard_scale
        )
        if graphType == "Dot":
            return self.returnDotplot(dot_color_df, dot_size_df, groupBy, groupOrder)
        elif graphType == "Heatmap":
            return self.returnHeatmapPlot(
                dot_color_df, var_groups=None, groupby=groupBy,
            )
        else:
            raise ValueError("Unexpected graph type received: {}".format(graphType))

    @staticmethod
    def returnHeatmapPlot(dot_color_df, var_groups, groupby):
        if var_groups is None:
            data = go.Heatmap(
                x=dot_color_df.columns,
                y=dot_color_df.index,
                z=dot_color_df,
                colorscale=pos_cmap_dash
            )
        else:
            data = go.Heatmap(
                x=[var_groups, dot_color_df.columns],
                y=dot_color_df.index,

                z=dot_color_df,
                colorscale=pos_cmap_dash
            )
        fig = go.Figure(data=data)
        fig.update_yaxes(title_text=groupby)
        fig.update_layout(xaxis=dict(tickangle=-90))
        fig.update_layout(autosize=True)

        fig = optFig(fig)
        return fig, dot_color_df

    def get_marker_gene_plot(
        self, groupBy, markerGeneUsed=5,
        cosgParams=dict(mu=1, remove_lowly_expressed=True, n_genes_user=50)
    ):
        if isinstance(groupBy, (str, float)):
            marker_df = self.returnMarkerDf(groupby=groupBy, key_added='cosg')
        else:
            self.adata.obs["group_by"] = groupBy

            marker_df = self.returnMarkerDf(groupby="group_by", key_added='cosg', **cosgParams)
            groupBy = "group_by"
        markerGeneNameList = marker_df.values[:markerGeneUsed].reshape((1, -1), order="F")[0]
        dot_color_df, dot_size_df = self.returnDotColorAndSize(self.adata, markerGeneNameList, groupBy)
        groupOrder = list(self.adata.obs[groupBy].value_counts(ascending=False).index)[::-1] # sort counts
        # groupOrder = list(self.adata.obs[groupBy].value_counts(ascending=False).index)
        return self.returnDotplot(dot_color_df, dot_size_df, groupBy, groupOrder)

    def returnMarkerGeneEvaluationPlot(
            self, cellIDs, cellCluster, annotationSeries, marker_ref_path, markerGeneUsed,
            showNum=10, cosgParams=dict(mu=1, remove_lowly_expressed=True),
            # showNum=5, cosgParams=dict(mu=1, remove_lowly_expressed=True),
    ):
        adata = self.adata
        if cellCluster not in annotationSeries.values:  # search a value in index in Series
            # ValueError: Cannot setitem on a Categorical with a new category, set the categories first
            annotationSeries = annotationSeries.cat.add_categories(cellCluster)
        adata.obs["group_by"] = annotationSeries
        adata.obs.loc[cellIDs, "group_by"] = cellCluster

        cosgParams["n_genes_user"] = markerGeneUsed
        cosg.cosg(
            adata, groupby="group_by", key_added='cosg', reference="rest",
            **cosgParams
        )
        markerSeries = pd.Series(
            adata.uns['cosg']['scores'][cellCluster],
            index=adata.uns['cosg']['names'][cellCluster]
        )

        from scipy import io
        loaded_data = io.loadmat(marker_ref_path)
        geneWeight = pd.DataFrame(
            loaded_data['data'].todense(),
            index=[x[0] for x in loaded_data['index'][0]],
            columns=[x[0] for x in loaded_data['columns'][0]]
        )

        geneWeight = geneWeight[list(set(markerSeries.index) & set(geneWeight.columns))]
        # refCOSGScores = markerSeries[geneWeight.columns] / markerSeries[geneWeight.columns].max()
        # scores = geneWeight.values.dot(refCOSGScores)
        # print(geneWeight[overlapGenes])
        # print(markerSeries[overlapGenes]/markerSeries[overlapGenes].max())
        # print()
        scores = np.multiply(
            geneWeight.values.dot(markerSeries[geneWeight.columns] > 0),
            (geneWeight > 0).values.dot(markerSeries[geneWeight.columns] / markerSeries[geneWeight.columns].sum())
        )

        scores = pd.Series(scores, index=geneWeight.index)
        scores = scores.sort_values(ascending=False)[:showNum]

        plotDf = pd.DataFrame(
            [
                [source.split("_")[0] for source in scores.index],
                [source.split("_")[1] for source in scores.index],
                list(scores)
            ],
            index=["tissue", "cell type", "scores"],
        ).T
        plotDf["index"] = scores.index

        myColors = [
            '#FF0000', '#00FF00',
            # '#0000FF',
            '#00FFFF', '#FF00FF',
            '#FFA500',
            # '#800080',
            '#008080', '#FFC0CB',
            # '#E6E6FA',
            '#A52A2A', '#808000', '#FF7F50', '#000080', '#40E0D0',
            '#FFD700', '#F5F5DC', '#D2B48C', '#FA8072', '#87CEEB',
        ]
        colorsDict = mappingColor(plotDf["tissue"].unique(), myColors)
        plotDf["color"] = plotDf["tissue"].apply(lambda x: colorsDict[x])
        # category_order = plotDf['index'].tolist()
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
                    orientation='h',
                    marker=dict(color=subPlotDf["color"]),
                    hovertext=(
                            "tissue: " + subPlotDf["tissue"] +
                            "<br>cell type: " + subPlotDf["cell type"] +
                            "<br>scores: " + subPlotDf["scores"].astype(str)
                    ),
                    hoverinfo='text',
                    # group should be str type
                    name=tissue,
                    # legendgroup=tissue,
                    showlegend=True if index in checkDf.index else False,
                    # name=str(group),
                ),
            )
            annotations.append(dict(
                x=0.01*(plotDf["scores"].max()), y=subPlotDf["index"].values[0],
                text=subPlotDf["cell type"].values[0], font=dict(size=12),
                xanchor="left", showarrow=False
            ))
        for annotation in annotations:
            figure.add_annotation(annotation)

        figure.update_layout(
            title=dict(
                text=cellCluster,
                x=0.5,
                xanchor='center'
            ),
            yaxis=dict(
                tickvals=[""]*len(plotDf),
                # tickangle=-45,
                title="",
            ),
            xaxis=dict(
                title="Marker Gene Score",
            ),
            legend=dict(
                font=dict(
                    size=10  # Set the font size of the legend
                ),
                itemsizing='constant',  # Ensure legend items are sized consistently
                traceorder="reversed",
            ),
        )
        figure = optFig(figure)

        overlapDf = []
        for markerSource in scores.index:
            refGenes = geneWeight.columns[geneWeight.loc[markerSource] > 0]
            markerGenes = markerSeries.index

            def sortGenes(genes, markerSource):
                geneScores = pd.Series(
                    np.multiply(geneWeight.loc[markerSource], markerSeries[geneWeight.columns]),
                    index=geneWeight.columns
                )
                geneSort = list(geneScores.sort_values(ascending=False).index)

                COSGSort = []
                markerSort = []
                for gene in genes:
                    if gene in geneSort:
                        markerSort.append(gene)
                    else:
                        COSGSort.append(gene)

                COSGSort = sorted(COSGSort, key=lambda x: list(markerSeries.index).index(x))
                markerSort = sorted(markerSort, key=lambda x: geneSort.index(x))
                return markerSort + COSGSort

            overlapGenes = list(set(markerGenes) & set(refGenes))
            cosgGenes = list(set(markerGenes) - set(refGenes))
            # onlyRefGenes = list(set(refGenes) - set(markerGenes))
            overlapDf.append([
                markerSource,
                ", ".join(sortGenes(markerGenes, markerSource)),
                ", ".join(refGenes),
                scores[markerSource],
                len(overlapGenes), ", ".join(sortGenes(overlapGenes, markerSource)),
                ", ".join(sortGenes(cosgGenes, markerSource)),
            ])

        overlapDf = pd.DataFrame(
            overlapDf,
            columns=[
                "refCellType", "markerGenes", "refGenes", "score",
                "overlapNum", "Overlap Genes", "COSG Unique Genes",
            ]
        )
        # overlapDf = overlapDf.set_index("refCellType")
        overlapDf.index = overlapDf["refCellType"]

        return figure, overlapDf

    def returnColorDotPlot(self, cellCluster, groupBySeries, overlapDf, cellType):
        adata = self.adata
        adata.obs["group_by"] = groupBySeries
        markerGenes = overlapDf.loc[cellType, "markerGenes"].split(", ")
        # markerRefGene = list(
        #     adata.var_names[
        #         adata.var_names.isin(overlapDf.loc[cellType, "refGenes"])
        #     ]
        # )
        # showGenes = list(set(markerGenes) | set(markerRefGene))
        # plotDf = sc.get.obs_df(adata, showGenes + ["group_by"])
        # geneSort = plotDf.loc[plotDf["group_by"] == cellCluster][showGenes].mean().sort_values(ascending=False).index

        overlapGenes = overlapDf.loc[cellType, "Overlap Genes"].split(", ")
        showGenes = markerGenes
        geneSort = markerGenes

        if len(showGenes) == 0:
            return go.Figure(), pd.DataFrame()
        else:
            figure, plotDf = self.get_dot_plot(var_names=geneSort, groupby="group_by", clusters=[], selectedCells=[])

            # update tick labels
            annotations = []
            for gene, index in zip(geneSort, range(0, len(geneSort))):
                # if (gene in markerGenes) and (gene in markerRefGene):
                #     annotations.append(dict(
                #         x=index, y=-0.01, text=gene, xref='x', yref='paper', xanchor='center', yanchor='top',
                #         showarrow=False, font=dict(color='orange', size=12), textangle=-90,
                #     ))
                # elif gene in markerGenes:
                #     annotations.append(dict(
                #         x=index, y=-0.01, text=gene, xref='x', yref='paper', xanchor='center', yanchor='top',
                #         showarrow=False, font=dict(color='red', size=12), textangle=-90,
                #     ))
                # else:
                #     annotations.append(dict(
                #         x=index, y=-0.01, text=gene, xref='x', yref='paper', xanchor='center', yanchor='top',
                #         showarrow=False, font=dict(color='blue', size=12), textangle=-90,
                #     ))
                if gene in overlapGenes:
                    annotations.append(dict(
                        x=index, y=-0.01, text=gene, xref='x', yref='paper', xanchor='center', yanchor='top',
                        showarrow=False, font=dict(color='red', size=12), textangle=-90,
                    ))
                else:
                    annotations.append(dict(
                        x=index, y=-0.01, text=gene, xref='x', yref='paper', xanchor='center', yanchor='top',
                        showarrow=False, font=dict(color='blue', size=12), textangle=-90,
                    ))
            figure.update_layout(
                xaxis=dict(
                    tickvals=list(range(0, len(geneSort))),
                    ticktext=[''] * len(geneSort),  # Hide default tick labels
                ),
                annotations=annotations
            )
            figure = optFig(figure)
            return figure, plotDf

    @staticmethod
    def returnExpressionScore(adata, gene_i, gene_j, use_rep=None):
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

        def returnNoneZeroCounts(X, axis):
            from scipy import sparse
            if sparse.issparse(X):
                get_nonzeros = lambda X, axis: X.getnnz(axis)
            else:
                get_nonzeros = lambda X, axis: np.count_nonzero(X, axis)
            return get_nonzeros(X, axis)

        cell_mask_i = returnNoneZeroCounts(cellxgene_i, axis=1) > 0
        cell_mask_j = returnNoneZeroCounts(cellxgene_j, axis=1) > 0
        cell_mask = cell_mask_i | cell_mask_j
        cellxgene_i = cellxgene_i[cell_mask]
        cellxgene_j = cellxgene_j[cell_mask]

        # refer to: https://github.com/scverse/scanpy/blob/1.10.4/src/scanpy/tools/_score_genes.py
        from scipy import sparse
        def _sparse_nanmean(X, axis):
            """
            np.nanmean equivalent for sparse matrices
            """
            if not sparse.issparse(X):
                raise TypeError("X must be a sparse matrix")

            # count the number of nan elements per row/column (dep. on axis)
            Z = X.copy()
            Z.data = np.isnan(Z.data)
            Z.eliminate_zeros()
            n_elements = Z.shape[axis] - Z.sum(axis)

            # set the nans to 0, so that a normal .sum() works
            Y = X.copy()
            Y.data[np.isnan(Y.data)] = 0
            Y.eliminate_zeros()

            # the average
            s = Y.sum(axis, dtype="float64")  # float64 for score_genes function compatibility)
            m = s / n_elements

            return m

        def _nan_means(x, axis, dtype=None):

            if sparse.issparse(x):
                return np.array(_sparse_nanmean(x, axis=axis)).flatten()
            return np.nanmean(x, axis=axis, dtype=dtype)

        i_mean = _nan_means(cellxgene_i, axis=1)
        if sparse.issparse(cellxgene_j):
            cellxgene_j = cellxgene_j.todense()

        # return pd.DataFrame(
        #     np.divide(2*cellxgene_j, cellxgene_j + np.array([i_mean]*cellxgene_j.shape[1]).T), index=adata.obs_names[cell_mask], columns=gene_j
        # )
        def custom_sigmoid(x, y, k=0.5, scale=1):
            # k: Hyperparameters to control the steepness
            return scale * (1 / (1 + np.exp(-k * (x - y))))

        return pd.DataFrame(
            custom_sigmoid(cellxgene_j, np.array([i_mean] * cellxgene_j.shape[1]).T), index=adata.obs_names[cell_mask],
            columns=gene_j
        )

    def returnScores(self, gene_i, gene_j, use_rep=None, groupby=None, cluster=None, cosg_scores=None):
        adata = self.adata
        # i the marker identified by COSG(index of results), j: the marker from reference(columns of results)
        marker_scores = self.returnGeneSimilarity(gene_i, gene_j, groupby=groupby, weighted=True, min_exp_pct=None)

        if cosg_scores is None:
            cosgAdata = adata[:, list(set(gene_i + gene_j))].copy()
            cosg.cosg(cosgAdata, groupby=groupby, n_genes_user=len(set(gene_i + gene_j)), reference="rest",
                      remove_lowly_expressed=False)
            cosg_scores = pd.Series(
                cosgAdata.uns['rank_genes_groups']['scores'][cluster],
                index=cosgAdata.uns['rank_genes_groups']['names'][cluster],
            )
        cosg_i = cosg_scores[gene_i]
        cosg_j = cosg_scores[gene_j]

        marker_scores = cosg_j.index.map(
            lambda x: 1 if x in cosg_i.index else marker_scores[x].sum() * (cosg_j[x] / cosg_i.sum())
        )

        exp_scores = self.returnExpressionScore(adata[adata.obs[groupby] == cluster], gene_i, gene_j, use_rep=use_rep)
        for col in exp_scores:
            if col in gene_i:
                exp_scores[col] = [1] * len(exp_scores)

        return (exp_scores.values.dot(marker_scores.values)) / len(gene_j)

    def returnMarkerGeneScoringPlot(
        self, cellIDs, annotation, markerDict, title, layer=None, use_raw=False,
        showNum=5, geneUsed=5, markerUsed=5
    ):
        # cellIDs, annotation: ID Series + selected or clusterName + annotation Series
        adata = self.adata
        if isinstance(annotation, str) and annotation == "selected":
            adata.obs["group_by"] = "not selected"
            adata.obs.loc[cellIDs, "group_by"] = "selected"
            groupby = "group_by"
            cluster = "selected"
        else:
            adata.obs["group_by"] = annotation
            groupby = "group_by"
            cluster = cellIDs

        # def qcMarkerDict(adata, markerDict, geneUsed=5):
        #     # markerDict = markerDict.copy()
        #     # total_genes = [gene for genes in markerDict.values() for gene in genes]
        #     # duplicated_genes = {gene for gene in total_genes if total_genes.count(gene) > 1}
        #     # markerDict = {key: [gene for gene in genes if gene not in duplicated_genes] for key, genes in markerDict.items()}
        # # qcMarkerDict
        if len(adata) > 100:
            min_cells = 50
        else:
            min_cells = int(len(adata) * 0.5)
        sc.pp.filter_genes(adata, min_cells=min_cells)

        delKey = []
        for key in markerDict:
            selectSeries = pd.Series(markerDict[key], index=markerDict[key])
            markerDict[key] = selectSeries[selectSeries.isin(adata.var_names)]
            if len(markerDict[key]) == 0:
                delKey.append(key)
        for key in delKey:
            del markerDict[key]

        # cosg_scores calculated
        cosg.cosg(adata, groupby=groupby, n_genes_user=markerUsed, reference="rest", remove_lowly_expressed=True,
                  expressed_pct=0.2)
        marker_cosg = pd.Series(
            adata.uns['rank_genes_groups']['scores'][cluster], index=adata.uns['rank_genes_groups']['names'][cluster],
        )
        gene_i = marker_cosg.index

        total_genes = list(set([gene for genes in markerDict.values() for gene in genes]))
        cosgAdata = adata[:, total_genes].copy()
        cosg.cosg(
            cosgAdata, groupby=groupby, n_genes_user=len(total_genes), reference="rest",
            remove_lowly_expressed=False
        )
        marker_cosg = pd.concat(
            [
                marker_cosg,
                pd.Series(
                    cosgAdata.uns['rank_genes_groups']['scores'][cluster],
                    index=cosgAdata.uns['rank_genes_groups']['names'][cluster],
                )
            ]
        )
        marker_cosg = marker_cosg[~marker_cosg.index.duplicated(keep='first')]

        # cluster gene_scores
        gene_scores = pd.DataFrame(None, columns=["score", "cluster"])

        for key in markerDict:
            gene_j = markerDict[key]
            gene_j = list(set(gene_j))

            # for unsorted marker gene list
            if geneUsed:
                gene_j = sorted(gene_j, key=lambda x: list(marker_cosg.index).index(x))[:geneUsed]
                # gene_j = sorted(gene_j, key=lambda x: list(marker_cosg.index).index(x))
                markerDict[key] = gene_j

            gene_score = self.returnScores(
                gene_i, gene_j, use_rep=None, groupby=groupby, cluster=cluster,
                cosg_scores=marker_cosg
            )
            gene_scores = pd.concat(
                [
                    gene_scores,
                    pd.DataFrame([gene_score, [key] * len(gene_score)], index=["score", "cluster"]).T
                ]
            )
            # gene_scores = pd.Series(gene_scores, name=key)

        plotDf = gene_scores
        plotOrder = plotDf.groupby("cluster").apply(
            lambda subDf: subDf["score"].median()
        ).sort_values(ascending=False).index

        # plotDf = plotDf.loc[plotDf["cluster"].isin(plotOrder[:showNum])]
        plotDf["score"] = plotDf["score"].astype(float)

        # # I don't know why the violin doesn't show in figure
        # figure = px.violin(
        #     plotDf, x="cluster", y="score", category_orders=plotOrder[:showNum],
        #     box=True,
        # )
        # figure.update_traces(box_visible=True)

        figure = go.Figure()
        for cluster in plotOrder:
            figure.add_trace(
                go.Violin(
                    x=[cluster] * (plotDf["cluster"] == cluster).sum(),
                    y=plotDf.loc[plotDf["cluster"] == cluster, "score"],
                    name=cluster, box_visible=True,
                    # meanline_visible=True
                )
            )

        figure.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center'
            ),
            legend=dict(
                font=dict(
                    size=10  # Set the font size of the legend
                ),
                itemsizing='constant'  # Ensure legend items are sized consistently
            ),
            xaxis=dict(
                tickangle=-45,
                tickvals=plotOrder
            ),
            yaxis=dict(
                title="Cell Scores",
            ),
        )

        figure = optFig(
            figure, cut_off_x=True,
            cutt_off_x_kwargs=dict(func=lambda x: x[:25] + "..." if len(x) > 25 else x)
        )

        return figure, plotDf, marker_cosg

    @staticmethod
    def returnCellStatFig(plotDf, histType, colorBy, selectedCells, fixedCells=None):
        if fixedCells is None:
            plotDf["CellClick_Category"] = splitIndex(plotDf.index, [fixedCells, selectedCells])
        else:
            plotDf["CellClick_Category"] = splitIndex(plotDf.index, [fixedCells, selectedCells])
        plotDf["CellClick_CellIDs"] = plotDf.index

        plotX = plotDf.columns[0]
        plotY = plotDf.columns[1]  # if plotX == plotY, "CellClick_Category" also correct
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

            # Create a figure with the right layout
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
                        font=dict(
                            size=10  # Set the font size of the legend
                        ),
                        itemsizing='constant',  # Ensure legend items are sized consistently
                        x=1.05, y=1, xanchor='left', yanchor='top'  # Position the legend slightly outside the plot
                    ),
                    hovermode="x",
                    # margin=dict(b=0, t=10, l=0, r=10)
                )
            )
            # Add the traces
            legend = []
            # t highlight or not highlight
            for i, t in enumerate(selectedMapping):  # selected, selected cluster
                # for j in selectedMapping[t]
                selectDf = plotDf.loc[plotDf[hueCol].isin(selectedMapping[t])]
                for j, col in enumerate(y_axis):
                    colDf = selectDf.loc[selectDf[plotY] == col]
                    barDf = colDf.value_counts(plotX)[x_axis]
                    barDf = barDf[barDf > 0]
                    if len(barDf) == 0:
                        continue

                    figure.add_bar(
                        x=barDf.index,
                        y=barDf,
                        # Set the right yaxis depending on the selected product (from enumerate)
                        yaxis=f"y{i + 1}",
                        # Offset the bar trace, offset needs to match the width
                        # For categorical traces, each category is spaced by 1
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
                        marker=marker[t],
                        customdata=[
                                       "{}@4712@{}@4712{}@4712@{}".format(plotX, plotY, t, col)
                                   ] * len(barDf)
                    )
                    if col not in legend:
                        legend.append(col)
            figure.update_xaxes(categoryorder='array', categoryarray=x_axis)

            # figure = px.histogram(
            #     plotDf, x=plotX, y=plotY, color=hueCol, category_orders=category_orders,
            # )
            # figure.update_traces(
            #     customdata=["{}@{}".format(plotX, hueCol)] * len(plotDf)
            # )
        else:
            # if table_type(plotDf[plotCol]) == "text":
            #     plotDf[plotCol] = plotDf[plotCol].astype(str)
            #     plotDf = plotDf.value_counts()
            #     plotDf.name = "Counts"
            #     plotDf = plotDf.reset_index()
            #
            #     norm = histType.split("_")[1]
            #     if norm == "Norm":
            #         for subCluster in plotDf[hueCol].unique():
            #             selectSeries = plotDf[hueCol] == subCluster
            #             plotDf.loc[selectSeries, "Ratio"] = plotDf.loc[selectSeries, "Counts"] / (
            #                 plotDf.loc[selectSeries, "Counts"].sum())
            #
            #     figure = px.histogram(
            #         plotDf, x=plotCol, y="Ratio" if norm == "Norm" else "Counts", color=hueCol,
            #         barmode="group", category_orders=category_orders
            #     )
            #     figure.update_layout(yaxis_title="Ratio" if norm == "Norm" else "Counts")
            #     figure.update_traces(
            #         customdata=["{}@{}".format(plotCol, hueCol)] * len(plotDf)
            #     )
            # else:
            #     figure = px.violin(
            #         plotDf, x=plotCol, color=hueCol,
            #         violinmode="group", category_orders=category_orders,
            #         points='all',
            #         custom_data=["CellClick_CellIDs"]
            #     )
            category_orders = {
                hueCol: sorted(plotDf[hueCol].unique())
            }
            # if table_type(plotDf[plotX]) == "text":
            #     category_orders[plotX] = sorted(plotDf[plotX].unique())
            figure = go.Figure()
            for name in category_orders[hueCol]:
                figure.add_trace(
                    go.Box(
                        x=plotDf.loc[plotDf[hueCol] == name, plotX],
                        y=plotDf.loc[plotDf[hueCol] == name, plotY],
                        # color=plotDf[hueCol],
                        # points=False,
                        # width=0.8,  scalemode="width",
                        name=name,
                    )
                )
            # figure = px.violin(
            #     plotDf, x=plotX, y=plotY, color=hueCol,
            #     category_orders=category_orders,
            #     # points='all',
            #     custom_data=["CellClick_CellIDs"]
            # )
            figure.update_layout(
                yaxis=dict(title=dict(text=plotY)),
            )

        figure.update_layout(
            dragmode='select',
        )
        figure = optFig(figure)
        return figure, plotDf

    @staticmethod
    def returnSankeyFig(historyDf):
        """
        return a sankey fig based a historyDf,
        :param historyDf: each col record the cluster distribution
        :return: sankey fig
        """
        import plotly.graph_objects as go

        # check whether to change the level of clusterRecord
        def clusterRecordLevelCheck(clusterDf, columns):
            checkSeries = clusterDf.T.apply(
                lambda row: not (row[columns[0]] == row[columns[1]] or row[columns[1]] == row[columns[2]])
            )
            return False if checkSeries.sum() == 0 else True

        plotCols = list(historyDf.columns)
        for colIndex in range(1, len(historyDf.columns) - 1):
            clusterDf = historyDf[historyDf.columns[colIndex - 1: colIndex + 2]]
            if clusterRecordLevelCheck(clusterDf, clusterDf.columns):
                continue
            else:
                plotCols.remove(historyDf.columns[colIndex])

        historyDf = historyDf[plotCols]
        sourceList = []
        targetList = []
        valueList = []
        # label = [sorted(list(historyDf[historyDf.columns[0]].unique()))]
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

            # targetRef = sorted(list(historyDf[subCols[1]].unique()))
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

        # refer to: https://plotly.com/python/sankey-diagram/
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labelList,
                color="blue"
            ),
            link=dict(
                source=sourceList,  # indices correspond to labels, eg A1, A2, A1, B1, ...
                target=targetList,
                value=valueList
            ))])
        fig = optFig(fig)
        return fig

    def write_adata(self, path, annotation):
        adata = self.adata
        adata.obs[annotation.columns] = annotation

        sc.write(filename=path, adata=adata)


if __name__ == '__main__':
    pass
