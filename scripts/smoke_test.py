#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/usage-guide.md",
    "references/workflow-why.md",
    "references/discovery/client-types.md",
    "references/user/output-schema.md",
    "references/persona/persona-dimensions.md",
    "references/content/topic-rules.md",
    "references/workflow/stage-gates.md",
    "references/report/report-template.md",
    "templates/discovery/discovery-output.schema.json",
    "templates/user/user-insights.schema.json",
    "templates/persona/persona-output.schema.json",
    "templates/content/content-output.schema.json",
    "templates/workflow/workflow-handoff.schema.json",
    "templates/report/report-input.schema.json",
    "templates/report/report-output.schema.json",
    "scripts/build_workflow_bundle.py",
    "scripts/build_report_package.py",
    "scripts/build_from_workflow_bundle.py",
    "scripts/render_report.py",
]

FORBIDDEN_PATTERNS = [
    "欧世杰",
    "张瑜",
    "林岚",
    "oushijie",
    "linlan",
]


def main() -> None:
    missing = [item for item in REQUIRED if not (ROOT / item).exists()]
    if missing:
        raise SystemExit(f"missing required files: {missing}")

    forbidden_hits = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts:
            continue
        if path.name == "smoke_test.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                forbidden_hits.append(f"{path}: {pattern}")

    if forbidden_hits:
        raise SystemExit("forbidden client-like data found:\n" + "\n".join(forbidden_hits))

    print("rockf-rta-skill smoke test passed")
