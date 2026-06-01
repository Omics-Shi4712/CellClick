"""
@File        : main.py
@Author      : Min Dai, shi4712
@Date        : 2023/10/17 20:09
@Description : the main callbacks to run CellMarker
"""
import dash_bootstrap_components as dbc

from settings import hostDict
from apps.header import header
from apps.body import body

from callbacks.final import *

app = dash.Dash(
    __name__,
    # server=server,
    assets_folder="assets",
    # external_stylesheets=[
    #     # dbc.themes.BOOTSTRAP,
    #     # dbc.icons.BOOTSTRAP,
    # #     "assets/bootstrap-icons-1.11.3/fonts/bootstrap-icons.scss"
    # ]
    external_stylesheets=[
        "assets/bootstrap-icons-1.11.3/bootstrap-icons-1.11.3/font/bootstrap-icons.css"
    ]
)

app.layout = dash.html.Div(
    [
        header,
        body,
    ]
)

# app.css.config.serve_locally = True
# app.scripts.config.serve_locally = True
app.run_server(
    debug=True,
    # debug=True,
    **hostDict
)
