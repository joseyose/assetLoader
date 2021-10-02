# from importlib import reload
import geometry_finder
from PyQt5 import QtWidgets, QtCore, QtGui, uic
import sys
import os

# reload(geometry_finder)

# start class
class AssetViewer(QtWidgets.QDialog):
    def __init__(self):
        super(AssetViewer, self).__init__()
        # print("Running AssetViewer Constructor")

        # windowtile --- this call is not working, so I'm guessing I'm calling
        # the wrong thing
        self.setWindowTitle("Asset Viewer - [BETA]")
        uic.loadUi("./ui/dialog.ui", self)

        self.configure_ui()
        self.workers = []

    def configure_ui(self):
        """
        Configures the main sections of the ui like buttons and labels.
        This used to build the ui from scratch here before switching
        over to "ui" files.
        :return:
            None
        """
        # Directory line event for when a user hits enter after typing their
        # desired directory
        self.path_line.returnPressed.connect(self.update_path)
        # Browser button events
        self.btn_browser.clicked.connect(self.load_browser)

        # Load button events
        self.btn_load.clicked.connect(self.load_asset)
        self.btn_load.clearFocus()
        # Close button events
        self.btn_close.clicked.connect(self.close)

        # Set up the image we use for the title area
        icon = QtGui.QPixmap("./ui/resources/box.png")
        self.lbl_icon.setPixmap(icon)

    def populate(self):
        """
        Fills up the list widget with the available assets in the directory
        provided by the user.
        :return:
            None
        """
        # Get string from the ui directory path line
        dir_path = self.path_line.text()
        # Run external module that finds the stuff in the directory assigned.
        # This returns a dictionary we use later on
        try:
            self.assets = geometry_finder.FindAssets(directory=dir_path)

            if self.assets:
                for name, info in self.assets.items():
                    self.list_widget.addItem(name)
            else:
                sys.stderr.write(f"No assets available in {dir_path}\n")

        except Exception as err:
            sys.stderr.write(f"{err}\n")

    def load_browser(self):
        # Load the file dialog
        path = QtWidgets.QFileDialog.getExistingDirectory()
        if path:
            self.path_line.setText(path)
            self.populate()

    def update_path(self):
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

            worker = [False, self.asset_path]
            self.workers.append(worker)

        self.run()

    def run(self):

        for info in self.workers:
            index = self.workers.index(info)
            worker = info[0]
            name = info[1]

            # if worker is None and used is False:
            if worker is False:
                self.workers[index][0] = QtCore.QProcess()
                self.workers[index][0].start("gplay", [name])
                self.workers[index][0].finished.connect(lambda: self.process_finished(index))
                # self.workers[index][0].stateChanged.connect(self.handle_state)

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
