"""
@File        : settings.py
@Author      : MinDai, shi4712
@Date        : 2023/10/17 20:09
@Description : Define some basic constants and environment parameters
"""

import os

projectDir = os.path.dirname(__file__)
dataDir = os.path.join(projectDir, "data")
if not os.path.exists(dataDir):
    os.makedirs(dataDir)

tmpDir = os.path.join(projectDir, "tmp")
if not os.path.exists(tmpDir):
    os.makedirs(tmpDir)

hostDict = {
    # "host": "192.168.10.9",
    # "port": "7000",
    "host": "127.0.0.1",
    "port": 4712,
    # "use_reloader": False
    # "host": "8.140.239.104",
    # "port": 4712,
}

# ClickCellManager config
ClickCellManagerInitDict = {
    "max_data_number": 5,  # the numbers to handel multi-omics data
    "dataDir": dataDir,
}

# CanvasManager config
CanvasManagerInitDict = {
    "rowNum": 3,
    "colNum": 2
}

# # the mode CellMarker works
# # in local, CellMarker not load/save data with dash upload element
# # in sever, CellMarker load/save data with dash upload element
# mode = "local"  # sever

marker_ref = [
    os.path.join(projectDir, "marker_ref/CellMarker"),
    os.path.join(projectDir, "marker_ref/SingleCellBase"),
    os.path.join(projectDir, "marker_ref/CellSTAR"),
]

marker_ref_validation = [
    os.path.join(projectDir, "marker_ref/Other"),
]