#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: callbacks_2_dataSettings.py
@time: 2023/10/17 22:00
"""
import time

import anndata
import dash

from callbacks.callbacks_1_collapsedCard import *

import os
import uuid
import base64

@callback(
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Data Source", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Data Source", "type": "Dropdown"
        },
        "options"
    ),

    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Local Data", "type": "Label"
        },
        "style"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Local Data", "type": "Button"
        },
        "style"
    ),

    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "History Data", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "History Data", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "History Data", "type": "Label"
        },
        "style"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "History Data", "type": "Dropdown"
        },
        "style"
    ),

    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Current Data", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Current Data", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Current Data", "type": "Label"
        },
        "style"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Current Data", "type": "Dropdown"
        },
        "style"
    ),

    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Object Name", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Object Name", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Object Name", "type": "Label"
        },
        "style"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Upload",
            "label_name": "Object Name", "type": "Dropdown"
        },
        "style"
    ),
    inputs=dict(
        dataSourceValue=Input(
            {
                "card_name": "Data Settings", "form_name": "Upload",
                "label_name": "Data Source", "type": "Dropdown"
            },
            "value"
        ),
        upload=(
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Local Data", "type": "Label"
                },
                "style"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Local Data", "type": "Button"
                },
                "style"
            ),
        ),
        history=(
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "History Data", "type": "Label"
                },
                "style"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "History Data", "type": "Dropdown"
                },
                "style"
            ),
        ),
        current=(
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Current Data", "type": "Label"
                },
                "style"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Current Data", "type": "Dropdown"
                },
                "style"
            ),
        ),
        adataObject=(
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Object Name", "type": "Label"
                },
                "style"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Object Name", "type": "Dropdown"
                },
                "style"
            ),
        ),
        refSubmit=Input("refresh_clusterHistoryRecorder", "data"),
        cellClickAlert=Input("CellClickAlert", "children"),  # a signal about data change,
    )
)
def returnUploadForm(dataSourceValue, upload, history, current, adataObject, refSubmit, cellClickAlert):
    if dataSourceValue == None:
        dataSourceValue = "Local Data"
    uploadLabelStyle, uploadInputStyle = [{} if style is None else style for style in upload]
    historyLabelStyle, historyInputStyle = [{} if style is None else style for style in history]
    currentLabelStyle, currentInputStyle = [{} if style is None else style for style in current]
    adataNameLabelStyle, adataNameInputStyle = [{} if style is None else style for style in adataObject]

    ctxIDStr = returnCtxIdStr(dash.callback_context, index=0)
    if ctxIDStr == "" or dataSourceValue == "Local Data":  # merge tow situation
        dataSourceValue = "Local Data"
        if cellClickManager.mode == "app":
            dataSourceOptions = [
                "Local Data", "History Data",
                # "Current Data"
            ]
        elif cellClickManager.mode == "jupyter":
            dataSourceOptions = [
                "Local Data", "History Data",
                # "Current Data",
                "Anndata Object"
            ]
        else:
            raise ValueError("Error Value was passed for CellClick mode")
        dataSourceOptions = returnDropdownOptions(dataSourceOptions, sort=False)

        uploadLabelStyle["display"] = "block"
        uploadInputStyle["display"] = "block"

        historyLabelStyle["display"] = "none"
        historyInputStyle["display"] = "none"
        historyInputValue = dash.no_update
        historyInputOptions = dash.no_update

        currentLabelStyle["display"] = "none"
        currentInputStyle["display"] = "none"
        currentInputValue = dash.no_update
        currentInputOptions = dash.no_update

        adataNameLabelStyle["display"] = "none"
        adataNameInputStyle["display"] = "none"
        adataNameInputValue = dash.no_update
        adataNameInputOptions = dash.no_update
    else:
        dataSourceOptions = dash.no_update
        if dataSourceValue == "History Data":
            uploadLabelStyle["display"] = "none"
            uploadInputStyle["display"] = "none"

            historyLabelStyle["display"] = "block"
            historyInputStyle["display"] = "block"
            dataDir = cellClickManager.returnDataDir()
            fileNames = os.listdir(dataDir)
            fileNames = [fileName.split(".")[0] for fileName in fileNames]
            if len(fileNames) == 0:
                fileNames = ["None"]
            historyInputOptions = returnDropdownOptions(fileNames)
            historyInputValue = fileNames[0]

            currentLabelStyle["display"] = "none"
            currentInputStyle["display"] = "none"
            currentInputValue = dash.no_update
            currentInputOptions = dash.no_update

            adataNameLabelStyle["display"] = "none"
            adataNameInputStyle["display"] = "none"
            adataNameInputValue = dash.no_update
            adataNameInputOptions = dash.no_update
        elif dataSourceValue == "Current Data":
            uploadLabelStyle["display"] = "none"
            uploadInputStyle["display"] = "none"

            historyLabelStyle["display"] = "none"
            historyInputStyle["display"] = "none"
            historyInputValue = dash.no_update
            historyInputOptions = dash.no_update

            currentLabelStyle["display"] = "block"
            currentInputStyle["display"] = "block"
            clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
            if clusterHistoryRecorder and clusterHistoryRecorder.refCol:
                currentInputOptions = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
                currentInputOptions = sorted(currentInputOptions.unique())
                currentInputValue = "selected"
                currentInputOptions = returnDropdownOptions(currentInputOptions, ["selected"])
            else:
                currentInputValue = "None"
                currentInputOptions = returnDropdownOptions(["None"])

            adataNameLabelStyle["display"] = "none"
            adataNameInputStyle["display"] = "none"
            adataNameInputValue = dash.no_update
            adataNameInputOptions = dash.no_update
        elif dataSourceValue == "Anndata Object":
            uploadLabelStyle["display"] = "none"
            uploadInputStyle["display"] = "none"

            historyLabelStyle["display"] = "none"
            historyInputStyle["display"] = "none"
            historyInputValue = dash.no_update
            historyInputOptions = dash.no_update

            currentLabelStyle["display"] = "none"
            currentInputStyle["display"] = "none"
            currentInputValue = dash.no_update
            currentInputOptions = dash.no_update

            adataNameLabelStyle["display"] = "block"
            adataNameInputStyle["display"] = "block"

            adataNameInputOptions = cellClickManager.cacheAdata.keys()
            adataNameInputValue, adataNameInputOptions = returnDropdown(adataNameInputOptions)
        else:
            raise ValueError("Error Value was passed for dataSourceValue： {}".format(dataSourceValue))

    dataSource = [dataSourceValue, dataSourceOptions]
    upload = [uploadLabelStyle, uploadInputStyle]
    history = [historyInputValue, historyInputOptions, historyLabelStyle, historyInputStyle]
    current = [currentInputValue, currentInputOptions, currentLabelStyle, currentInputStyle]
    adataObject = [adataNameInputValue, adataNameInputOptions, adataNameLabelStyle, adataNameInputStyle]
    return dataSource + upload + history + current + adataObject


# save file into server, more details can be seen from:
# https://docs.faculty.ai/user-guide/apps/examples/dash_file_upload_download.html
@callback(
    Output("CellClickAlert", "children"),
    Output("CellClickAlert", "is_open"),
    Output("CellClickAlert", "color"),
    inputs=dict(
        newData=(
            Input(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Local Data", "type": "Upload"
                },
                "filename"
            ),
            Input(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Local Data", "type": "Upload"
                },
                "contents"
            ),
        ),
        cacheData=(
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Data Source", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "History Data", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Current Data", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Object Name", "type": "Dropdown"
                },
                "value"
            ),
            Input(
                {
                    "card_name": "Data Settings", "form_name": "Upload",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
        ),
        currentUserSessionID=State("User Session ID", "data"),
    ),
    prevent_initial_call=True,
)
def update_output(newData, cacheData, currentUserSessionID):
    """Save uploaded files and generate cellclick object"""

    def save_file(name, content):
        """Decode and store a file uploaded with Plotly Dash."""
        data = content.encode("utf8").split(b";base64,")[1]
        with open(os.path.join(dataDir, name), "wb") as fp:
            fp.write(base64.decodebytes(data))
        return os.path.join(dataDir, name)

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
    dataDir = cellClickManager.returnDataDir()
    try:
        ctxId = json.loads(ctxIdStr)
    except json.JSONDecodeError:
        return "Errors in trans ctxId to json: {}".format(ctxIdStr), True, "danger"

    dataSource, historyData, currentData, objectName, n_clicks = cacheData
    if (ctxId["label_name"] == "Local Data") or (ctxId["label_name"] == "Submit" and dataSource == "Local Data"):
        timeArray = time.localtime(time.time())
        sessionID = time.strftime("%Y%m%d%H%M%S", timeArray)
        uploaded_filename, uploaded_file_content = newData

        suffix = os.path.splitext(uploaded_filename)[-1][1:]
        save_file("{}.{}".format(sessionID, suffix), uploaded_file_content)
        try:
            cellClickManager.add(sessionID, suffix=suffix)

        except ValueError as e:
            os.remove(os.path.join(dataDir, "{}.{}".format(sessionID, suffix)))
            raise ValueError(e)
        alertInfo = "Data has been uploaded successfully, whose CellClick ID is {}".format(sessionID)
    elif ctxId["label_name"] == "Submit":
        if dataSource == "History Data" and historyData != "None":
            fileNames = os.listdir(dataDir)
            for fileName in fileNames:
                if fileName.startswith(historyData):
                    suffix = fileName.split(".")[-1]
                    break
            cellClickManager.add(historyData, suffix=suffix)
            alertInfo = "Data has been uploaded successfully, whose CellClick ID is {}".format(historyData)
        elif dataSource == "Current Data" and currentData != "None":
            selectedCellsRecorder = cellClickManager.selectedCellsRecorder
            clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
            adata = cellClickManager.returnAdata()

            # when upload data with current data, clusterHistoryRecorder has been set
            if currentData == "selected":
                cellIDs = selectedCellsRecorder.selectedCells
            else:
                cellIDs = clusterHistoryRecorder.returnCellIDs(currentData)
            newAdata = adata[cellIDs].copy()

            annotation = clusterHistoryRecorder.returnAnnotation()[cellIDs]
            newAdata.obs[clusterHistoryRecorder.refCol] = annotation

            # fileName = "{}_{}".format(cellClickManager.currentData, currentData)
            # newAdata.write(os.path.join(tmpDir, "{}.h5ad".format(fileName)))
            # cellClickManager.add(fileName, suffix="h5ad", dataDir=tmpDir)
            # alertInfo = "Data has been uploaded successfully, whose CellClick ID is {}".format(fileName)

            dataID = "{}_{}".format(cellClickManager.currentData, currentData)
            cellClickManager.add_adata(newAdata, ID=dataID, to="CellClick")
            alertInfo = "Data has been uploaded successfully, whose CellClick ID is {}".format(dataID)
        elif dataSource == "Anndata Object":
            adata = cellClickManager.cacheAdata[objectName]

            cellClickManager.add_adata(adata, ID=objectName, to="CellClick")
            alertInfo = "Data has been uploaded successfully, whose CellClick ID is {}".format(objectName)
        else:
            if dataSource == "History Data":
                alertInfo = "Error input for {} with {}".format(dataSource, historyData)
            else:
                alertInfo = "Error input for {} with {}".format(dataSource, currentData)
            return alertInfo, True, "danger"
    else:
        return "No file name or content is uploaded!", True, "danger"

    # # init cell table
    # adata = cellClickManager.returnAdata()
    # expressionDf = pd.DataFrame(adata.X, columns=adata.var.index, index=adata.obs.index)
    # tableManager.initCellTable(metaData=adata.obs.copy(), expressionData=expressionDf)

    print("Data has been uploaded!")
    return alertInfo, True, "success"


@callback(
    Output(
        {
            "card_name": "Data Settings", "form_name": "Remove",
            "label_name": "Data ID", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Change",
            "label_name": "Data ID", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Remove",
            "label_name": "Data ID", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Change",
            "label_name": "Data ID", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Remove",
            "label_name": "Current ID", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Change",
            "label_name": "Current ID", "type": "Input"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Remove",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Change",
            "label_name": "Submit", "type": "Button"
        },
        "disabled"
    ),
    Output("User Session ID", "data"),
    Output("Current Data ID", "children"),
    Output("Removed Data ID", "data"),
    # Output("Introduction", "style"),
    inputs=dict(
        removeGroup=(
            Input(
                {
                    "card_name": "Data Settings", "form_name": "Remove",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Remove",
                    "label_name": "Data ID", "type": "Dropdown"
                },
                "value"
            ),
        ),
        changeGroup=(
            Input(
                {
                    "card_name": "Data Settings", "form_name": "Change",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Change",
                    "label_name": "Data ID", "type": "Dropdown"
                },
                "value"
            ),
        ),
        uploadSignal=Input("CellClickAlert", "children"),  # a signal to change CellMarker
        refresh_UserSessionIDRecorder=Input("refresh_UserSessionIDRecorder", "data"),
        currentUserSessionID=State("User Session ID", "data"),
        reset=Input("reset", "n_clicks"),
        # introduction=State("Introduction", "style"),
        preprocessced=Input("PreprocessingAlert", "children"),
    ),
    prevent_initial_call=True,
)
def returnUserSessionID(
    removeGroup, changeGroup,
    uploadSignal, refresh_UserSessionIDRecorder,
    currentUserSessionID, reset,
    # introduction,
    preprocessced
):
    # callbacks merging return remove/change form and return userSessionID
    def returnRemoveAndChangeForm():
        IDList = cellClickManager.CellClickID
        option = returnDropdownOptions(IDList)
        value = IDList[0] if len(IDList) > 0 else None
        disabled = True if len(option) <= 1 else False
        return [value, value], [option, option], disabled, disabled

    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)

    ctxId = {}
    if ctxIdStr == "CellClickAlert":
        pass
    elif ctxIdStr == "refresh_UserSessionIDRecorder":
        pass
    elif ctxIdStr == "reset":
        if cellClickManager.currentData is not None:
            cellClickManager.reset()
        else:
            raise PreventUpdate
    elif ctxIdStr == "PreprocessingAlert":
        pass
    else:
        ctxId = json.loads(ctxIdStr)
        if ctxId["form_name"] == "Change":
            loadID = changeGroup[1]
            cellClickManager.load(loadID)
        elif ctxId["form_name"] == "Remove":
            cellClickManager.remove(removeGroup[1])
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))

    if currentUserSessionID != cellClickManager.currentData:
        userSessionID = cellClickManager.currentData
    else:
        if ctxIdStr == "PreprocessingAlert":
            userSessionID = cellClickManager.currentData
        else:
            userSessionID = dash.no_update

    values, options, removeDisabled, changeDisabled = returnRemoveAndChangeForm()
    if ctxId.get("form_name", None) == "Remove":
        removedDataID = removeGroup[1]
    else:
        removedDataID = dash.no_update

    # if cellClickManager.currentData is not None:
    #     introduction["display"] = "none"
    # else:
    #     introduction["display"] = "block"

    return (
        values + options +
        [cellClickManager.currentData, cellClickManager.currentData] +
        [removeDisabled, changeDisabled] +
        [userSessionID, "Current Data ID is: {}".format(cellClickManager.currentData)] + [removedDataID]
        # + [introduction]
    )


@callback(
    Output(
        {
            "card_name": "Data Settings", "form_name": "Annotation Type",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Annotation Type",
            "label_name": "Annotation", "type": "Dropdown"
        },
        "options"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Annotation Type",
            "label_name": "Data Type", "type": "Dropdown"
        },
        "value"
    ),
    Output(
        {
            "card_name": "Data Settings", "form_name": "Annotation Type",
            "label_name": "Data Type", "type": "Dropdown"
        },
        "options"
    ),
    Output("refresh_annotationTypeRecorder", "data"),
    inputs=dict(
        userSessionId=Input("User Session ID", "data"),
        annotationParameters=(
            Input(
                {
                    "card_name": "Data Settings", "form_name": "Annotation Type",
                    "label_name": "Annotation", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Data Settings", "form_name": "Annotation Type",
                    "label_name": "Data Type", "type": "Dropdown"
                },
                "value"
            )
        ),
        referenceSubmitParameters=(
            Input(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Submit", "type": "Button"
                },
                "n_clicks"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Preprocessed", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Reference", "type": "Dropdown"
                },
                "value"
            ),
            State(
                {
                    "card_name": "Preprocessing", "form_name": "Cell Clustering",
                    "label_name": "Method", "type": "Dropdown"
                },
                "value"
            ),
            # State(
            #     {
            #         "card_name": "Preprocessing", "form_name": "Cell Clustering",
            #         "label_name": "Resolution", "type": "Slider"
            #     },
            #     "value"
            # ),
        ),
        submit=Input(
            {
                "card_name": "Data Settings", "form_name": "Annotation Type",
                "label_name": "Submit", "type": "Button"
            },
            "n_clicks"
        ),
        refresh=State("refresh_annotationTypeRecorder", "data"),
    ),
    prevent_initial_call=True
)
def returnAnnotationTypeForm(userSessionId, referenceSubmitParameters, annotationParameters, submit, refresh):
    ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)

    if ctxIdStr == "User Session ID":
        if userSessionId is None:
            raise PreventUpdate
        else:
            # init annotation and data type dropdown component and annotationTypeDict
            annotationTypeRecoder = cellClickManager.annotationTypeRecorder
            annotations = list(annotationTypeRecoder.annotationTypeDict.keys())

            if len(annotations) == 0:
                annotationValue = None
                annotationOptions = returnDropdownOptions(annotations)

                dataTypeValue = None
                dataTypeOptions = []
            else:
                annotationValue = annotations[0]
                annotationOptions = returnDropdownOptions(annotations)

                dataTypeValue = annotationTypeRecoder.annotationTypeDict[annotationValue]
                dataTypeOptions = [{"label": "Category", "value": "text"}, {"label": "Number", "value": "numeric"}]
            refresh = dash.no_update
    else:
        ctxId = json.loads(ctxIdStr)
        annotationValue, dataTypeValue = annotationParameters
        if ctxId["type"] == "Dropdown":
            annotationTypeRecoder = cellClickManager.annotationTypeRecorder
            dataTypeValue = annotationTypeRecoder.annotationTypeDict[annotationValue]

            clusterHistoryRecord = cellClickManager.clusterHistoryRecorder
            if annotationValue == clusterHistoryRecord.refCol:
                dataTypeOptions = [{"label": "Category", "value": "text"}]
            else:
                dataTypeOptions = [{"label": "Category", "value": "text"}, {"label": "Number", "value": "numeric"}]

            annotationOptions = dash.no_update
            refresh = dash.no_update
        elif ctxId["type"] == "Button":
            if ctxId["form_name"] == "Cell Clustering":
                n_clicks, processedBy, refName, method = referenceSubmitParameters
                if processedBy == "Custom":
                    if cellClickManager.refreshRecoder(
                        recoder="annotationTypeRecorder", method="modification",
                        annotationValue=refName, dataTypeValue="text"
                    ):
                        refresh = refresh + 1
                    else:
                        refresh = dash.no_update

                    if annotationValue == refName:
                        annotationValue, annotationOptions = [dash.no_update] * 2
                        dataTypeValue = "text"
                        dataTypeOptions = [{"label": "Category", "value": "text"}]
                    else:
                        annotationValue, annotationOptions, dataTypeValue, dataTypeOptions = [dash.no_update] * 4
                else:

                    if cellClickManager.refreshRecoder(
                        recoder="annotationTypeRecorder", method="add",
                        annotationValue="{}_CellClick".format(method.lower()), dataTypeValue="text"
                    ):
                        refresh = refresh + 1
                    else:
                        refresh = dash.no_update
                    annotationTypeRecoder = cellClickManager.annotationTypeRecorder
                    annotations = list(annotationTypeRecoder.annotationTypeDict.keys())

                    if annotationValue is None:
                        annotationValue, annotationOptions = returnDropdown(annotations, value=annotationValue)
                        dataTypeOptions = [{"label": "Category", "value": "text"}]
                        dataTypeValue = annotationTypeRecoder.annotationTypeDict[annotationValue]
                    else:
                        annotationValue, annotationOptions = returnDropdown(annotations, value=annotationValue)
                        dataTypeValue, dataTypeOptions = [dash.no_update] * 2

            elif ctxId["form_name"] == "Annotation Type":
                # modify annotationTypeDict according annotation and data type value
                if cellClickManager.refreshRecoder(
                    recoder="annotationTypeRecorder", method="modification",
                    annotationValue=annotationValue, dataTypeValue=dataTypeValue
                ):
                    refresh = refresh + 1
                else:
                    refresh = dash.no_update

                annotationValue, annotationOptions, dataTypeValue, dataTypeOptions = [dash.no_update] * 4
            else:
                raise ValueError("Unexpected form input received: {}".format(ctxId["form_name"]))
        else:
            raise ValueError("Unexpected input received: {}".format(ctxIdStr))

    return annotationValue, annotationOptions, dataTypeValue, dataTypeOptions, refresh


