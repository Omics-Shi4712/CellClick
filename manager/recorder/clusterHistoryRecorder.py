#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: The manager for clusterRecorder, which record the history and result of cell identification
@version: 1.0.0
@file: clusterHistoryRecorder.py
@time: 2023/11/7 14:33
"""
import pandas as pd

import scanpy as sc
# import leidenalg
# # ImportError: Please install the leiden algorithm:
# # `conda install -c conda-forge leidenalg` or `pip3 install leidenalg`.

from manager.recorder.recorder import Recorder


class ClusterHistoryRecorder(Recorder):

    def __init__(self):
        self.refCol = None
        self.level = None
        self.cellIDs = None
        self.records = None

    def init(self, adata, refExisted, refCol=None, cluster_method=None, resolution=None):
        if not refExisted:
            if cluster_method == "Leiden":
                sc.tl.leiden(adata, resolution=resolution, key_added="leiden_CellClick")
                refCol = "leiden_CellClick"
            elif cluster_method == "Louvain":
                sc.tl.louvain(adata, resolution=resolution, key_added="louvain_CellClick")
                refCol = "louvain_CellClick"
            else:
                raise ValueError("Unexpected cluster_method received: {}".format(cluster_method))

        self.refCol = refCol
        self.level = 0
        self.cellIDs = list(adata.obs_names)
        self.records = {
            "round_0": list(adata.obs[refCol])
        }
        return True

    def updateBasedRollback(self):
        if self.level == 0:
            return False
        else:
            del self.records["round_{}".format(self.level)]
            self.level -= 1
            return True

    def updateBasedOnReAnnotation(self, selectedCells, rawName, newName):

        # selectedCells, rawName, newName, n_clicks = reAnnotationParameters
        # newClusterRecordDict = clusterRecordDict

        currentLevel = self.level
        nextLevel = self.level + 1
        clusterDf = pd.DataFrame(
            self.records["round_{}".format(currentLevel)],
            index=self.cellIDs,
            columns=[currentLevel],
        )
        if rawName == "selected":
            selectSeries = clusterDf.index.isin(selectedCells)
        else:
            selectSeries = (clusterDf[currentLevel] == rawName)
        clusterDf[nextLevel] = clusterDf[currentLevel]
        clusterDf.loc[selectSeries, nextLevel] = newName

        self.level += 1
        self.records["round_{}".format(self.level)] = list(clusterDf[self.level])
        return True

    def updateBasedOnReClustering(self, value, prefix, cluster_method, resolution, adata, selectedCells):
        if value == "selected":
            cells = selectedCells
            if len(cells) == 0:
                cells = list(adata.obs_names)
        else:
            annotationSeries = self.returnAnnotation(self.level)
            cells = list(annotationSeries[annotationSeries == value].index)

        adata.obs["CellClick_annotation"] = self.records["round_{}".format(self.level)]
        adata.obs.loc[cells, "CellClick_annotation"] = prefix if prefix else value
        # for AttributeError: Can only use .cat accessor with a 'category' dtype
        adata.obs["CellClick_annotation"] = adata.obs["CellClick_annotation"].astype("category")

        if cluster_method == "Leiden":
            sc.tl.leiden(adata, resolution=resolution, key_added="leiden_CellClick")
            sc.tl.leiden(
                adata, resolution=resolution,
                # adata, resolution=0.68,
                restrict_to=("CellClick_annotation", [prefix if prefix else value]),
                random_state=4712,
                key_added="CellClick_annotation",
            )
        elif cluster_method == "Louvain":
            sc.tl.louvain(
                adata, resolution=resolution,
                # adata, resolution=0.68,
                restrict_to=("CellClick_annotation", [prefix if prefix else value]),
                random_state=4712,
                key_added="CellClick_annotation",
            )
        else:
            raise ValueError("Unexpected cluster_method received: {}".format(cluster_method))

        self.records["round_{}".format(self.level+1)] = list(adata.obs["CellClick_annotation"])
        self.level += 1
        return True

    def updateBasedOnMergeData(self, annotation):
        currentLevel = self.level
        nextLevel = self.level + 1

        clusterDf = pd.DataFrame(
            self.records["round_{}".format(currentLevel)],
            index=self.cellIDs,
            columns=[currentLevel],
        )
        clusterDf[nextLevel] = clusterDf[currentLevel]
        clusterDf.loc[annotation.index, nextLevel] = annotation

        self.level += 1
        self.records["round_{}".format(self.level)] = list(clusterDf[self.level])
        return True

    def returnAnnotation(self, level=None):
        if level is None:
            level = self.level

        assert level is not None, """None is invalid for level"""

        refAnnotation = self.records["round_{}".format(level)]
        refAnnotation = pd.Series(
            refAnnotation, index=self.cellIDs, name=self.refCol
        )
        refAnnotation = refAnnotation.astype("category")
        return refAnnotation

    def returnCellIDs(self, clusterName):
        refAnnotation = self.returnAnnotation(self.level)
        if clusterName not in refAnnotation.unique():
            raise ValueError("{} not in current cluster annotation, please check it!".format(clusterName))
        return list(refAnnotation.index[refAnnotation == clusterName])


if __name__ == '__main__':
    pass
