#!/usr/bin/env python3
"""PreToolUse hook: blocks destructive terminal commands before execution."""
import json
import re
import sys

BLOCKED_PATTERNS = [
    r"git\s+push\s+.*--force",
    r"git\s+reset\s+--hard",
    r"rm\s+-rf",
    r"Remove-Item\s+.*-Recurse.*-Force",
    r"DROP\s+(TABLE|SCHEMA|DATABASE)",
    r"TRUNCATE\s+TABLE",
    r"git\s+clean\s+-fd",
    r"format\s+[A-Z]:",  # format drive
]


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return

    tool_name = data.get("tool_name", "")

    # Only check terminal/command execution tools
    if "terminal" not in tool_name.lower() and "execute" not in tool_name.lower():
        return

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "") or tool_input.get("input", "") or ""

    if not command:
        return

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Blocked by safety hook: matches destructive pattern '{pattern}'. Ask the user for explicit approval before running this command.",
                }
            }
            json.dump(output, sys.stdout)
            sys.exit(0)

    # No output = allow


if __name__ == "__main__":
    main()
