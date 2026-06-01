#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description:
@version: 1.0.0
@file: callbacks_8_cellTable.py
@time: 2023/11/7 17:16
"""
from callbacks.callbacks_7_reAnnotation import *


# @callback(
#     Output(
#         {
#             "class": "Cells Table", "group": "container",
#             "type": "Div"
#         },
#         "style"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "container",
#             "type": "Table"
#         },
#         "style_table"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "switcher",
#             "type": "Button", "label": ALL
#         },
#         "active"
#     ),
#     inputs=dict(
#         userSessionId=Input("User Session ID", "data"),
#         switcher=Input(
#             {
#                 "class": "Cells Table", "group": "switcher",
#                 "type": "Button", "label": ALL
#             },
#             "n_clicks"
#         ),
#         selectedButtonActive=State(
#             {
#                 "class": "Cells Table", "group": "switcher",
#                 "type": "Button", "label": "Selected"
#             },
#             "active"
#         ),
#         containerStyle=(
#             State(
#                 {
#                     "class": "Cells Table", "group": "container",
#                     "type": "Div"
#                 },
#                 "style"
#             ),
#             State(
#                 {
#                     "class": "Cells Table", "group": "container",
#                     "type": "Table",
#                 },
#                 "style_table"
#             ),
#         ),
#     ),
# )
# def returnCellsTableClass(userSessionId, switcher, selectedButtonActive, containerStyle):
#     divStyle, tableStyle = containerStyle
#     if userSessionId is None:
#         divStyle["visibility"] = "hidden"
#         tableStyle["display"] = "none"
#         switcherActive = [True, False, False]
#     else:
#         ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
#
#         divStyle["visibility"] = "visible"
#         tableStyle["display"] = "block"
#         if ctxIdStr == "User Session ID":
#             switcherActive = [True, False, False]
#         else:
#             ctxId = json.loads(ctxIdStr)
#             if ctxId["group"] == "switcher":
#                 if ctxId["label"] == "Meta":
#                     switcherActive = [True, False,  dash.no_update]
#                 elif ctxId["label"] == "Expression":
#                     switcherActive = [False, True,  dash.no_update]
#                 else:
#                     switcherActive = [dash.no_update, dash.no_update, not selectedButtonActive]
#             else:
#                 raise ValueError("Unexpected input received: {}".format(ctxIdStr))
#
#     return divStyle, tableStyle, switcherActive
#
#
# @callback(
#     Output(
#         {
#             "class": "Cells Table", "group": "container", "type": "Table"
#         },
#         "data"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "container", "type": "Table"
#         },
#         "columns"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "container", "type": "Table"
#         },
#         'sort_by'
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "container", "type": "Table"
#         },
#         'filter_query'
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "container", "type": "Table"
#         },
#         "page_current"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "container", "type": "Table"
#         },
#         "page_count"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "controller",
#             "type": "Dropdown", "label": "Add Column"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "controller",
#             "type": "Dropdown", "label": "Add Column"
#         },
#         "options"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "controller",
#             "type": "Dropdown", "label": "Remove Column"
#         },
#         "value"
#     ),
#     Output(
#         {
#             "class": "Cells Table", "group": "controller",
#             "type": "Dropdown", "label": "Remove Column"
#         },
#         "options"
#     ),
#     inputs=dict(
#         userSessionId=Input("User Session ID", "data"),
#         tableShowContentParameters=(
#             Input("refresh_clusterHistoryRecorder", "data"),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "switcher",
#                     "type": "Button", "label": ALL
#                 },
#                 "n_clicks"
#             ),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "container", "type": "Table"
#                 },
#                 'sort_by'
#             ),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "container", "type": "Table"
#                 },
#                 'filter_query'
#             ),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "container", "type": "Table"
#                 },
#                 "page_current"
#             ),
#         ),
#         modifyColumnParameters=(
#             Input("refresh_annotationTypeRecorder", "data"),
#             State(
#                 {
#                     "class": "Cells Table", "group": "controller",
#                     "type": "Dropdown", "label": "Add Column"
#                 },
#                 "value"
#             ),
#             State(
#                 {
#                     "class": "Cells Table", "group": "controller",
#                     "type": "Dropdown", "label": "Remove Column"
#                 },
#                 "value"
#             ),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "controller",
#                     "type": "Button", "label": "Add Column"
#                 },
#                 "n_clicks"
#             ),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "controller",
#                     "type": "Button", "label": "Remove Column"
#                 },
#                 "n_clicks"
#             ),
#         ),
#         selectionParameters=(
#             Input(
#                 {
#                     "class": "Cells Table", "group": "controller",
#                     "type": "Button", "label": "Select All"
#                 },
#                 "n_clicks"
#             ),
#             Input(
#                 {
#                     "class": "Cells Table", "group": "controller",
#                     "type": "Button", "label": "Unselect All"
#                 },
#                 "n_clicks"
#             ),
#         ),
#         refresh_selectedCellsRecorder=Input("refresh_selectedCellsRecorder", "data"),
#     ),
#     prevent_initial_call=True
# )
# def returnCellsTable(
#         userSessionId,
#         tableShowContentParameters,
#         modifyColumnParameters,
#         refresh_selectedCellsRecorder,
#         selectionParameters
# ):
#     if userSessionId is None:
#         raise PreventUpdate
#     else:
#         tableManager = cellClickManager.cellTable
#         annotationTypeDict = cellClickManager.annotationTypeRecorder.annotationTypeDict
#         clusterHistoryRecorder = cellClickManager.clusterHistoryRecorder
#         selectedCells = cellClickManager.selectedCellsRecorder.selectedCells
#
#         # read input
#         refresh_clusterHistoryRecorder, switcherClick, sort_by, filter_query, page_current = tableShowContentParameters
#         refresh_annotationTypeRecorder, addColumn, removeColumn, addClick, removeClick = modifyColumnParameters
#         # selectedCells, selectClick, unSelectClick, resetClick, tableSelected = selectedRowParameters
#
#         # set default output
#         # used to create data, so not set dash.no_update as default value
#         page_current = page_current
#         filter_query = filter_query
#         sort_by = sort_by
#         data, columns, page_count, selected_rows = [dash.no_update]*4
#         removeColumnValue, removeColumnOptions = [dash.no_update]*2
#         addColumnValue, addColumnOptions = [dash.no_update]*2
#
#         def updateCellsTable():
#             tableManager.setCacheData()
#             return tableManager.returnShowData(0), 0, tableManager.returnPageCount()
#
#         def returnColumnsControllerDropdown(removable=True):
#             optionsList = tableManager.returnRemoveAbleColumns() if removable else tableManager.returnAddableColumns()
#             value = optionsList[0] if len(optionsList) > 0 else None
#             options = returnDropdownOptions(optionsList)
#             return value, options
#
#         if len(dash.callback_context.triggered) > 1:
#             ctxIdStrs = returnCtxIdStr(dash.callback_context)
#             if (
#                 # add ref by CellClick
#                 (('refresh_clusterHistoryRecorder' in ctxIdStrs) and ('refresh_annotationTypeRecorder' in ctxIdStrs)) or
#                 # initial the table
#                 "User Session ID" in ctxIdStrs
#             ):
#                 tableManager.initSwitcher()
#                 tableManager.setSelectedCells(selectedCells)
#                 data, page_current, page_count = updateCellsTable()
#                 columns = tableManager.returnTableColumns(annotationTypeDict)
#                 # selected_rows = tableManager.returnSelectedRows()
#                 addColumnValue, addColumnOptions = returnColumnsControllerDropdown(False)
#                 removeColumnValue, removeColumnOptions = returnColumnsControllerDropdown(True)
#             elif 'refresh_selectedCellsRecorder' in ctxIdStrs:
#                 for ctxIdStr in ctxIdStrs:
#                     try:
#                         ctxId = json.loads(ctxIdStr)
#                     except json.decoder.JSONDecodeError:
#                         continue
#
#                     if ctxId["group"] == "controller" and ctxId["label"] in ["Select All", "Unselect All"]:
#                         if ctxId["label"] == "Select All":
#                             tableManager.setSelectedCells(list(tableManager.cacheData.index))
#                         else:  # ctxId["label"] == "Unselect All"
#                             tableManager.setSelectedCells([])
#                         data, page_current, page_count = updateCellsTable()
#                         break
#         else:
#             ctxIdStr = returnCtxIdStr(dash.callback_context, index=0)
#             if ctxIdStr == "refresh_selectedCellsRecorder":
#                 tableManager.setSelectedCells(selectedCells)
#             #     selected_rows = tableManager.returnSelectedRows()
#             elif ctxIdStr == "refresh_annotationTypeRecorder":
#                 if tableManager.switcher[0] == "metaData":
#                     columns = tableManager.returnTableColumns(annotationTypeDict)
#                 else:
#                     raise PreventUpdate
#             elif ctxIdStr == "refresh_clusterHistoryRecorder":
#                 if clusterHistoryRecorder.refCol:
#                     refValues = clusterHistoryRecorder.returnAnnotation(clusterHistoryRecorder.level)
#                     refName = clusterHistoryRecorder.refCol
#                     tableManager.modifyCellTabelData("metaData", refName, refValues)
#                     data = tableManager.returnShowData(page_current)
#
#                 addColumnValue, addColumnOptions = returnColumnsControllerDropdown(False)
#                 removeColumnValue, removeColumnOptions = returnColumnsControllerDropdown(True)
#             else:
#                 ctxId = json.loads(ctxIdStr)
#                 if ctxId["group"] == "switcher":
#                     switcherLabel = ctxId["label"]
#                     if switcherLabel == "Selected":
#                         tableManager.setSwitcher(isSelectedTable=not tableManager.switcher[1])
#                     else:
#                         description = "metaData" if switcherLabel == "Meta" else "expressionData"
#                         tableManager.setSwitcher(description=description)
#                         # because we can't show the filter_query by filter_query attribute,
#                         # we don't decided to save the filter_query
#                         # when switch the table type, we set the filter_query and sort_by as "" and []
#                         tableManager.setRecords("filter_query", "")
#                         tableManager.setRecords("sort_by", [])
#                         filter_query = tableManager.returnRecords("filter_query")
#                         sort_by = tableManager.returnRecords("sort_by")
#
#                         addColumnValue, addColumnOptions = returnColumnsControllerDropdown(False)
#                         removeColumnValue, removeColumnOptions = returnColumnsControllerDropdown(True)
#                     # tableManager.modifySelectedCells(tableSelected)
#
#                     data, page_current, page_count = updateCellsTable()
#                     columns = tableManager.returnTableColumns(annotationTypeDict)
#                     # selected_rows = tableManager.returnSelectedRows()
#                 elif ctxId["group"] == "container":
#                     triggeredValue = dash.callback_context.triggered[0]["prop_id"].split(".")[1]
#                     if triggeredValue == "sort_by":
#                         # tableManager.modifySelectedCells(tableSelected)
#                         tableManager.setRecords("sort_by", sort_by)
#                         # actually, page count is not need to update
#                         data, page_current, page_count = updateCellsTable()
#                         # selected_rows = tableManager.returnSelectedRows()
#                     elif triggeredValue == "filter_query":
#                         # tableManager.modifySelectedCells(tableSelected)
#                         tableManager.setRecords("filter_query", filter_query)
#
#                         data, page_current, page_count = updateCellsTable()
#                         # selected_rows = tableManager.returnSelectedRows()
#                     elif triggeredValue == "page_current":
#                         # tableManager.modifySelectedCells(tableSelected)
#
#                         data = tableManager.returnShowData(page_current)
#                         # selected_rows = tableManager.returnSelectedRows()
#                     else:
#                         raise ValueError("Unexpected table input received: {}".format(triggeredValue))
#                 elif ctxId["group"] == "controller":
#                     if ctxId["label"] in ["Add Column", "Remove Column"]:
#                         if ctxId["label"] == "Add Column":
#                             if addColumn is not None:
#                                 tableManager.modifyShowColumns(addColumn=addColumn)
#                         else:
#                             if removeColumn is not None:
#                                 tableManager.modifyShowColumns(removeColumn=removeColumn)
#                         data = tableManager.returnShowData(page_current)
#                         columns = tableManager.returnTableColumns(annotationTypeDict)
#
#                         addColumnValue, addColumnOptions = returnColumnsControllerDropdown(False)
#                         removeColumnValue, removeColumnOptions = returnColumnsControllerDropdown(True)
#                     # elif ctxId["label"] in ["Select All", "Unselect All"]:
#                     #     if ctxId["label"] == "Select All":
#                     #         tableManager.setSelectedCells(list(tableManager.cacheData.index))
#                     #     else: # ctxId["label"] == "Unselect All"
#                     #         tableManager.setSelectedCells([])
#                     #     data, page_current, page_count = updateCellsTable()
#                     else:
#                         raise ValueError("Unexpected controller input received: {}".format(ctxId["label"]))
#                 else:
#                     raise ValueError("Unexpected input received: {}".format(ctxIdStr))
#
#         return (
#             data, columns, sort_by, filter_query, page_current, page_count,
#             # selected_rows,
#             addColumnValue, addColumnOptions, removeColumnValue, removeColumnOptions
#         )
#
