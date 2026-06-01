#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: document_template.py
@time: 2024/12/25 10:28
"""
from apps.moduleSettings import dataSettingCard, preprocessingCard, dataVisualizationCard, geneAnalysisCard, evaluationValidationCard, cellReannotationCard


def createDocumentJson(modules):
    document = {}
    for module in modules:
        moduleDict = {
            "overview": "",
        }
        formDict = {}
        for form in module["forms"]:
            formDict[form["form_name"]] = {
                "overview": {
                    "img": "", "description": ""
                },
                "form introduction": {"img": ""},
                "example": [{"video": "", "title": "", "description": "",}]
            }
            inputsDict = {}
            for line in form["lines"]:
                if line[0]["label_name"] != "Submit" and line[0]["label_name"] != "Object Name":
                    inputsDict[line[0]["label_name"]] = ""
            formDict[form["form_name"]]["form introduction"]["inputs"] = inputsDict
        moduleDict["forms"] = formDict
        document[module["card_name"]] = moduleDict

    import json
    with open("./document_template.json", "w") as f:
        json.dump(document, f)


cellClickModules = [
    dataSettingCard, preprocessingCard, dataVisualizationCard,
    geneAnalysisCard, evaluationValidationCard, cellReannotationCard
]

createDocumentJson(cellClickModules)
