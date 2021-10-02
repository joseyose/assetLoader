from importlib import reload
from geometry_finder import FindAssets
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import os
import resources
import subprocess
import time
import pprint


# reload(FindAssets)

# start class
class AssetViewer(QtWidgets.QDialog):
    def __init__(self):
        super(AssetViewer, self).__init__()
        print("Running AssetViewer Constructor")

        # windowtile
        self.setWindowTitle("Asset Viewer - [BETA]")
        # self.resize(600, 600)
        uic.loadUi("dialog.ui", self)

        self.build_ui()
        self.path_line.editingFinished.connect(self.update_path)

        self.p = None
        self.workers = []
        # pprint.pprint(self.assets)

    def build_ui(self):
        # layout = QtWidgets.QVBoxLayout(self)
        #
        # btn_widget = QtWidgets.QWidget()
        # btn_layout = QtWidgets.QHBoxLayout(btn_widget)
        # layout.addWidget(btn_widget)

        # Directory line
        # label_dir = QtWidgets.QLabel("Assets Directory:")
        # self.path_line = QtWidgets.QLineEdit()
        self.path_line.returnPressed.connect(self.update_path)

        # btn_browser = QtWidgets.QPushButton("...")
        # btn_browser = QtWidgets.QToolButton()
        # btn_browser.setText("...")
        # btn_browser.clearFocus()
        self.btn_browser.clicked.connect(self.load_browser)

        # btn_layout.addWidget(label_dir)
        # btn_layout.addWidget(self.path_line)
        # btn_layout.addWidget(btn_browser)

        # self.list_widget = QtWidgets.QListWidget()
        # layout.addWidget(self.list_widget)

        #############################################
        # bottom_widget = QtWidgets.QWidget()
        # bottom_layout = QtWidgets.QHBoxLayout(bottom_widget)
        # layout.addWidget(bottom_widget)

        # btn_load = QtWidgets.QPushButton("Load")
        self.btn_load.clicked.connect(self.load_asset)
        self.btn_load.clearFocus()
        # btn_close = QtWidgets.QPushButton("Close")
        self.btn_close.clicked.connect(self.close)

        icon = QtGui.QPixmap("./resources/box.png")
        self.lbl_icon.setPixmap(icon)

        # bottom_layout.addWidget(btn_load)
        # bottom_layout.addWidget(btn_close)

    def populate(self):
        dir_path = self.path_line.text()
        self.assets = FindAssets(directory=dir_path)
        if self.assets:
            for name, info in self.assets.items():
                self.list_widget.addItem(name)
        else:
            print("No assets available. Double check your path")

    def load_browser(self):
        # Load the file dialog
        path = QtWidgets.QFileDialog.getExistingDirectory()
        if path:
            self.path_line.setText(path)
            self.populate()

    def update_path(self):
        print("updating path")
        self.list_widget.clear()
        self.populate()

    def get_selection(self):
        selected = self.list_widget.selectedItems()
        return selected

    def load_asset(self):
        asset = self.get_selection()
        if asset:
            asset_name = asset[0].text()
            ext = self.assets[asset_name]["type"]
            self.asset_path = os.path.join(self.path_line.text(), f"{asset_name}{ext}")
            # print(self.asset_path)

            worker = [False, self.asset_path, False]
            # self.workers.insert(0, worker)
            self.workers.append(worker)

        self.run()

        # print(self.workers)

    def run(self):

        for info in self.workers:
            index = self.workers.index(info)
            worker = info[0]
            name = info[1]
            used = info[2]
            # if worker is None and used is False:
            if worker is False:
                self.workers[index][0] = QtCore.QProcess()
                self.workers[index][0].start("gplay", [name])
                self.workers[index][0].finished.connect(lambda: self.process_finished(index))
                self.workers[index][0].stateChanged.connect(self.handle_state)

    def process_finished(self, index):
        self.workers[index][0] = True
        # self.workers[index][2] = True

    def handle_state(self, state):
        """This sends to `stdout` what the status of the application is

        Args:
            The state from the application

        Returns:
            None
        """
        states = {
            QtCore.QProcess.NotRunning: 'Not running',
            QtCore.QProcess.Starting: 'Starting',
            QtCore.QProcess.Running: 'Running',
        }
        state_name = states[state]
        print(f"State changed: {state_name}")

        # if state_name == "Not running":
        #     self.workers.remove(index)
        #     print("POP IT")


# def show_ui():
#     app = QtWidgets.QApplication(sys.argv)
#     ui = AssetViewer()
#     ui.show()
#     return ui

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = AssetViewer()
    main.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print("Closing window...")
