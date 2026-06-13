#!/usr/bin/env python3
"""Lightweight workflow audit for docs/build/ artifacts.

This is a generic template version of the workflow audit used to catch obvious
process drift in build artifacts.

Usage:
    python scripts/workflow_audit.py
    python scripts/workflow_audit.py --scope phase2
    python scripts/workflow_audit.py --output docs/build/workflow-reviews/custom.md
    python scripts/workflow_audit.py --check
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = PROJECT_ROOT / "docs" / "build"
REPORT_DIR = BUILD_DIR / "workflow-reviews"
ACKNOWLEDGED_FILE = REPORT_DIR / "acknowledged.md"

DEFERRED_SECTION_RE = re.compile(
    r"##\s+(?:\d+\.\s*)?(?:Deferred Items|Issues [Dd]eferred[^\n]*|Deferred Items Remaining)\s*\n(.*?)(?=\n##|\Z)",
    re.DOTALL,
)
STEP_REF_RE = re.compile(r"(?:step|sub-?plan)\s*\d", re.IGNORECASE)
UNRESOLVED_RE = re.compile(
    r"\b(TBD|TODO|FIXME|open question|needs decision|unresolved|needs clarification)\b",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scope", help="Limit audit to a phase directory name, e.g. phase2"
    )
    parser.add_argument("--output", help="Write report to a custom path")
    parser.add_argument(
        "--check", action="store_true", help="Exit 1 when anomalies exist"
    )
    return parser.parse_args()


def load_acknowledged() -> dict[str, list[str]]:
    if not ACKNOWLEDGED_FILE.exists():
        return {}

    content = ACKNOWLEDGED_FILE.read_text(encoding="utf-8", errors="ignore")
    acknowledgments: dict[str, list[str]] = {}
    current: str | None = None

    for line in content.splitlines():
        section = re.match(r"^##\s+(.+)$", line)
        if section:
            current = section.group(1).strip().lower()
            continue

        if not current or not line.strip().startswith("-"):
            continue

        pattern = line.strip().lstrip("- ").split("|")[0].strip()
        if pattern:
            acknowledgments.setdefault(current, []).append(pattern.lower())

    return acknowledgments


def is_acknowledged(acks: dict[str, list[str]], section: str, text: str) -> bool:
    patterns = acks.get(section, [])
    lowered = text.lower()
    return any(pattern in lowered for pattern in patterns)


def find_step_dirs(scope: str | None) -> list[Path]:
    if not BUILD_DIR.is_dir():
        return []

    phase_dirs = sorted(path for path in BUILD_DIR.iterdir() if path.is_dir())
    step_dirs: list[Path] = []

    for phase_dir in phase_dirs:
        if scope and scope.lower() not in phase_dir.name.lower():
            continue
        if phase_dir.name == "workflow-reviews":
            continue
        for child in sorted(phase_dir.iterdir()):
            if child.is_dir() and child.name.lower().startswith("step"):
                step_dirs.append(child)

    return step_dirs


def has_fixes(step_dir: Path) -> bool:
    top_level = any(
        path.name.startswith("fixes") and path.suffix == ".md"
        for path in step_dir.iterdir()
        if path.is_file()
    )
    if top_level:
        return True
    archive_dir = step_dir / "archive"
    return archive_dir.is_dir() and any(
        path.name.startswith("fixes") and path.suffix == ".md"
        for path in archive_dir.iterdir()
        if path.is_file()
    )


def fixes_count(step_dir: Path) -> int:
    count = sum(
        1
        for path in step_dir.iterdir()
        if path.is_file() and path.name.startswith("fixes") and path.suffix == ".md"
    )
    archive_dir = step_dir / "archive"
    if archive_dir.is_dir():
        count += sum(
            1
            for path in archive_dir.iterdir()
            if path.is_file() and path.name.startswith("fixes") and path.suffix == ".md"
        )
    return count


def scan_missing_artifacts(
    step_dirs: list[Path], acks: dict[str, list[str]]
) -> list[str]:
    findings: list[str] = []
    for step_dir in step_dirs:
        missing: list[str] = []
        if not (step_dir / "plan.md").exists():
            missing.append("plan.md")
        if not any(
            path.is_file()
            and path.name.startswith("implementation")
            and path.suffix == ".md"
            for path in step_dir.iterdir()
        ):
            missing.append("implementation*.md")
        if not has_fixes(step_dir):
            missing.append("fixes*.md")
        if missing:
            finding = (
                f"{step_dir.relative_to(PROJECT_ROOT)}: missing {', '.join(missing)}"
            )
            if not is_acknowledged(acks, "missing-artifacts", finding):
                findings.append(finding)
    return findings


def scan_review_rounds(step_dirs: list[Path], acks: dict[str, list[str]]) -> list[str]:
    findings: list[str] = []
    for step_dir in step_dirs:
        count = fixes_count(step_dir)
        if count >= 3:
            finding = f"{step_dir.relative_to(PROJECT_ROOT)}: {count} fixes files"
            if not is_acknowledged(acks, "review-rounds", finding):
                findings.append(finding)
    return findings


def scan_deferred_items(step_dirs: list[Path], acks: dict[str, list[str]]) -> list[str]:
    findings: list[str] = []
    for step_dir in step_dirs:
        for impl_file in sorted(step_dir.glob("implementation*.md")):
            text = impl_file.read_text(encoding="utf-8", errors="ignore")
            for match in DEFERRED_SECTION_RE.finditer(text):
                section = match.group(1)
                for line in section.splitlines():
                    stripped = line.strip()
                    if not stripped.startswith(("-", "*")):
                        continue
                    if not STEP_REF_RE.search(stripped):
                        finding = f"{impl_file.relative_to(PROJECT_ROOT)}: {stripped.lstrip('-* ').strip()}"
                        if not is_acknowledged(acks, "deferred-items", finding):
                            findings.append(finding)
    return findings


def scan_unresolved(step_dirs: list[Path], acks: dict[str, list[str]]) -> list[str]:
    findings: list[str] = []
    for step_dir in step_dirs:
        files = list(step_dir.glob("*.md"))
        archive_dir = step_dir / "archive"
        if archive_dir.is_dir():
            files.extend(path for path in archive_dir.glob("*.md"))
        for md_file in sorted(files):
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            for number, line in enumerate(text.splitlines(), start=1):
                if UNRESOLVED_RE.search(line):
                    finding = (
                        f"{md_file.relative_to(PROJECT_ROOT)} L{number}: {line.strip()}"
                    )
                    if not is_acknowledged(acks, "unresolved-decisions", finding):
                        findings.append(finding)
    return findings


def build_report(scope: str | None) -> tuple[str, int]:
    acks = load_acknowledged()
    step_dirs = find_step_dirs(scope)

    missing_artifacts = scan_missing_artifacts(step_dirs, acks)
    review_rounds = scan_review_rounds(step_dirs, acks)
    deferred_items = scan_deferred_items(step_dirs, acks)
    unresolved = scan_unresolved(step_dirs, acks)

    anomaly_count = (
        len(missing_artifacts)
        + len(review_rounds)
        + len(deferred_items)
        + len(unresolved)
    )

    lines = [
        f"# Workflow Audit — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Scope: `{scope}`" if scope else "Scope: all phases",
        "",
        f"Total step folders scanned: {len(step_dirs)}",
        f"Total anomalies: {anomaly_count}",
        "",
        "## Review Round Counts",
        "",
    ]

    if review_rounds:
        lines.extend(f"- {item}" for item in review_rounds)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Missing Workflow Artifacts",
            "",
        ]
    )
    if missing_artifacts:
        lines.extend(f"- {item}" for item in missing_artifacts)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Deferred Items Without Owning Steps",
            "",
        ]
    )
    if deferred_items:
        lines.extend(f"- {item}" for item in deferred_items)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Unresolved Decisions",
            "",
        ]
    )
    if unresolved:
        lines.extend(f"- {item}" for item in unresolved)
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "Use `docs/build/workflow-reviews/acknowledged.md` to suppress known or historical anomalies by substring pattern.",
        ]
    )

    return "\n".join(lines) + "\n", anomaly_count


def main() -> int:
    args = parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_text, anomaly_count = build_report(args.scope)

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = PROJECT_ROOT / output_path
    else:
        output_path = REPORT_DIR / f"metrics-{datetime.now().strftime('%Y-%m-%d')}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding="utf-8")
    print(f"Wrote report: {output_path.relative_to(PROJECT_ROOT)}")
    print(f"Anomalies: {anomaly_count}")

    return 1 if args.check and anomaly_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
