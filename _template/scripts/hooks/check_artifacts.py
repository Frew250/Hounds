#!/usr/bin/env python3
"""Stop hook: warns if build artifacts are missing for the current step branch."""
import json
import os
import re
import subprocess
import sys


def _step_dir_matches(step_dir: str, step_num: str) -> bool:
    padded = step_num.zfill(2)
    return step_dir.startswith(f"step{step_num}") or step_dir.startswith(
        f"step{padded}"
    )


def get_branch():
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def find_step_folder(branch):
    """Try to match branch name to a docs/build/ step folder."""
    phase_match = re.search(r"phase(\d+)", branch, re.IGNORECASE)
    step_match = re.search(r"step(\d+(?:\.\d+)?[a-z]?)", branch, re.IGNORECASE)
    if not step_match:
        return None

    phase_num = phase_match.group(1) if phase_match else None
    step_num = step_match.group(1)

    build_dir = "docs/build"
    if not os.path.isdir(build_dir):
        return None

    phase_dirs = sorted(
        [d for d in os.listdir(build_dir) if d.startswith("phase")],
        key=lambda d: (
            float(re.search(r"\d+", d).group()) if re.search(r"\d+", d) else 0
        ),
        reverse=True,
    )
    for phase_dir in phase_dirs:
        if phase_num and not phase_dir.startswith(f"phase{phase_num}"):
            continue
        phase_path = os.path.join(build_dir, phase_dir)
        if not os.path.isdir(phase_path):
            continue
        for step_dir in os.listdir(phase_path):
            if _step_dir_matches(step_dir, step_num):
                return os.path.join(phase_path, step_dir)

    return None


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, Exception):
        data = {}

    if data.get("stop_hook_active"):
        return

    branch = get_branch()

    # Only check on step branches, not build-track or main
    if not branch or branch in ("main",):
        return

    # Skip if it looks like a build-track branch (customize this pattern)
    if (
        branch.startswith("feat/")
        and "phase" not in branch.lower()
        and "step" not in branch.lower()
    ):
        return

    step_folder = find_step_folder(branch)

    if step_folder is None:
        output = {
            "systemMessage": f"Could not match branch '{branch}' to a build step folder. Make sure docs/build/ artifacts exist if this was a build step."
        }
        json.dump(output, sys.stdout)
        return

    # Check for required artifacts
    missing = []
    if not os.path.isfile(os.path.join(step_folder, "plan.md")):
        missing.append("plan.md")

    has_implementation_log = any(
        file_name == "implementation.md"
        or (file_name.startswith("implementation-") and file_name.endswith(".md"))
        for file_name in os.listdir(step_folder)
        if os.path.isfile(os.path.join(step_folder, file_name))
    )
    if not has_implementation_log:
        missing.append("implementation.md or implementation-*.md")

    has_any_fixes = any(
        f.startswith("fixes") and f.endswith(".md")
        for f in os.listdir(step_folder)
        if os.path.isfile(os.path.join(step_folder, f))
    )
    archive_folder = os.path.join(step_folder, "archive")
    if not has_any_fixes and os.path.isdir(archive_folder):
        has_any_fixes = any(
            f.startswith("fixes") and f.endswith(".md")
            for f in os.listdir(archive_folder)
            if os.path.isfile(os.path.join(archive_folder, f))
        )
    if not has_any_fixes:
        missing.append("fixes*.md (no review file)")

    if missing:
        output = {
            "systemMessage": f"Build artifact check: {step_folder} is missing {', '.join(missing)}. Every step needs plan.md, an implementation log, and at least one fixes file."
        }
        json.dump(output, sys.stdout)


if __name__ == "__main__":
    main()
