import os
import shutil
import socket
from pathlib import Path
from uuid import uuid4

import pytest


os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("BOT_TOKEN", "offline-test-placeholder")


@pytest.fixture(autouse=True)
def block_external_network(monkeypatch):
    """Fail every offline test that attempts a network connection."""

    def forbidden(*_args, **_kwargs):
        raise AssertionError("external network access is forbidden in offline tests")

    monkeypatch.setattr(socket, "create_connection", forbidden)


@pytest.fixture
def safe_tmp_path():
    """A sandbox-writable temporary directory without pytest chmod behavior."""
    path = Path(__file__).resolve().parents[1] / ".test-runtime" / uuid4().hex
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
        try:
            path.parent.rmdir()
        except OSError:
            pass
