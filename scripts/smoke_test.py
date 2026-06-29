#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "templates/user-insights.schema.json",
    "templates/user-profiles.md",
    "templates/user-lifecycle.md",
    "templates/report.md",
    "references/output-schema.md",
    "references/chart-spec.md",
    "references/interview-flow.md",
    "references/question-bank.md",
    "examples/transcript-example.md",
    "outputs/test-generic-user-insights.json",
    "outputs/test-anonymized-report.md",
]

FIXED_STAGES = [
    "无意识",
    "有意识",
    "记住你",
    "关注你",
    "了解你",
    "接触你",
    "好朋友",
    "选择你",
    "有收获",
    "转介绍",
]


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def check_required_files():
    for rel in REQUIRED_FILES:
        assert_true((ROOT / rel).exists(), f"Missing required file: {rel}")


def check_example_json():
    path = ROOT / "outputs/test-generic-user-insights.json"
    data = json.loads(path.read_text())

    for key in ["meta", "business_context", "interview_source", "user_profiles", "user_lifecycle"]:
        assert_true(key in data, f"Missing root key: {key}")

    profiles = data["user_profiles"]
    for key in ["potential_users", "core_users", "high_value_users", "unfit_users"]:
        assert_true(key in profiles, f"Missing profile group: {key}")
        assert_true(isinstance(profiles[key], list), f"Profile group must be a list: {key}")

    lifecycle = data["user_lifecycle"]
    assert_true(len(lifecycle) == 10, f"Lifecycle must contain 10 stages, got {len(lifecycle)}")
    assert_true([item["stage"] for item in lifecycle] == FIXED_STAGES, "Lifecycle stages are not in fixed order")

    for item in lifecycle:
        assert_true(len(item.get("core_pains", [])) >= 3, f"Stage {item['stage']} must have at least 3 core pains")
        for field in ["typical_scenarios", "touchpoints", "user_thoughts", "user_behaviors", "trust_barriers", "progress_actions", "signals"]:
            assert_true(isinstance(item.get(field, []), list), f"Stage {item['stage']} field {field} must be a list")


def main():
    check_required_files()
    check_example_json()
    print("RTA-USER smoke test passed")


if __name__ == "__main__":
    main()
