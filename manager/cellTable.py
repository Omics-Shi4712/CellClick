#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: manager to control cell table behavior
@version: 1.0.0
@file: cellTable.py
@time: 2023/11/7 17:21
"""
from dash.dash_table.Format import Format, Scheme, Trim


class CellTable(object):
    pageSize = 6
    startColNum = 5

    def __init__(self):
        self.metaData = None
        self.expressionData = None
        self.cacheData = None
        self.showData = None
        self.switcher = []

        # records the table attributes not shared between different table. usually column related
        self.records = {
            "metaData": {
                "showColumns": [],
                "filter_query": "",
                "sort_by": [],
            },
            "expressionData": {
                "showColumns": [],
                "filter_query": "",
                "sort_by": [],
            },
        }
        self.selectedCells = []
        self.canvasCol = []

    def initCellTable(self, metaData, expressionData):
        def preprocessTableData(data):
            columns = data.columns
            data["Cell ID"] = data.index
            data = data[["Cell ID"] + list(columns)]
            showColumns = list(data.columns[: self.startColNum])
            return data, showColumns

        self.metaData, self.records["metaData"]["showColumns"] = preprocessTableData(metaData)
        self.expressionData, self.records["expressionData"]["showColumns"] = preprocessTableData(expressionData)

    def modifyCellTabelData(self, dataType, refName, refValues):
        if dataType == "metaData":
            self.metaData[refName] = refValues
        elif dataType == "expression":
            self.expressionData[refName] = refValues
        self.setCacheData()

    def initSwitcher(self):
        self.switcher = ["metaData", False]

    def setSwitcher(self, description=None, isSelectedTable=None):
        if description is not None:
            self.switcher[0] = description
        if isSelectedTable is not None:
            self.switcher[1] = isSelectedTable

    def setRecords(self, key, value):
        description = self.switcher[0]
        if key not in self.records[description]:
            raise KeyError("Unvalidated key: {}".format(key))

        self.records[description][key] = value

    def returnRecords(self, key):
        description = self.switcher[0]
        if key not in self.records[description]:
            raise KeyError("Unvalidated key: {}".format(key))

        return self.records[description][key]

    def setSelectedCells(self, selectedCells):
        self.selectedCells = selectedCells

    def modifySelectedCells(self, selectedRows):
        pageContent = self.showData
        removeRowIds = set(range(0, len(pageContent))) - set(selectedRows)
        removeCellIds = set([pageContent["Cell ID"][remove_row] for remove_row in removeRowIds])
        addCellIds = set([pageContent["Cell ID"][select_row] for select_row in selectedRows])

        self.selectedCells = set(self.selectedCells) - set(removeCellIds)
        self.selectedCells = list(self.selectedCells | addCellIds)

    def returnData(self):
        description = self.switcher[0]
        return self.metaData if description == "metaData" else self.expressionData

    def modifyShowColumns(self, addColumn=None, removeColumn=None):
        showColumns = self.returnShowColumns()

        if addColumn:
            showColumns.append(addColumn)
        if removeColumn:
            if len(showColumns) > 2:   # it seems error layout when none columns display, and Cell ID is the index
                showColumns.remove(removeColumn)

        # self.setShowColumns(showColumns)
        self.setRecords("showColumns", showColumns)

    def returnTableColumns(self, annotationTypeDict):
        showColumns = self.returnRecords("showColumns")

        columns = [
            {
                "id": "Cell ID", "name": "Cell ID",
                "selectable": False, "deletable": False,
                "type": "text"
            }
        ]
        for column in showColumns:
            if column == "Cell ID":
                continue

            if column in annotationTypeDict:
                dataType = annotationTypeDict[column]
            else:
                # if column not in annotationTypeDict, it should be a gene name
                dataType = "numeric"

            columnDict = {
                "id": column, "name": column,
                "selectable": True, "deletable": True,
                "type": dataType
            }
            if dataType == "numeric":
                columnDict["format"] = Format(precision=4, scheme=Scheme.fixed, trim=Trim.yes)
            columns.append(columnDict)
        return columns

    def returnAddableColumns(self):
        data = self.returnData()
        columns = data.columns
        showColumns = self.returnRecords("showColumns")
        addableColumns = []
        for column in columns:
            if column not in showColumns:
                addableColumns.append(column)
        return addableColumns

    def returnRemoveAbleColumns(self):
        removeAbleColumns = self.returnRecords("showColumns").copy()
        removeAbleColumns.remove("Cell ID")
        return removeAbleColumns

    def setCacheData(self):
        tableData = self.returnData()

        isSelectedTable = self.switcher[1]
        if isSelectedTable:
            selectedSeries = tableData["Cell ID"].isin(self.selectedCells)
            tableData = tableData.loc[selectedSeries]

        sort_by = self.returnRecords("sort_by")
        tableData = tableData.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[col['direction'] == 'asc' for col in sort_by]
        )

        filter_query = self.returnRecords("filter_query")
        filtering_expressions = filter_query.split(' && ')
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = self.__split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                filter_value = float(filter_value)
                tableData = tableData.loc[getattr(tableData[col_name], operator)(filter_value)]
            elif operator == 'contains':
                tableData = tableData.loc[tableData[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                tableData = tableData.loc[tableData[col_name].str.startswith(filter_value)]
        if len(tableData) == 0:
            tableData.loc[0] = [None] * len(tableData.columns)
        self.cacheData = tableData
        self.setSelectedCells(set(self.selectedCells) & set(self.cacheData["Cell ID"]))

    def returnShowData(self, currentPage):
        self.showData = self.cacheData.iloc[currentPage * self.pageSize:(currentPage + 1) * self.pageSize]
        self.showData.index = range(0, min(self.pageSize, len(self.showData)))
        return self.showData[self.returnRecords("showColumns")].to_dict('records')

    def returnPageCount(self):
        cellNum = len(self.cacheData)
        if cellNum % self.pageSize == 0:
            pageCount = int(cellNum / self.pageSize)
        else:
            pageCount = int(cellNum / self.pageSize) + 1
        return pageCount

    def returnSelectedRows(self):
        selectedCells = self.selectedCells
        selectedCellsIndex = self.showData["Cell ID"].isin(selectedCells)
        return list(self.showData.index[selectedCellsIndex])

    def initCanvasCol(self):
        self.canvasCol = []

    def modifyCanvasCol(self, newSelected=[], addCols=[], removeCols=[]):
        removeCols = set(removeCols + list(set(self.canvasCol) - set(newSelected)))
        addCols = set(addCols + list(set(newSelected) - set(self.canvasCol)))

        if len(removeCols) + len(addCols) != 1:
            raise ValueError("There are unexpected col num to add and remove: {}, {}".format(addCols, removeCols))

        if len(addCols) == 1:
            addCol = list(addCols)[0]
            removeCol = False
            self.canvasCol.append(addCol)
        else:
            addCol = False
            removeCol = list(removeCols)[0]
            self.canvasCol.remove(removeCol)

        return addCol, removeCol

    # used by the table filter
    # https://dash.plotly.com/datatable/callbacks
    @staticmethod
    def __split_filter_part(filter_part):
        operators = [['ge ', '>='],
                     ['le ', '<='],
                     ['lt ', '<'],
                     ['gt ', '>'],
                     ['ne ', '!='],
                     ['eq ', '='],
                     ['contains '],
                     ['datestartswith ']]

        for operator_type in operators:
            for operator in operator_type:
                if operator in filter_part:
                    name_part, value_part = filter_part.split(operator, 1)
                    name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                    value_part = value_part.strip()
                    v0 = value_part[0]
                    if v0 == value_part[-1] and v0 in ("'", '"', '`'):
                        value = value_part[1: -1].replace('\\' + v0, v0)
                    else:
                        # try:
                        #     value = float(value_part)
                        # except ValueError:
                        value = value_part

                    # word operators need spaces after them in the filter string,
                    # but we don't want these later
                    return name, operator_type[0].strip(), value

        return [None] * 3

    # API may be deprecated in future
    def setFilter_query(self, filter_query):
        self.setRecords("filter_query", filter_query)

    def returnFilter_query(self):
        return self.returnRecords("filter_query")

    def setShowColumns(self, newShowColumns):
        self.setRecords("showColumns", newShowColumns)

    def returnShowColumns(self):
        return self.returnRecords("showColumns")


if __name__ == '__main__':
    pass
