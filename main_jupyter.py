#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: main_jupyter.py.py
@time: 2024/12/2 9:36
"""

import dash_bootstrap_components as dbc

from settings import hostDict
from apps.header import header
from apps.body import body

from callbacks.final import *
from jupyter_dash import JupyterDash

cellClickManager.__setMode__("jupyter")

app = JupyterDash(
    __name__,
    # server=server,
    assets_folder="assets",
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
    # external_stylesheets=[
    #     "assets/2_common.css", "assets/3_custom.css", "assets/0_bootstrap.min.css", "assets/1_bootstrap-icons.css"
    # ]
)

app.layout = dash.html.Div(
    [
        header,
        body,
    ]
)
# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
# app.run_server(
#     # debug=False,
#     debug=True,
#     **hostDict
# )
