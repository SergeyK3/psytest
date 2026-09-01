"""Small cross-platform inter-process file lock for runtime coordination."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import BinaryIO


class LockTimeoutError(TimeoutError):
    """Raised when a runtime lock cannot be acquired before its timeout."""


class InterProcessFileLock:
    """An OS-backed lock released automatically when the process exits."""

    def __init__(self, path: Path, timeout_seconds: float = 30.0) -> None:
        self.path = Path(path)
        self.timeout_seconds = timeout_seconds
        self._file: BinaryIO | None = None

    def __enter__(self) -> "InterProcessFileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            self.path.parent.chmod(0o700)
        self._file = self.path.open("a+b")
        if os.name != "nt":
            self.path.chmod(0o600)
        self._ensure_lock_byte()
        self._acquire()
        return self

    def __exit__(self, _exc_type, _exc, _traceback) -> None:
        if self._file is None:
            return
        try:
            self._release()
        finally:
            self._file.close()
            self._file = None

    def _ensure_lock_byte(self) -> None:
        assert self._file is not None
        self._file.seek(0, os.SEEK_END)
        if self._file.tell() == 0:
            self._file.write(b"0")
            self._file.flush()
        self._file.seek(0)

    def _acquire(self) -> None:
        assert self._file is not None
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            try:
                if os.name == "nt":
                    import msvcrt

                    self._file.seek(0)
                    msvcrt.locking(self._file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except OSError as exc:
                if time.monotonic() >= deadline:
                    raise LockTimeoutError("Timed out acquiring runtime lock") from exc
                time.sleep(0.05)

    def _release(self) -> None:
        assert self._file is not None
        if os.name == "nt":
            import msvcrt

            self._file.seek(0)
            msvcrt.locking(self._file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)
