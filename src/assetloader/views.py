'''
/*
 * views.py
 *
 * by joseyose, Oct 2021
 *
 * Implementation of the Window class. This handles all of the logic for the
 * PyQt5 GUI. It provides the AssetLoader main window.
 *
 */
'''

from .getassets import FindAssets
from .ui.window import Ui_Dialog
from PyQt5 import QtWidgets, QtCore, QtGui
from pathlib import Path
import sys


class Window(QtWidgets.QDialog, Ui_Dialog):
    """Inherits from QDialog, Ui_Dialog. Sets up all of the necessary
    GUI logic.
    """
    def __init__(self):
        """inits Window"""
        super(Window, self).__init__()

        self._setupUI()
        self.setWindowTitle("AssetLoader - [BETA]")
        self.configure_ui()
        self.workers = []

        self.list_widget.itemClicked.connect(self._updateStateWhenSelected)

    def _setupUI(self):
        """Initialize all of the ui that was created in qtdesigner.
        It also disables the load button at startup.
        """
        self.setupUi(self)
        self.btn_load.setEnabled(False)

    def configure_ui(self):
        """
        Configures the main sections of the ui like buttons and labels.
        This used to build the ui from scratch here before switching
        over to "ui" files.
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
        icon = QtGui.QPixmap("./src/assetloader/ui/resources/box.png")
        self.lbl_icon.setPixmap(icon)

    def populate(self):
        """
        Fills up the list widget with the available assets in the directory
        provided by the user.
        """
        # Get string from the ui directory path line
        dir_path = self.path_line.text()
        # Run external module that finds the stuff in the directory assigned.
        # This returns a dictionary we use later on
        try:
            self.assets = FindAssets(directory=dir_path)

            if self.assets:
                for name, info in self.assets.items():

                    self.list_widget.addItem(info["fullname"])
                    # a = info["fullname"]
                    # print(a)
            else:
                sys.stderr.write(f"No assets available in {dir_path}\n")

        except Exception as err:
            sys.stderr.write(f"{err}\n")

    def load_browser(self):
        """Handles the logic for loading up a file dialog, and calling the
        populate function after acquiring a path.
        """
        # Set initial directory based on your home directory
        if self.path_line.text():
            initDir = self.path_line.text()
        else:
            initDir = str(Path.home())
        # Load the file dialog
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory Containing 3D Objects", initDir)
        if path:
            self.path_line.setText(path)
            self.populate()

    def update_path(self):
        """Updates the list of assets available to load if the user updates
        the paths directly instead of going through the file dialog.
        """
        self.list_widget.clear()
        self.populate()

    def get_selection(self):
        """Collects the item the user has a selected

        Returns:
            A list containing the assets selected by the user.
        """
        selected = self.list_widget.selectedItems()
        return selected

    def load_asset(self):
        """Retrieves the selected asset from the list and adds a new worker
        to our worker stack and calls `self.run`
        """
        asset = self.get_selection()
        if asset:
            asset_name = asset[0].text()
            self.asset_path = self.assets[asset_name]["path"]

            worker = [False, self.asset_path]
            self.workers.append(worker)

        self.run()

    def run(self):
        """Checks our worker stack and anyone not running already it will
        create a new QProcess and launch the `GPlay` application
        """

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
        """Changes the status of the worker thread to done after the
        user closes it

        Args:
            index ([int]): Index of the worker in the stack that needs
            to update
        """
        self.workers[index][0] = True

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

    def _updateStateWhenSelected(self):
        """Enables the load button"""
        self.btn_load.setEnabled(True)
