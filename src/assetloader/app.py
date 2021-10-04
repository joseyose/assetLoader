import sys
from PyQt5.QtWidgets import QApplication
from .views import Window
'''
/*
 * app.py
 *
 * by joseyose, Oct 2021
 *
 * Main driver for our GUI application.
 *
 */
'''
"""This module provides the AssetLoader application."""


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()

    sys.exit(app.exec())
