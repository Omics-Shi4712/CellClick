#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: manager to control canvas behavior
@version: 1.0.0
@file: canvas.py
@time: 2023/11/7 17:19
"""


class CanvasManager(object):
    """
    there are (maxCanvas + 1) canvas in canvas component,
    so the pos of canvas component is equal to the pos - 1 of canvas manager
    """
    canvasDivClassDict = {
        "QC": "canvasDiv_total",
        "Gene Dot": "canvasDiv_total",
        "Cell Stat": "canvasDiv_total",
        "Marker Gene Scoring": "canvasDiv_total",
        "Marker Gene Identification": "canvasDiv_total",
        "Marker Gene Evaluation": "canvasDiv_total_higher",
        "Annotation Evaluation": "canvasDiv_total",
        "Cell Selection": "canvasDiv_total",
    }

    def __init__(self, rowNum=3, colNum=2):
        assert colNum in [1, 2, 3, 4, 6, 12], """colNum should be one of {}""".format("\t".join([1, 2, 3, 4, 6, 12]))
        self.__maxCanvas = rowNum * colNum
        self.canvasNum = 0
        self.__canvasIndex = 0
        self.canvas = [None]*self.__maxCanvas
        self.canvasIDs = [None]*self.__maxCanvas
        # self.histogramRecord = [None]*self.__maxCanvas
        self.posOffset = 0  # the offset of canvas component and canvas manager

    def returnIndex(self):
        return self.canvasIndex

    def returnFirstNonePos(self):
        if self.canvasNum == self.__maxCanvas:
            raise ValueError("There is no position without canvas")

        for i in range(0, self.__maxCanvas):
            if self.canvas[i] is None:
                return i + self.posOffset
        return False

    def __returnCanvas(self, figType, canvasParameters):
        from dash import dcc
        from apps.template import returnIDDict, returnFigCard

        def initQCGraph(**kwargs):
            attributes = kwargs["Attributes"]
            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={"Attributes": attributes},
                    id=returnIDDict(
                        **{
                            "class": "QC", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="QC", index=canvasNum,
                    dataID=dataID, attributes=attributes,
                ),
            ]
            return canvasChildren

        def initGeneEmbeddingGraph(**kwargs):
            geneName = kwargs["Gene Name"]
            dataID = kwargs["Data ID"]
            embedding = kwargs.get("Embedding", None)
            clusters = kwargs.get("Clusters", None)
            canvasChildren = [
                dcc.Store(
                    data={"Gene Name": geneName, "Embedding": embedding, "Clusters": clusters},
                    id=returnIDDict(
                        **{
                            "class": "geneEmbedding", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="geneEmbedding", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initGeneDotGraph(**kwargs):
            geneName = kwargs["Gene Name"]
            dataID = kwargs["Data ID"]
            annotation = kwargs["Annotation"]
            canvasChildren = [
                dcc.Store(
                    data={"Gene Name": geneName, "Annotation": annotation},
                    id=returnIDDict(
                        **{
                            "class": "geneDot", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="geneDot", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initCellEmbeddingGraph(**kwargs):
            Embedding = kwargs["Embedding"]
            Annotation = kwargs["Annotation"]
            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={"Embedding": Embedding, "Annotation": Annotation},
                    id=returnIDDict(
                        **{
                            "class": "cellEmbedding", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="cellEmbedding", index=canvasNum,
                    dataID=dataID, dropdownLabels=["Embedding", "Annotation"],
                ),
            ]

            return canvasChildren

        def initCellStatGraph(**kwargs):
            dataID = kwargs["Data ID"]
            x_Annotation = kwargs["x_Annotation"]
            y_Annotation = kwargs["y_Annotation"]
            canvasChildren = [
                dcc.Store(
                    data={"x_Annotation": x_Annotation, "y_Annotation": y_Annotation},
                    id=returnIDDict(
                        **{
                            "class": "cellStat", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="cellStat", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initMarkerGeneIdentificationGraph(**kwargs):
            annotation = kwargs["Annotation"]
            groupACells = kwargs["Group A Cells"]
            groupAName = kwargs["Group A"]
            groupBCells = kwargs["Group B Cells"]
            groupBName = kwargs["Group B"]

            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={
                        "Annotation": annotation,
                        "Group A Name": groupAName, "Group B Name": groupBName,
                        "Group A": groupACells, "Group B": groupBCells,
                    },
                    id=returnIDDict(
                        **{
                            "class": "markerGeneIdentification", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="markerGeneIdentification", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initMarkerGeneEvaluationGraph(**kwargs):
            markerSource = kwargs["Marker Source"]
            species = kwargs["Species"]
            clusterName = kwargs["Cluster Name"]
            geneNum = kwargs["Gene Number"]

            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={
                        "Marker Source": markerSource, "Species": species,
                        "Cluster Name": clusterName, "Gene Number": geneNum,
                    },
                    id=returnIDDict(
                        **{
                            "class": "markerGeneEvaluation", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="markerGeneEvaluation", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initExpressionSimilaritySearchGraph(**kwargs):
            annotation = kwargs["Annotation"]
            geneName = kwargs["Gene Name"]

            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={
                        "Annotation": annotation, "Gene Name": geneName,
                    },
                    id=returnIDDict(
                        **{
                            "class": "expressionSimilaritySearch", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="expressionSimilaritySearch", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initAnnotationEvaluationGraph(**kwargs):
            cellCluster = kwargs["Cell Cluster"]
            geneNumber = kwargs["Gene Number"]
            embedding = kwargs["Embedding"]

            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={
                        "Cell Cluster": cellCluster, "Gene Number": geneNumber,
                        "Embedding": embedding,
                    },
                    id=returnIDDict(
                        **{
                            "class": "annotationEvaluation", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="annotationEvaluation", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initMarkerGeneScoringGraph(**kwargs):
            markerSource = kwargs["Marker Source"]
            sourceName = kwargs["Source Name"]
            cellCluster = kwargs["Cell Cluster"]
            geneNum = kwargs["Gene Number"]

            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={
                        "Marker Source": markerSource, "Source Name": sourceName,
                        "Cell Cluster": cellCluster, "Gene Number": geneNum,
                        "Annotation History": {},
                    },
                    id=returnIDDict(
                        **{
                            "class": "markerGeneScoring", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="markerGeneScoring", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initCellSelectionGraph(**kwargs):
            # returnDropdownLine(label_name="Embedding", input_name="Embedding"),
            # returnDropdownLine(label_name="Annotation", input_name="Annotation"),
            # returnDropdownLine(label_name="Table Content", input_name="Table Content"),
            embedding = kwargs["Embedding"]
            annotation = kwargs["Annotation"]
            tableContent = kwargs["Table Content"]

            dataID = kwargs["Data ID"]
            canvasChildren = [
                dcc.Store(
                    data={
                        "Embedding": embedding, "Annotation": annotation,
                        "Table Content": tableContent,
                    },
                    id=returnIDDict(
                        **{
                            "class": "cellSelection", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="cellSelection", index=canvasNum,
                    dataID=dataID,
                ),
            ]
            return canvasChildren

        def initVisualizationGraph(**kwargs):
            # method = kwargs["Graph Type"]
            dataID = kwargs["Data ID"]
            clusterName = kwargs["Cluster Name"]
            # if method == "History":
            #     defaultParameters = dict(Method=method)
            # else:
            #     defaultParameters = dict(Method=method, Embedding=embedding)
            canvasChildren = [
                dcc.Store(
                    data={"Cluster Name": clusterName},
                    id=returnIDDict(
                        **{
                            "class": "visualization", "group": "graph",
                            "type": "Store", "index": canvasNum
                        }
                    )
                ),
                returnFigCard(
                    figType="visualization", index=canvasNum,
                    dataID=dataID, dropdownLabels=["embedding", "level"],
                ),
            ]
            return canvasChildren

        canvasNum = self.__canvasIndex
        switchDict = {
            "QC": initQCGraph,
            "Gene Embedding": initGeneEmbeddingGraph,
            "Gene Dot": initGeneDotGraph,
            "Cell Embedding": initCellEmbeddingGraph,
            "Cell Stat": initCellStatGraph,
            "Marker Gene Identification": initMarkerGeneIdentificationGraph,
            "Marker Gene Evaluation": initMarkerGeneEvaluationGraph,
            "Expression Similarity Search": initExpressionSimilaritySearchGraph,
            "Marker Gene Scoring": initMarkerGeneScoringGraph,
            "Annotation Evaluation": initAnnotationEvaluationGraph,
            "Cell Selection": initCellSelectionGraph,
            "Visualization": initVisualizationGraph,
        }
        canvas = switchDict[figType](**canvasParameters)
        return canvas

    def addCanvas(self, figType, canvasParameters, dataID, pos=None):
        if not pos:
            try:
                pos = self.returnFirstNonePos()
            except ValueError:
                raise ValueError("Max canvas has been shown: {}".format(self.__maxCanvas))
        else:
            if self.canvas[pos - self.posOffset] is not None:
                raise ValueError("Can't add new canvas to a position with canvas: {}".format(pos))
        pos = pos - self.posOffset

        canvas = self.__returnCanvas(figType, canvasParameters)
        self.canvas[pos] = canvas
        self.canvasIDs[pos] = dataID

        self.__canvasIndex += 1
        self.canvasNum += 1

        # if figType == "Histogram":
        #     self.histogramRecord[pos] = canvasParameters["colName"]
        return canvas

    # def returnHistogramPos(self, colName):
    #     return self.histogramRecord.index(colName) + self.posOffset

    def removeCanvas(self, pos):
        pos = pos - self.posOffset
        self.canvas = self.canvas[0: pos] + self.canvas[pos+1:] + [None]
        self.canvasIDs = self.canvasIDs[0: pos] + self.canvasIDs[pos+1:] + [None]
        # self.histogramRecord = self.histogramRecord[0: pos] + self.histogramRecord[pos + 1:] + [None]
        self.canvasNum -= 1

    def initCanvas(self):
        self.canvas = [None] * self.__maxCanvas
        self.__canvasIndex = 0
        self.canvasNum = 0
        self.canvasIDs = [None] * self.__maxCanvas
        # self.histogramRecord = [None]*self.__maxCanvas
        self.posOffset = 0  # the offset of canvas component and canvas manager


if __name__ == '__main__':
    pass
