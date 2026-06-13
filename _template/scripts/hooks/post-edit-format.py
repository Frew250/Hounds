#!/usr/bin/env python3
"""Post-edit auto-format hook.

Runs after file edits, reads JSON payload from stdin, and formats supported files.
Supports Python (via ruff) and JS/TS (via prettier).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

PRETTIER_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".css", ".json"}
REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIR = REPO_ROOT / "frontend"


def _resolve_ruff_executable() -> str:
    """Resolve Ruff executable from PATH or local virtual environment."""
    found = shutil.which("ruff")
    if found:
        return found

    candidates = [
        REPO_ROOT / ".venv" / "Scripts" / "ruff.exe",
        REPO_ROOT / ".venv" / "bin" / "ruff",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return "ruff"


RUFF_EXECUTABLE = _resolve_ruff_executable()


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a subprocess command without raising on non-zero exit."""
    return subprocess.run(command, check=False, capture_output=True, text=True)


def _extract_filepath(raw_input: str) -> str:
    """Extract file path from hook payload JSON."""
    if not raw_input.strip():
        return ""

    try:
        payload = json.loads(raw_input)
    except json.JSONDecodeError:
        return ""

    if not isinstance(payload, dict):
        return ""

    for key in ("file_path", "path", "filePath"):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def _format_python(file_path: Path) -> None:
    """Run Ruff formatting and autofixes for Python files."""
    _run([RUFF_EXECUTABLE, "format", "--quiet", str(file_path)])
    _run([RUFF_EXECUTABLE, "check", "--fix", str(file_path)])

    remaining = _run([RUFF_EXECUTABLE, "check", str(file_path)])
    output = (remaining.stdout or "") + (remaining.stderr or "")
    if "Found" in output:
        message = {
            "systemMessage": f"Lint issues in {file_path}:\\n{output}",
        }
        sys.stdout.write(json.dumps(message))


def _format_prettier(file_path: Path) -> None:
    """Run Prettier formatting for JS/TS/CSS/JSON files."""
    try:
        resolved = file_path.resolve()
    except OSError:
        resolved = file_path

    if resolved.is_relative_to(FRONTEND_DIR):
        command = [
            "npx",
            "--prefix",
            str(FRONTEND_DIR),
            "prettier",
            "--write",
            "--log-level",
            "silent",
            str(file_path),
        ]
    else:
        command = [
            "npx",
            "prettier",
            "--write",
            "--log-level",
            "silent",
            str(file_path),
        ]

    _run(command)


def main() -> None:
    raw = sys.stdin.read()
    file_path_str = _extract_filepath(raw)
    if not file_path_str:
        return

    file_path = Path(file_path_str)
    suffix = file_path.suffix.lower()

    if suffix == ".py":
        _format_python(file_path)
    elif suffix in PRETTIER_EXTENSIONS:
        _format_prettier(file_path)


if __name__ == "__main__":
    main()
