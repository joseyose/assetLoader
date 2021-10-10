import pytest
import os
# from assetloader.getassets import FindAssets, main
# from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from assetloader.getassets import FindAssets
# from assetloader.views import Window


# Test the exceptions raised
def test_wrongpath():
    path = "/hello/moto"
    with pytest.raises(Exception):
        FindAssets(path)


# def test_noargprovided(capture_stderr):
#     main()
#     assert capture_stderr["stderr"] == "Usage: python3 ./getassets.py directory"


def test_returnisdict():
    path = os.getcwd()
    assets = FindAssets(path)
    assert isinstance(assets, dict)


# When calling FindAssets ann subsequently we call find_assets on it we should
# get none, but not entirely sure why yet :)
def test_findassets():
    path = os.getcwd()
    assets = FindAssets(path).find_assets(path)
    assert assets == None


# @pytest.mark.skip(reason="I haven't implemented this yet")
# def test_skipexample():
#     assert 1 + 1 == 2


# @pytest.mark.xfail
# def test_failexample():
#     assert 1 / 0 == 1

# def test_search(qtbot):
#     # tmpdir.join('video1.abc').ensure()
#     p = "/home/joseyose/Documents/projects/test"
#     win = Window()
#     win.show()
#     qtbot.addWidget(win)

#     qtbot.keyClicks(win.path_line, p)
#     qtbot.keyPress(win.path_line, Qt.Key_Enter)
#     count = win.list_widget.count()

#     # win.list_widget.clear()
#     # qtbot.mouseClick(win.btn_browser, QtCore.Qt.LeftButton)
#     assert win.path_line.text() == p
#     assert count == 25
    # assert app_test.label.text() == "Assets Directory"


def test_load(qtbot, app_test, tmpdir):
    p = str(tmpdir)

    amount = 10
    for i in range(amount):
        with open(f"{p}/rock{i}.abc", "w") as f:
            f.write("")

    qtbot.keyClicks(app_test.path_line, p)
    qtbot.keyPress(app_test.path_line, Qt.Key_Enter)
    count = app_test.list_widget.count()

    # qtbot.mouseClick(win.btn_browser, QtCore.Qt.LeftButton)
    # assert app_test.path_line.text() == "ehllo"
    assert count == amount
    app_test.list_widget.clear()
    count = app_test.list_widget.count()
    assert count == 0
    # assert app_test.label.text() == "Assets Directory"


def test_clearing_list(qtbot, app_test, tmpdir):
    p = str(tmpdir)
    amount = 1
    for i in range(amount):
        with open(f"{p}/rock{i}.abc", "w") as f:
            f.write("")

    qtbot.keyClicks(app_test.path_line, p)
    qtbot.keyPress(app_test.path_line, Qt.Key_Enter)
    app_test.list_widget.clear()
    count = app_test.list_widget.count()
    assert count == 0
