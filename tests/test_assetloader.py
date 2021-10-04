import pytest
import os
# from assetloader.getassets import FindAssets, main
from assetloader.getassets import FindAssets


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
