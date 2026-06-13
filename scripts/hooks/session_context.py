#!/usr/bin/env python3
"""SessionStart hook: injects branch, build phase, and project state into every new agent session."""
import json
import os
import re
import subprocess
import sys


def _sort_key(name: str) -> tuple[int, tuple[int, ...], int, str]:
    match = re.match(r"(phase|step)(\d+(?:\.\d+)?)([a-z])?", name, re.IGNORECASE)
    if not match:
        return (1, (999999,), 0, name)
    parts = tuple(int(x) for x in match.group(2).split("."))
    suffix = ord(match.group(3).lower()) - ord("a") + 1 if match.group(3) else 0
    return (0, parts, suffix, name)


def get_branch():
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() or "detached HEAD"
    except Exception:
        return "unknown"


def get_latest_build_step():
    build_dir = "docs/build"
    if not os.path.isdir(build_dir):
        return None, None, []

    phases = sorted(
        [d for d in os.listdir(build_dir) if os.path.isdir(os.path.join(build_dir, d))],
        key=_sort_key,
    )
    if not phases:
        return None, None, []

    latest_phase = phases[-1]
    phase_path = os.path.join(build_dir, latest_phase)
    steps = sorted(
        [
            d
            for d in os.listdir(phase_path)
            if os.path.isdir(os.path.join(phase_path, d))
            and d.lower().startswith("step")
        ],
        key=_sort_key,
    )
    if not steps:
        return latest_phase, None, []

    latest_step = steps[-1]
    step_path = os.path.join(phase_path, latest_step)
    artifacts = sorted([f for f in os.listdir(step_path) if f.endswith(".md")])
    return latest_phase, latest_step, artifacts


def get_dirty_file_count():
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5
        )
        lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
        return len(lines)
    except Exception:
        return -1


def main():
    branch = get_branch()
    phase, step, artifacts = get_latest_build_step()
    dirty = get_dirty_file_count()

    parts = [f"Branch: {branch}"]

    if "phase" in branch.lower() or "step" in branch.lower():
        parts.append("On a step branch")

    if phase and step:
        parts.append(f"Latest build step: {phase}/{step}")
        parts.append(f"Artifacts: {', '.join(artifacts) if artifacts else 'none'}")
        has_plan = "plan.md" in artifacts
        has_impl = any(
            artifact == "implementation.md"
            or (artifact.startswith("implementation-") and artifact.endswith(".md"))
            for artifact in artifacts
        )
        has_fixes = any(f.startswith("fixes") for f in artifacts)
        archive_path = os.path.join("docs", "build", phase, step, "archive")
        has_archived_fixes = os.path.isdir(archive_path) and any(
            f.startswith("fixes") for f in os.listdir(archive_path)
        )
        if has_impl and has_archived_fixes and not has_fixes:
            parts.append("Status: finalized (archived)")
        elif has_impl and has_fixes:
            parts.append("Status: implementation done, review in progress")
        elif has_impl:
            parts.append("Status: implementation done, awaiting review")
        elif has_plan:
            parts.append("Status: planned, awaiting implementation")
        else:
            parts.append("Status: in progress")

    if dirty == 0:
        parts.append("Working tree: clean")
    elif dirty > 0:
        parts.append(f"Working tree: {dirty} modified file(s)")
        parts.append(
            "WARNING: Uncommitted changes detected. Do NOT run git pull until you "
            "commit or stash. Sequence: git add + git commit (or git stash) first, "
            "then git pull."
        )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": " | ".join(parts),
        }
    }
    json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
