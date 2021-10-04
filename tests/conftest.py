import pytest
import sys


@pytest.fixture
def capture_stderr(monkeypatch):
    buffer = {"stderr": "", "write_calls": 0}

    def fake_write(s):
        buffer["stderr"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stderr, "write", fake_write)
    return buffer
