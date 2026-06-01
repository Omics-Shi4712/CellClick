#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: the callbacks about manager canvas
@version: 1.0.0
@file: callbacks_9_canvasManager.py.py
@time: 2023/11/7 17:15
"""
from callbacks.callbacks_8_cellTable import *


@callback(
    Output(
        {"type": "Div", "class": "canvas", "index": ALL},
        "style"
    ),
    Output(
        {"type": "Div", "class": "canvas", "function": "container", "index": ALL},
        "children"
    ),
    Output(
        {"type": "Div", "class": "canvas", "index": ALL},
        "className"
    ),
    inputs=dict(
        userSessionId=State("User Session ID", "data"),
        # in preprocessing card, labels with id raise Invalid prop for this component error
        QCParameters=(
            State(
                {
                    "card_name": "Preprocessing", "form_name": "QC",
                    "label_name": ALL, "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "QC",
                    "label_name": ALL, "type": ALL
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Preprocessing", "form_name": "QC",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        dataVisualizationParameters=(
            State(
                {
                    "card_name": "Data Visualization", "form_name": ALL,
                    "label_name": ALL, "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Data Visualization", "form_name": ALL,
                    "label_name": ALL, "type": ALL
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Data Visualization", "form_name": ALL,
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        geneAnalysisParameters=(
            State(
                {
                    "card_name": "Gene Analysis", "form_name": ALL,
                    "label_name": ALL, "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Gene Analysis", "form_name": ALL,
                    "label_name": ALL, "type": ALL
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Gene Analysis", "form_name": ALL,
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        evaluationValidationParameters=(
            State(
                {
                    "card_name": "Evaluation and Validation", "form_name": ALL,
                    "label_name": ALL, "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Evaluation and Validation", "form_name": ALL,
                    "label_name": ALL, "type": ALL
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Evaluation and Validation", "form_name": ALL,
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        clusterVisualizationParameters=(
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Cell Selection",
                    "label_name": ALL, "type": ALL
                },
                "id"
            ),
            State(
                {
                    "card_name": "Cell Reannotation", "form_name": "Cell Selection",
                    "label_name": ALL, "type": ALL
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Cell Reannotation", "form_name": "Cell Selection",
                    "label_name": ALL, "type": "Button"
                },
                "n_clicks"
            ),
        ),
        removeCanvasParameters=(
            Input({"type": "Button", "class": "canvas", "function": "close", "index": ALL}, "n_clicks"),
            State({"type": "Div", "class": "canvas", "index": ALL}, "style"),
            State({"type": "Div", "class": "canvas", "function": "container", "index": ALL}, "children"),
            State({"type": "Div", "class": "canvas", "index": ALL}, "className"),
        ),
        removedDataID=Input("Removed Data ID", "data"),
        reset=Input("reset", "n_clicks"),
    ),
)
def returnCanvas(
        userSessionId,
        QCParameters,
        dataVisualizationParameters, geneAnalysisParameters,
        evaluationValidationParameters,
        clusterVisualizationParameters,
        removeCanvasParameters, removedDataID,
        reset,
):
    def initCanvas():
        styles = [{"display": "none"}] * len(canvasManager.canvas)
        children = [None] * len(canvasManager.canvas)
        classNames = ["canvasDiv_default"] * len(canvasManager.canvas)

        # tableManger of CellClickManager is None, so use [] rather than tableManager.canvasCol
        return styles, children, classNames

    def removeCanvas(canvasPos, **kwargs):
        n_clicks, styles, children, classNames = removeCanvasParameters

        styles = styles[0: canvasPos] + styles[canvasPos + 1:] + [{"display": "none"}]
        children = children[0: canvasPos] + children[canvasPos + 1:] + [None]
        canvasManager.removeCanvas(canvasPos, **kwargs)

        classNames = classNames[0: canvasPos] + classNames[canvasPos + 1:] + ["canvasDiv_default"]
        return styles, children, classNames

    def removeData(removeData, **kwargs):
        n_clicks, styles, children, classNames = removeCanvasParameters
        for canvasPos, canvasData in zip(range(0, len(canvasManager.canvasIDs))[::-1], canvasManager.canvasIDs[::-1]):
            if removeData == canvasData:
                styles = styles[0: canvasPos] + styles[canvasPos + 1:] + [{"display": "none"}]
                children = children[0: canvasPos] + children[canvasPos + 1:] + [None]
                canvasManager.removeCanvas(canvasPos, **kwargs)

                classNames = classNames[0: canvasPos] + classNames[canvasPos + 1:] + ["canvasDiv_default"]
        return styles, children, classNames

    def addCanvas(canvasPos, figType, canvasParameters):
        canvas = canvasManager.addCanvas(
            figType=figType, canvasParameters=canvasParameters,
            dataID=userSessionId, pos=canvasPos,
        )

        styles = removeCanvasParameters[1]
        if styles[canvasPos]:
            styles[canvasPos]["display"] = "block"
        else:
            styles[canvasPos] = {"display": "block"}
        children = [dash.no_update if i != canvasPos else canvas for i in range(0, len(styles))]

        canvasDivClassName = canvasManager.canvasDivClassDict.get(figType, "canvasDiv_default")
        classNames = [dash.no_update if i != canvasPos else canvasDivClassName for i in range(0, len(styles))]

        return styles, children, classNames

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    canvasManager = cellClickManager.canvasManager
    # more work could be done to merge initCanvas, removeCanvas and addCanvas
    if (userSessionId is None) or (ctxIdStr == "") or (ctxIdStr == "reset"):
        return initCanvas()
    elif ctxIdStr == "Removed Data ID":
        return removeData(removeData=removedDataID)
    else:
        groupCellRecorder = cellClickManager.groupCellsRecorder
        ctxId = json.loads(ctxIdStr)

        if ctxId.get("class", None) == "canvas":
            pos = ctxId["index"]
            return removeCanvas(pos)
            # pass  # it seems can not pass current removed data ID
        # add canvas only with card_name
        elif "card_name" in ctxId:
            switchDict = {
                "Preprocessing": QCParameters,
                "Data Visualization": dataVisualizationParameters,
                # "Cluster Analysis": clusterAnalysisParameters,
                "Gene Analysis": geneAnalysisParameters,
                "Evaluation and Validation": evaluationValidationParameters,
                "Cell Reannotation": clusterVisualizationParameters,
            }

            formName = ctxId["form_name"]
            formContent = {"Data ID": userSessionId}
            inputIds, inputValues, n_clicks = switchDict[ctxId["card_name"]]
            for ID, value in zip(inputIds, inputValues):
                if ID["form_name"] == formName:
                    formContent[ID["label_name"]] = value

            if formName == "Marker Gene Identification":
                formContent["Group A Cells"] = groupCellRecorder.groupA
                formContent["Group B Cells"] = groupCellRecorder.groupB

            pos = canvasManager.returnFirstNonePos()  # the index of canvas in layout

            return addCanvas(pos, formName, formContent)
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))


if __name__ == '__main__':
    pass
