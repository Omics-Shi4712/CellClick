#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: The manager for cell selection, which record the selected cells in different group
@version: 1.0.0
@file: groupCellsRecorder.py
@time: 2023/11/8 13:13
"""
from manager.recorder.recorder import Recorder


class GroupCellsRecorder(Recorder):

    def __init__(self):
        self.groupA = []
        self.groupB = []

    def updateBasedOnSelected(self, group, selectedCells, **kwargs):
        if group == "Group B" and not selectedCells:  # for group A, None selectedCells means select all cells
            raise ValueError("There is none cells selected in Group B")

        if group == "Group A":
            self.groupA = selectedCells
        else:
            self.groupB = selectedCells
        return True

    def updateBasedOnRest(self, adata, **kwargs):  # group B only
        if len(self.groupA) == 0:
            return False
        cellIDs = adata.obs_names
        self.groupB = list(cellIDs[~ cellIDs.isin(self.groupA)])
        return True

    def updateBasedOnAll(self, adata, **kwargs):
        self.groupA = list(adata.obs_names)
        return True

    def updateBasedOnNone(self, **kwargs):  # group B only
        self.groupB = []
        return True

    def updateBasedOnAnnotation(self, group, clusterName, selectSeries, **kwargs):
        if group == "Group A":
            self.groupA = list(selectSeries[selectSeries == clusterName].index)
        else:
            self.groupB = list(selectSeries[selectSeries == clusterName].index)
        return True


if __name__ == '__main__':
    pass
