#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: The manager for cell selection, which record the selected cells
@version: 1.0.0
@file: selectedCellsRecorder.py
@time: 2023/11/7 21:34
"""
import pandas as pd
import scanpy as sc

from manager.recorder.recorder import Recorder
from scripts.utils import splitIndex


class SelectedCellsRecorder(Recorder):
    def __init__(self):
        self.selectedCells = []

    def updateBasedOnCanvas(
            self, selection, ctxId,
            adata, clusterHistoryRecorder, fixedActive,
            # cellStatParameters,
            fixedCells
    ):
        graphType, graphIndex = ctxId["class"], ctxId["index"]
        # replace PreventUpdate with False to achieve prevent update
        if selection is None:
            # when new a graph, the selected data is None
            return False
        selectCells = selection["points"]
        if graphType == "cellEmbedding" or graphType == "cellSelection":
            self.selectedCells = [p['customdata'] for p in selectCells]
            return True
        elif graphType == "cellStat":
            if len(selectCells) == 0:
                return False

            if isinstance(selectCells[0]["customdata"], list):
                self.selectedCells = [p['customdata'][0] for p in selectCells]
                return True
            else:
                bars = []
                for p in selectCells:
                    if len(p["pointNumbers"]) > 0:  # a valid selection for a bar
                        # bars.append([p["x"], p["curveNumber"]])   # plotCol_value, hueCol_index
                        bars.append([p["x"] + p["customdata"].split("@4712@")])  # x, y, selected
                if len(bars) == 0:
                    return False

                plotCol, hueCol = selectCells[0]['customdata'].split("@")
                refDf = sc.get.obs_df(
                    adata, keys=[plotCol, hueCol] if hueCol and hueCol != "CellClick_Category" else [plotCol],
                    use_raw=False
                )
                if plotCol == clusterHistoryRecorder.refCol:
                    refDf[plotCol] = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
                refDf[plotCol] = refDf[plotCol].astype(str)

                if hueCol == "CellClick_Category":
                    fixedCells = fixedCells if fixedActive else None
                    currentSelectedCells = self.selectedCells
                    refDf["CellClick_Category"] = splitIndex(refDf.index, [fixedCells, currentSelectedCells])
                if plotCol == clusterHistoryRecorder.refCol:
                    refDf[plotCol] = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
                refDf[hueCol] = refDf[hueCol].astype(str)

                histIDs, figureDatas, selectedCells = cellStatParameters
                index = None
                for histID, histIndex in zip(histIDs, range(0, len(histIDs))):
                    if histID["index"] == ctxId["index"]:
                        index = histIndex
                        break
                if index is None:
                    raise ValueError("Not found the histogram graph with index: {}".format(ctxId["index"]))
                figureData = figureDatas[index]

                selectSeries = pd.Series([False]*len(refDf), index=refDf.index)
                for bar in bars:
                    plotCol_value, hueCol_index = bar
                    # legendgroup also works?
                    hueCol_value = figureData['data'][hueCol_index]["name"]
                    selectSeries = selectSeries | ((refDf[plotCol] == plotCol_value) & (refDf[hueCol] == hueCol_value))
                self.selectedCells = list(refDf.loc[selectSeries].index)
                return True
        else:
            raise ValueError("Unexpected class received: {}".format(graphType))

    def updateBasedOnTable(self, operation, tableCells):
        if operation == "Select All":
            self.selectedCells = tableCells
        elif operation == "Unselect All":
            self.selectedCells = list(set(self.selectedCells) - set(tableCells))
        else:
            raise ValueError("Unexpected button operation was passed: {}".format(operation))
        return True

    def updateBasedOnFixedSelection(self, fixedActive, fixedCells):
        if fixedActive:
            return False

        self.selectedCells = fixedCells
        return True


if __name__ == '__main__':
    pass
