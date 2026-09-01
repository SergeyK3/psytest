import os
import shutil
import socket
import tempfile
from pathlib import Path

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
    """A unique temporary directory that is always outside the Git checkout."""
    repository_root = Path(__file__).resolve().parents[1]
    configured_root = os.getenv("PSYTEST_TEST_TMPDIR", "").strip()
    temporary_root = Path(configured_root or tempfile.gettempdir()).expanduser().resolve()
    if not temporary_root.is_dir():
        raise RuntimeError("PSYTEST_TEST_TMPDIR must reference an existing directory")
    if temporary_root == repository_root or repository_root in temporary_root.parents:
        raise RuntimeError("Test temporary directory must be outside the Git checkout")

    path = Path(
        tempfile.mkdtemp(prefix="psytest-tests-", dir=str(temporary_root))
    ).resolve()
    try:
        assert path != repository_root and repository_root not in path.parents
        yield path
    finally:
        if path.is_symlink():
            path.unlink()
        elif path.exists():
            shutil.rmtree(path)
