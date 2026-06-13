"""Build progress dashboard — generates console, Markdown, and HTML reports.

Usage:
    python scripts/build_progress.py              # Console output
    python scripts/build_progress.py --markdown    # Markdown table
    python scripts/build_progress.py --html        # HTML report
"""

import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = PROJECT_ROOT / "docs" / "build"
ARCH_BUILD_STEPS = PROJECT_ROOT / "docs" / "ARCH_BUILD_STEPS.md"
BUILD_TRACK_BRANCH = "dev"

USE_COLOR = (
    hasattr(sys.stdout, "isatty")
    and sys.stdout.isatty()
    and os.environ.get("NO_COLOR") is None
)


def _sort_key(name: str) -> tuple[int, tuple[int, ...], int, str]:
    match = re.match(r"(phase|step)(\d+(?:\.\d+)?)([a-z])?", name, re.IGNORECASE)
    if not match:
        return (1, (999999,), 0, name)
    parts = tuple(int(x) for x in match.group(2).split("."))
    suffix = ord(match.group(3).lower()) - ord("a") + 1 if match.group(3) else 0
    return (0, parts, suffix, name)


def get_step_status(step_path: Path) -> str:
    """Determine step status from artifacts present."""
    has_plan = (step_path / "plan.md").exists()
    has_impl = any(
        f.name == "implementation.md"
        or (f.name.startswith("implementation-") and f.name.endswith(".md"))
        for f in step_path.iterdir()
        if f.is_file()
    )
    has_fixes = any(
        f.name.startswith("fixes") and f.name.endswith(".md")
        for f in step_path.iterdir()
        if f.is_file()
    )
    archive = step_path / "archive"
    has_archived_fixes = archive.is_dir() and any(
        f.name.startswith("fixes") for f in archive.iterdir() if f.is_file()
    )

    if has_impl and has_archived_fixes and not has_fixes:
        return "finalized"
    elif has_impl and has_fixes:
        return "in review"
    elif has_impl:
        return "implemented"
    elif has_plan:
        return "planned"
    else:
        return "in progress"


def scan_build_dir() -> list[dict]:
    """Scan docs/build/ for phases and steps."""
    if not BUILD_DIR.is_dir():
        return []

    results = []
    phases = sorted(
        [d for d in BUILD_DIR.iterdir() if d.is_dir()],
        key=lambda d: _sort_key(d.name),
    )

    for phase_dir in phases:
        steps = sorted(
            [
                d
                for d in phase_dir.iterdir()
                if d.is_dir() and d.name.lower().startswith("step")
            ],
            key=lambda d: _sort_key(d.name),
        )
        for step_dir in steps:
            results.append(
                {
                    "phase": phase_dir.name,
                    "step": step_dir.name,
                    "status": get_step_status(step_dir),
                    "path": step_dir,
                }
            )

    return results


def print_console(steps: list[dict]) -> None:
    """Print progress to console."""
    status_icons = {
        "finalized": "✅" if USE_COLOR else "[DONE]",
        "in review": "🔍" if USE_COLOR else "[REVIEW]",
        "implemented": "🔨" if USE_COLOR else "[IMPL]",
        "planned": "📋" if USE_COLOR else "[PLAN]",
        "in progress": "🔄" if USE_COLOR else "[WIP]",
    }

    current_phase = None
    for step in steps:
        if step["phase"] != current_phase:
            current_phase = step["phase"]
            print(f"\n{current_phase}")
            print("-" * len(current_phase))

        icon = status_icons.get(step["status"], "❓")
        print(f"  {icon} {step['step']}: {step['status']}")

    total = len(steps)
    done = sum(1 for s in steps if s["status"] == "finalized")
    print(f"\nProgress: {done}/{total} steps finalized")


def print_markdown(steps: list[dict]) -> None:
    """Print progress as Markdown table."""
    print("# Build Progress\n")
    print("| Phase | Step | Status |")
    print("|-------|------|--------|")
    for step in steps:
        print(f"| {step['phase']} | {step['step']} | {step['status']} |")

    total = len(steps)
    done = sum(1 for s in steps if s["status"] == "finalized")
    print(f"\n**Progress: {done}/{total} steps finalized**")


def main():
    steps = scan_build_dir()

    if not steps:
        print("No build steps found in docs/build/")
        print("Create your first step with /newstep")
        return

    if "--markdown" in sys.argv:
        print_markdown(steps)
    else:
        print_console(steps)


if __name__ == "__main__":
    main()
