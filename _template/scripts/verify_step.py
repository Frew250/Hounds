"""Verify a build step is complete before finalization.

Usage:
    python scripts/verify_step.py <phase> <step>
    python scripts/verify_step.py <phase> <step> <subplan>

Examples:
    python scripts/verify_step.py phase2 step7a-new-data-models
    python scripts/verify_step.py phase2 step6.5-doc-refactor 6.5b
"""

import os
import re
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARCH_BUILD_STEPS = PROJECT_ROOT / "docs" / "ARCH_BUILD_STEPS.md"

# Configure this for your project — map canonical doc short names to file paths.
# Used by the canonical doc updates checker.
DOC_NAME_MAP = {
    # "DATA_MODEL": "docs/DATA_MODEL.md",
    # "API_DESIGN": "docs/API_DESIGN.md",
    # "CLAUDE": "CLAUDE.md",
    # "copilot-instructions": ".github/copilot-instructions.md",
}

# The build-track branch name (for TODO/FIXME diffing)
BUILD_TRACK_BRANCH = "{{BUILD_TRACK_BRANCH}}"

USE_COLOR = (
    hasattr(sys.stdout, "isatty")
    and sys.stdout.isatty()
    and os.environ.get("NO_COLOR") is None
)
PASS = "\033[32m✓\033[0m" if USE_COLOR else "[PASS]"
FAIL = "\033[31m✗\033[0m" if USE_COLOR else "[FAIL]"


def _run(
    cmd: list[str], cwd: str | Path | None = None, timeout: int = 120
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=cwd or PROJECT_ROOT,
            shell=(sys.platform == "win32"),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(
            cmd, returncode=1, stdout="", stderr=f"Command timed out after {timeout}s"
        )


def check_plan_exists(step_dir: Path) -> tuple[bool, str]:
    plan = step_dir / "plan.md"
    if not plan.exists():
        return False, "plan.md not found"
    if plan.stat().st_size == 0:
        return False, "plan.md is empty"
    return True, "plan.md exists and is non-empty"


def _extract_verdict_window(text: str) -> str:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.match(r"^\s*##\s+(?:\d+\.\s*)?Verdict\s*$", line, flags=re.IGNORECASE):
            return "\n".join(lines[i : min(len(lines), i + 8)])
    return ""


def _is_cleared_fixes_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    verdict_window = _extract_verdict_window(text)
    return "cleared" in verdict_window.lower()


def _latest_fixes_file(pattern_paths: list[Path]) -> Path | None:
    if not pattern_paths:
        return None

    def order_key(p: Path) -> tuple[int, float]:
        m = re.search(r"-(\d+)\.md$", p.name)
        n = int(m.group(1)) if m else -1
        return (n, p.stat().st_mtime)

    return sorted(pattern_paths, key=order_key)[-1]


def parse_required_subplans(step_dir: Path) -> list[str]:
    plan = step_dir / "plan.md"
    if not plan.exists():
        return []
    text = plan.read_text(encoding="utf-8", errors="ignore")
    matches = re.findall(r"Sub-plan\s+([0-9]+(?:\.[0-9]+)?[a-z][0-9]*)", text)
    ordered: list[str] = []
    seen: set[str] = set()
    for m in matches:
        if m not in seen:
            seen.add(m)
            ordered.append(m)
    return ordered


def check_subplan_artifacts(step_dir: Path, subplan: str) -> tuple[bool, str]:
    implementation = step_dir / f"implementation-{subplan}.md"
    if not implementation.exists():
        return False, f"Missing implementation-{subplan}.md"

    fixes_files = sorted(step_dir.glob(f"fixes-{subplan}-*.md"))
    archive_dir = step_dir / "archive"
    if not fixes_files and archive_dir.is_dir():
        fixes_files = sorted(archive_dir.glob(f"fixes-{subplan}-*.md"))
    if not fixes_files:
        return False, f"No fixes-{subplan}-*.md files found"

    latest = _latest_fixes_file(fixes_files)
    if latest is None:
        return False, f"Could not determine latest fixes file for {subplan}"

    if not _is_cleared_fixes_file(latest):
        return False, f"Latest fixes file is not cleared: {latest.name}"

    return True, f"{implementation.name} + cleared {latest.name}"


def check_full_step_artifacts(step_dir: Path) -> tuple[bool, str]:
    subplans = parse_required_subplans(step_dir)
    if subplans:
        missing: list[str] = []
        uncleared: list[str] = []
        for subplan in subplans:
            ok, msg = check_subplan_artifacts(step_dir, subplan)
            if not ok:
                if msg.startswith("Missing"):
                    missing.append(subplan)
                else:
                    uncleared.append(f"{subplan} ({msg})")
        if missing:
            return False, "Missing sub-plan implementation/clearance: " + ", ".join(
                missing
            )
        if uncleared:
            return False, "Sub-plan(s) not cleared: " + "; ".join(uncleared)
        return True, f"All required sub-plans cleared: {', '.join(subplans)}"

    implementation = step_dir / "implementation.md"
    if not implementation.exists():
        impls = sorted(step_dir.glob("implementation-*.md"))
        if impls:
            return (
                False,
                "Found sub-plan implementation files but no step-level implementation.md.",
            )
        return False, "Missing implementation.md"

    fixes_files = sorted(step_dir.glob("fixes*.md"))
    archive_dir = step_dir / "archive"
    if not fixes_files and archive_dir.is_dir():
        fixes_files = sorted(archive_dir.glob("fixes*.md"))
    if not fixes_files:
        return False, "No fixes*.md file found"

    latest = _latest_fixes_file(fixes_files)
    if latest is None:
        return False, "Could not determine latest fixes file"
    if not _is_cleared_fixes_file(latest):
        return False, f"Latest fixes file is not cleared: {latest.name}"

    return True, f"implementation.md + cleared {latest.name}"


def check_no_todo_fixme() -> tuple[bool, str]:
    result = _run(["git", "diff", "--name-only", f"{BUILD_TRACK_BRANCH}...HEAD"])
    if result.returncode != 0:
        return False, f"git diff failed: {result.stderr.strip()}"
    changed_files = [f for f in result.stdout.strip().splitlines() if f]
    if not changed_files:
        return True, "No files changed on this branch"
    hits: list[str] = []
    for rel_path in changed_files:
        full = PROJECT_ROOT / rel_path
        if not full.is_file():
            continue
        # Skip verification infrastructure
        if rel_path in ("scripts/verify_step.py", "scripts/build_progress.py"):
            continue
        try:
            text = full.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            upper = line.upper()
            if "TODO" in upper or "FIXME" in upper:
                # Skip YAML tool declarations, doc discussions, archive paths
                stripped = line.strip()
                if '"todo"' in stripped.lower():
                    continue
                if any(p in rel_path for p in ("archive/", "subagent-outputs/")):
                    continue
                hits.append(f"  {rel_path}:{i}")
    if hits:
        preview = hits[:10]
        msg = f"{len(hits)} TODO/FIXME marker(s) found:\n" + "\n".join(preview)
        if len(hits) > 10:
            msg += f"\n  ... and {len(hits) - 10} more"
        return False, msg
    return True, f"No TODO/FIXME in {len(changed_files)} changed file(s)"


def check_pytest() -> tuple[bool, str]:
    result = _run([sys.executable, "-m", "pytest", "tests/", "-v"])
    combined = (result.stdout + "\n" + result.stderr).strip()
    if result.returncode != 0:
        last_lines = [l for l in combined.splitlines() if l.strip()][-5:]
        return False, "pytest failed:\n" + "\n".join(f"  {l}" for l in last_lines)
    summary = [l for l in combined.splitlines() if "passed" in l or "failed" in l]
    return True, summary[-1].strip() if summary else "All tests passed"


def check_canonical_doc_updates(step_dir: Path) -> tuple[bool, str]:
    plan_file = step_dir / "plan.md"
    if not plan_file.exists():
        return True, "No plan.md — skipped"

    try:
        plan_text = plan_file.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return True, "Could not read plan.md — skipped"

    section_match = re.search(
        r"##\s+(?:\d+\.\s*)?Canonical Doc Updates\s*\n(.*?)(?=\n##|\Z)",
        plan_text,
        re.DOTALL,
    )
    if not section_match:
        return True, "No '## Canonical Doc Updates' section in plan"

    section = section_match.group(1)
    doc_refs: set[str] = set()
    for m in re.finditer(r"`?(docs/[A-Za-z_.\-/]+\.md)`?", section):
        doc_refs.add(m.group(1).strip("`"))
    for name in sorted(DOC_NAME_MAP, key=len, reverse=True):
        if name in section:
            doc_refs.add(DOC_NAME_MAP[name])

    if not doc_refs:
        return True, "Canonical Doc Updates section found but no target docs identified"

    unapplied: list[str] = []
    for doc_path_str in sorted(doc_refs):
        doc_path = PROJECT_ROOT / doc_path_str
        if not doc_path.exists():
            unapplied.append(f"{doc_path_str} (file does not exist)")

    if unapplied:
        detail = "\n".join(f"  {u}" for u in unapplied)
        return False, f"{len(unapplied)} canonical doc(s) not found:\n{detail}"

    return True, f"All {len(doc_refs)} proposed doc(s) exist"


# --- Deferred items checking ---

_DEFERRED_SECTION_RE = re.compile(
    r"##\s+(?:\d+\.\s*)?(?:Deferred Items|Issues [Dd]eferred[^\n]*|Deferred Items Remaining)\s*\n(.*?)(?=\n##|\Z)",
    re.DOTALL,
)
_STEP_REF_RE = re.compile(r"(?:step|sub-?plan)\s*\d", re.IGNORECASE)


def check_deferred_items(step_dir: Path) -> tuple[bool, str]:
    impl_files = sorted(step_dir.glob("implementation*.md"))
    if not impl_files:
        return True, "No implementation logs — skipped"

    unowned: list[str] = []
    for md_file in impl_files:
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for section_match in _DEFERRED_SECTION_RE.finditer(text):
            section = section_match.group(1)
            for line in section.splitlines():
                line = line.strip()
                if not (line.startswith("-") or line.startswith("*")):
                    continue
                content = line.lstrip("-* ").strip()
                if not content or content.lower() in ("none", "none.", "n/a"):
                    continue
                if not _STEP_REF_RE.search(line):
                    unowned.append(f"{md_file.name}: {content[:80]}")

    if unowned:
        detail = "\n".join(f"  {u}" for u in unowned[:5])
        return False, f"{len(unowned)} deferred item(s) without owning step:\n{detail}"

    return True, "All deferred items have owning steps"


# --- Main ---


def find_step_dir(phase: str, step: str) -> Path | None:
    build_dir = PROJECT_ROOT / "docs" / "build"
    if not build_dir.is_dir():
        return None

    for phase_dir in build_dir.iterdir():
        if not phase_dir.is_dir():
            continue
        if phase.lower() not in phase_dir.name.lower():
            continue
        for step_dir in phase_dir.iterdir():
            if not step_dir.is_dir():
                continue
            if step.lower() in step_dir.name.lower():
                return step_dir
    return None


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <phase> <step> [subplan]")
        sys.exit(1)

    phase = sys.argv[1]
    step = sys.argv[2]
    subplan = sys.argv[3] if len(sys.argv) > 3 else None

    step_dir = find_step_dir(phase, step)
    if step_dir is None:
        print(f"{FAIL} Could not find step directory for {phase}/{step}")
        sys.exit(1)

    print(f"Verifying: {step_dir.relative_to(PROJECT_ROOT)}")
    print()

    checks = [
        ("Plan exists", check_plan_exists(step_dir)),
    ]

    if subplan:
        checks.append(
            ("Sub-plan artifacts", check_subplan_artifacts(step_dir, subplan))
        )
    else:
        checks.append(("Step artifacts", check_full_step_artifacts(step_dir)))

    checks.extend(
        [
            ("No TODO/FIXME", check_no_todo_fixme()),
            ("Canonical doc updates", check_canonical_doc_updates(step_dir)),
            ("Deferred items", check_deferred_items(step_dir)),
            ("Tests pass", check_pytest()),
        ]
    )

    all_pass = True
    for name, (ok, msg) in checks:
        icon = PASS if ok else FAIL
        print(f"  {icon} {name}: {msg}")
        if not ok:
            all_pass = False

    print()
    if all_pass:
        print("All checks passed — step is ready for finalization.")
    else:
        print("Some checks failed — fix the issues above before finalizing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
