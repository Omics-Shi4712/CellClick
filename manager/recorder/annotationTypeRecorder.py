#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: the manager for annotation type recorder, which recorder the annotation type
@version: 1.0.0
@file: annotationTypeRecorder.py
@time: 2023/11/7 14:46
"""
from manager.recorder.recorder import Recorder

from scripts.utils import table_type


class AnnotationTypeRecorder(Recorder):
    def __init__(self):
        self.annotationTypeDict = None

    def init(self, adata):
        annotations = adata.obs.columns
        annotationTypeDict = {}
        for annotation in annotations:
            annotationTypeDict[annotation] = table_type(adata.obs[annotation])
        self.annotationTypeDict = annotationTypeDict

    def add(self, annotationValue, dataTypeValue):
        self.annotationTypeDict[annotationValue] = dataTypeValue

    def modification(self, annotationValue, dataTypeValue):
        self.annotationTypeDict[annotationValue] = dataTypeValue

    def returnTextAnnotation(self):
        textAnnotationList = []
        for annotation in self.annotationTypeDict:
            if self.annotationTypeDict[annotation] == "text":
                textAnnotationList.append(annotation)
        return None if len(textAnnotationList) == 0 else textAnnotationList[0], textAnnotationList

    def returnTextAnnotationDropdown(self, currentAnnotation=None):
        textAnnotationList = []
        for annotation in self.annotationTypeDict:
            if self.annotationTypeDict[annotation] == "text":
                textAnnotationList.append(annotation)

        if len(textAnnotationList) == 0:
            return None, textAnnotationList
        elif currentAnnotation is None:
            return textAnnotationList[0], textAnnotationList
        elif currentAnnotation not in textAnnotationList:
            return textAnnotationList[0], textAnnotationList
        else:
            return currentAnnotation, textAnnotationList
