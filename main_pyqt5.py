"""
@File        : main.py
@Author      : Min Dai, shi4712
@Date        : 2023/10/17 20:09
@Description : the main callbacks to run CellMarker
"""
import sys
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
import threading

import dash_bootstrap_components as dbc

from settings import hostDict
from apps.header import header
from apps.body import body

from callbacks.final import *


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowTitle('CellClick')

        # Correctly use QWebEngineView to display the Dash app
        self.web_view = QtWebEngineWidgets.QWebEngineView(self)
        self.web_view.setUrl(QtCore.QUrl("http://{}:{}".format(hostDict["host"], hostDict["port"])))
        self.setCentralWidget(self.web_view)

        # Start the Dash server in a separate thread
        threading.Thread(target=self.run_dash, daemon=True).start()

    def run_dash(self):
        app = dash.Dash(
            __name__,
            # server=server,
            assets_folder="assets",
            external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
        )
        app.layout = dash.html.Div(
            [
                header,
                body,
            ]
        )
        app.run_server(
            debug=False,
            **hostDict
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
    # sys.exit(app.exec_())