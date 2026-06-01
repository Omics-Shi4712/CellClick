#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: The manager for cell selection, which record the fixed cells
@version: 1.0.0
@file: fixedCellsRecorder.py
@time: 2023/11/7 21:34
"""

from manager.recorder.recorder import Recorder


class FixedCellsRecorder(Recorder):
    def __init__(self):
        self.fixedCells = []

    def init(self):
        self.fixedCells = []
        return True

    def updateBasedOnSelectedCells(self, selectedCells):
        self.fixedCells = selectedCells
        return True

    def updateBasedOnOperation(self, selectedCells, operation):
        fixedCells = self.fixedCells
        if operation == "add":
            self.fixedCells = list(set(fixedCells) | set(selectedCells))
        elif operation == "remove":
            self.fixedCells = list(set(fixedCells) - set(selectedCells))
        elif operation == "inter":
            self.fixedCells = list(set(fixedCells) & set(selectedCells))
        else:
            raise ValueError("Unexpected operation received: {}".format(operation))
        return True

if __name__ == '__main__':
    pass
