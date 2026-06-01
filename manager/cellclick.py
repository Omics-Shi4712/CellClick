#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: The manager for cellclick and manager
@version: 1.0.0
@file: cellclick.py
@time: 2023/10/17 20:10
"""
import os
import time

import pandas as pd

import scanpy as sc

from manager.recorder.annotationTypeRecorder import AnnotationTypeRecorder
from manager.recorder.clusterHistoryRecorder import ClusterHistoryRecorder
from manager.recorder.selectedCellsRecorder import SelectedCellsRecorder
from manager.recorder.fixedCellsRecorder import FixedCellsRecorder
from manager.recorder.groupCellsRecorder import GroupCellsRecorder
from manager.canvas import CanvasManager
from manager.cellTable import CellTable
from scripts.adataProcessor import AdataProcessor

from settings import CanvasManagerInitDict

recorders = [
    "annotationTypeRecorder", "clusterHistoryRecorder",
    "selectedCellsRecorder", "fixedCellsRecorder", "groupCellsRecorder",
    # "canvasManager", # It could not be record by CellMarker, but stored by CellClickManger
    "cellTable",
]


class CellClick(object):
    """
    receive adataDir as input and the adata should be saved earlier in previous process
    1) import, save adata with a session ID
    2) save/load data of adata and the store element, fixedcells, selectedcells and so on
    3) recover the table manager/canvas manager
    4) some basic plot function for CellMarker, dotplot, heatmap, embedding and so on?
    """
    def __init__(self, adataDir=None, ID=None, adata=None, adataSource="file"):
        if adataSource == "file":
            assert os.path.exists(adataDir), """No adata found in: {}""".format(adataDir)
            self._ID = ID
            self._filePath = adataDir
            # it will be replaced with a dir in unloaded stat to save memory
            self.adataProcessor = AdataProcessor(self._read())
        elif adataSource == "adata":
            self._ID = ID
            self._filePath = None
            self.adataProcessor = AdataProcessor(adata)
        else:
            raise ValueError("Error dataSource: {}.\nCorrect dataSource are 'file' and 'adata'.".format(adataSource))
        self.annotationTypeRecorder = AnnotationTypeRecorder()
        self.clusterHistoryRecorder = ClusterHistoryRecorder()

        self.selectedCellsRecorder = SelectedCellsRecorder()
        self.fixedCellsRecorder = FixedCellsRecorder()
        self.groupCellsRecorder = GroupCellsRecorder()

        self.cellTable = CellTable()
        self.preprocess()

    def preprocess(self):
        self.refreshAnnotationTypeRecorder(method="init", adata=self.returnAdata())

        expressionDf = sc.get.obs_df(self.returnAdata(), keys=list(self.returnAdata().var_names))
        self.cellTable.initCellTable(metaData=self.returnAdata().obs.copy(), expressionData=expressionDf.copy())
        # adata = self.returnAdata()
        pass

    def returnAdata(self):
        return self.adataProcessor.adata

    def __str__(self):
        return "<CellMarker>({})".format(self.getID())

    def _read(self):
        switchDict = {
            "rds": 0,
            "h5ad": sc.read,
        }
        import sys
        # print("stdout repr:", repr(sys.stdout))
        # print("stdout closed:", sys.stdout.closed)
        print(self._filePath)
        suffix = self._filePath.split(".")[0]
        readFunc = switchDict.get(suffix, sc.read)
        return readFunc(self._filePath)

    def getID(self):
        return self._ID

    def save(self, cellClickManager):
        # some progress to load history data
        #
        for recoder in recorders:
            self.__setattr__(recoder, cellClickManager.__getattribute__(recoder))

    def load(self):
        # some progress to load history data
        #
        pass

    def refreshAnnotationTypeRecorder(self, method, **kwargs):
        """
        modify annotation category based on parameters.
        :param method: the method called in recorder
        :param kwargs: [
            ("adata" for "init"), ("annotationValue" and “dataTypeValue” for "modification")
        :return: True if modification is performed else False
        """

        switchDict = {
            "init": self.annotationTypeRecorder.init,
            "modification": self.annotationTypeRecorder.modification,
            "add": self.annotationTypeRecorder.add,
        }
        assert method in switchDict.keys(), """Invalid method, valid is in: {}""".format(list(switchDict.keys()))

        switchDict[method](**kwargs)
        if method == "init":
            for annotationValue in self.annotationTypeRecorder.annotationTypeDict:
                dataTypeValue = self.annotationTypeRecorder.annotationTypeDict[annotationValue]
                self.returnAdata().obs[annotationValue] = self.returnAdata().obs[annotationValue].astype(
                    "category" if dataTypeValue == "text" else "float"
                )
            return True
        else:
            if method == "modification":
                annotationValue = kwargs.get("annotationValue")
                dataTypeValue = kwargs.get("dataTypeValue")
                if dataTypeValue == "text" and self.returnAdata().obs[annotationValue].dtype == "category":
                    self.returnAdata().obs[annotationValue] = self.returnAdata().obs[annotationValue].astype("category")
                    return True
                elif dataTypeValue == "numeric" and self.returnAdata().obs[annotationValue].dtype == "float":
                    self.returnAdata().obs[annotationValue] = self.returnAdata().obs[annotationValue].astype("float")
                    return True
                else:
                    return False
            elif method == "add":
                # wait cell clustering analysis
                # actually, a lock is more suitable method
                annotationValue = kwargs.get("annotationValue")
                import time
                while not (annotationValue in self.returnAdata().obs.columns):
                    time.sleep(1)
                return True
            else:
                raise ValueError("Invalid method: {}".format(method))

    def refreshClusterHistoryRecorder(self, method, **kwargs):
        switchDict = {
            "init": self.clusterHistoryRecorder.init,
            "rollback": self.clusterHistoryRecorder.updateBasedRollback,
            "reAnnotation": self.clusterHistoryRecorder.updateBasedOnReAnnotation,
            "reClustering": self.clusterHistoryRecorder.updateBasedOnReClustering,
            "mergeData": self.clusterHistoryRecorder.updateBasedOnMergeData,
        }
        assert method in switchDict.keys(), """Invalid method, valid is in: {}""".format(list(switchDict.keys()))
        if method == "init":
            kwargs["adata"] = self.returnAdata()
            result = switchDict[method](**kwargs)
            if not kwargs["refExisted"]:
                # adata is changed, so should update celltable
                expressionDf = sc.get.obs_df(self.returnAdata(), keys=list(self.returnAdata().var_names))
                self.cellTable.initCellTable(
                    metaData=self.returnAdata().obs.copy(), expressionData=expressionDf.copy()
                )
            return result
        elif method == "rollback":
            return switchDict[method](**kwargs)
        elif method == "reAnnotation":
            kwargs["selectedCells"] = self.selectedCellsRecorder.selectedCells
            return switchDict[method](**kwargs)
        elif method == "reClustering":
            kwargs["adata"] = self.returnAdata().copy()
            kwargs["selectedCells"] = self.selectedCellsRecorder.selectedCells
            return switchDict[method](**kwargs)
        elif method == "mergeData":
            return switchDict[method](**kwargs)
        else:
            pass

    def refreshSelectedCellsRecorder(self, method, **kwargs):
        switchDict = {
            "canvas": self.selectedCellsRecorder.updateBasedOnCanvas,
            "table": self.selectedCellsRecorder.updateBasedOnTable,
            "fixedSelection": self.selectedCellsRecorder.updateBasedOnFixedSelection,
        }

        assert method in switchDict.keys(), """Invalid method, valid is in: {}""".format(list(switchDict.keys()))
        if method == "canvas":
            kwargs["adata"] = self.returnAdata().copy()
            kwargs["clusterHistoryRecorder"] = self.clusterHistoryRecorder
            kwargs["fixedCells"] = self.fixedCellsRecorder.fixedCells
            return switchDict[method](**kwargs)
        elif method == "table":
            kwargs["tableCells"] = self.cellTable.cacheData["Cell ID"].to_list()
            return switchDict[method](**kwargs)
        elif method == "fixedSelection":
            kwargs["fixedCells"] = self.fixedCellsRecorder.fixedCells
            return switchDict[method](**kwargs)
        else:
            pass

    def refreshFixedCellsRecorder(self, method, **kwargs):
        switchDict = {
            "init": self.fixedCellsRecorder.init,
            "selected": self.fixedCellsRecorder.updateBasedOnSelectedCells,
            "modify": self.fixedCellsRecorder.updateBasedOnOperation,
        }
        assert method in switchDict.keys(), """Invalid method, valid is in: {}""".format(list(switchDict.keys()))
        if method == "init":
            return switchDict[method](**kwargs)
        elif method == "selected":
            kwargs["selectedCells"] = self.selectedCellsRecorder.selectedCells
            return switchDict[method](**kwargs)
        elif method == "modify":
            kwargs["selectedCells"] = self.selectedCellsRecorder.selectedCells
            return switchDict[method](**kwargs)
        else:
            # raise ValueError("Error key passed, valid keys are {}".format(",".join(list(switchDict.keys()))))
            pass

    def refreshGroupCellsRecorder(self, method, **kwargs):
        switchDict = {
            "selected": self.groupCellsRecorder.updateBasedOnSelected,
            "rest": self.groupCellsRecorder.updateBasedOnRest,
            "none": self.groupCellsRecorder.updateBasedOnNone,
            "all": self.groupCellsRecorder.updateBasedOnAll
        }
        if method not in switchDict:
            kwargs["clusterName"] = method
            if self.clusterHistoryRecorder.refCol and self.clusterHistoryRecorder.refCol == kwargs["annotation"]:
                kwargs["selectSeries"] = self.clusterHistoryRecorder.returnAnnotation()
            else:
                kwargs["selectSeries"] = self.returnAdata().obs[kwargs["annotation"]]
            return self.groupCellsRecorder.updateBasedOnAnnotation(**kwargs)
        else:
            if method == "selected":
                kwargs["selectedCells"] = self.selectedCellsRecorder.selectedCells
                return switchDict[method](**kwargs)
            elif method == "rest":
                kwargs["adata"] = self.returnAdata().copy()
                return switchDict[method](**kwargs)
            elif method == "none":
                return switchDict[method](**kwargs)
            elif method == "all":
                kwargs["adata"] = self.returnAdata().copy()
                return switchDict[method](**kwargs)
            else:
                pass


class CellClickManager(object):
    """
    1) Modify current data
    2) The pipe for Dash and Adata
    """
    modeList = ["app", "jupyter"]
    mode = "app"  # a tag to show the mode to running CellClick

    def __init__(self, max_data_number, dataDir):
        self._max_data_number = max_data_number
        self._dataDir = dataDir
        self.CellClick = {}
        self.cacheAdata = {}
        self.CellClickID = []
        self.currentData = None

        self.annotationTypeRecorder = None
        self.clusterHistoryRecorder = None

        self.selectedCellsRecorder = None
        self.fixedCellsRecorder = None
        self.groupCellsRecorder = None

        self.cellTable = None

        self.canvasManager = CanvasManager(**CanvasManagerInitDict)

    def __len__(self):
        return len(self.CellClick)

    @classmethod
    def __setMode__(cls, mode):
        assert mode in cls.modeList, """Error mode: {}""".format(mode)
        cls.mode = mode

    def returnDataDir(self):
        return self._dataDir

    def add(self, ID, suffix="h5ad", dataDir=None):
        assert ID is not None, """ID can't be None"""
        if dataDir is None:
            dataDir = self._dataDir

        if len(self) < self._max_data_number:
            if ID not in self.CellClickID:
                self.CellClick[ID] = CellClick(
                    adataDir=os.path.join(dataDir, "{}.{}".format(ID, suffix)), ID=ID,
                    adata=None, adataSource="file"
                )
                self.CellClickID.append(ID)
                if len(self) == 1:
                    self.load(ID)
            else:
                pass
        else:
            adataList = [str(self.CellClick[ID]) for ID in self.CellClick]
            # self.remove(ID)
            raise ValueError("Max data has been loaded: {}".format(", ".join(adataList)))

    def add_adata(self, adata, ID, to="cache"):
        if to == "CellClick":
            if len(self) < self._max_data_number:
                if ID not in self.CellClickID:
                    self.CellClick[ID] = CellClick(
                        adataDir=None, ID=ID,
                        adata=adata, adataSource="adata"
                    )
                    self.CellClickID.append(ID)
                    if len(self) == 1:
                        self.load(ID)
                else:
                    pass
            else:
                adataList = [str(self.CellClick[ID]) for ID in self.CellClick]
                # self.remove(ID)
                raise ValueError("Max data has been loaded: {}".format(", ".join(adataList)))
        elif to == "cache":
            import anndata
            assert isinstance(adata, anndata.AnnData), """Error object type for adata: {}""".format(type(adata))
            self.cacheAdata[ID] = adata
        else:
            raise ValueError("Error to: {}".format(to))

    def remove(self, ID):
        assert ID is not None, """ID can't be None"""
        if ID not in self.CellClick:
            raise KeyError("None data found for {}".format(ID))

        if self.currentData == ID:
            if len(self) > 1:
                for key in self.CellClick:
                    if key != ID:  # the first ID not equal to ID
                        nextID = key
                        break
                self.load(nextID)
            else:
                cellClick = self.get(self.currentData)
                cellClick.save(self)
                self.currentData = None

        del self.CellClick[ID]
        self.CellClickID.remove(ID)

        if len(self.CellClick) == 0:
            for recorder in recorders:
                self.__setattr__(recorder, None)

    def reset(self):
        # IDList = list(self.CellClick.keys())
        # for ID in IDList:
        #     if ID != self.currentData:
        #         self.remove(ID)

        # self.remove(self.currentData)
        self.CellClick = {}
        self.cacheAdata = {}
        self.CellClickID = []
        self.currentData = None

        self.annotationTypeRecorder = None
        self.clusterHistoryRecorder = None

        self.selectedCellsRecorder = None
        self.fixedCellsRecorder = None
        self.groupCellsRecorder = None

        self.cellTable = None
        self.canvasManager = CanvasManager(**CanvasManagerInitDict)

    def get(self, ID):
        assert ID is not None, """ID can't be None"""
        if ID not in self.CellClick:
            raise KeyError("None data found for {}".format(ID))

        return self.CellClick[ID]

    def returnAdata(self):
        return self.CellClick[self.currentData].returnAdata()

    def load(self, ID):
        assert ID is not None, """ID can't be None"""
        if ID == self.currentData:  # no need to load current data
            return True
        if self.currentData:  # False means CellMarker has none data
            cellClick = self.get(self.currentData)
            cellClick.save(self)

        cellClick = self.get(ID)
        cellClick.load()
        for recoder in recorders:
            self.__setattr__(recoder, cellClick.__getattribute__(recoder))

        self.currentData = ID

    def refreshRecoder(self, recoder, method, **kwargs):
        """
        refresh the recoder
        :param recoder:recoder to refresh
        :param method: method the refresh recoder
        :param kwargs: parameters to call method
        :return: True if recoder is refreshed else False
        """

        assert recoder in recorders, """Invalid recoder, valid recoder is in: {}""".format(recorders)
        # only allowed the modification on current data
        cellClick = self.get(self.currentData)

        switchDict = {
            "annotationTypeRecorder": cellClick.refreshAnnotationTypeRecorder,
            "clusterHistoryRecorder": cellClick.refreshClusterHistoryRecorder,
            "selectedCellsRecorder": cellClick.refreshSelectedCellsRecorder,
            "fixedCellsRecorder": cellClick.refreshFixedCellsRecorder,
            "groupCellsRecorder": cellClick.refreshGroupCellsRecorder,
        }
        return switchDict[recoder](method=method, **kwargs)


if __name__ == '__main__':
    pass
