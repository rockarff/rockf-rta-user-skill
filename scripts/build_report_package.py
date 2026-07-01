from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_report import (
    load_payload,
    normalize_topic,
    pick_representative_topics,
    write_package,
)


ROOT = Path(__file__).resolve().parents[1]
OUTLINE_PATH = ROOT / "templates" / "report-deck-outline.json"


def load_outline() -> list[dict]:
    data = json.loads(OUTLINE_PATH.read_text(encoding="utf-8"))
    return data.get("default_pages", [])


def infer_lifecycle_summary(payload: dict) -> dict:
    axis = payload.get("lifecycle_stage_axis", [])
    public_window = "前 6 阶段"
    if len(axis) >= 6:
        public_window = " / ".join(axis[:6])
    return {
        "focus_stages": axis[:6],
        "public_content_window": public_window,
        "transition_risk": "7-10 阶段更偏咨询、服务与转介绍，不作为短视频主选题区。",
    }


def infer_content_summary(payload: dict) -> dict:
    content = payload.get("content_judgment", {})
    return {
        "priority_users": content.get("public_focus", []),
        "content_mix": content.get("ratio", []),
        "avoid_now": content.get("avoid", []),
    }


def infer_not_recommended(payload: dict) -> list[str]:
    values: list[str] = []
    content = payload.get("content_judgment", {})
    persona = payload.get("persona_summary", {})
    values.extend(content.get("avoid", []))
    values.extend(persona.get("not_fit", []))
    deduped: list[str] = []
    seen: set[str] = set()
    for item in values:
        if item and item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def render_summary_md(output_payload: dict) -> str:
    lines = [f"# {output_payload['report_title']}", "", "## 核心结论"]
    for i, item in enumerate(output_payload.get("key_findings", []), start=1):
        lines.append(f"{i}. {item}")
    lines.extend(["", "## 当前阶段", output_payload.get("project_stage", "")])
    lines.extend(["", "## 下一步动作（30 天）"])
    for item in output_payload.get("next_actions_30d", []):
        lines.append(f"- {item}")
    lines.extend(["", "## 下一步动作（90 天）"])
    for item in output_payload.get("next_actions_90d", []):
        lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def render_speaker_notes_md(output_payload: dict) -> str:
    lines = ["# 报告讲解备注", "", "## 建议讲解顺序"]
    lines.extend([
        "- 先讲当前最值得抓的用户是谁。",
        "- 再讲哪些生命周期阶段适合公域内容。",
        "- 再讲此人的表达与人设应该怎么立。",
        "- 最后讲内容结构和下一步动作。",
        "",
        "## 讲解重点",
    ])
    for item in output_payload.get("key_findings", []):
        lines.append(f"- {item}")
    if output_payload.get("not_recommended"):
        lines.extend(["", "## 当前不建议", *[f"- {item}" for item in output_payload["not_recommended"]]])
    return "\n".join(lines).strip() + "\n"


def render_evidence_map_md(output_payload: dict) -> str:
    lines = ["# 结论依据映射", "", "## 本次报告依据", ""]
    lines.append("- 用户画像")
    lines.append("- 用户生命旅程")
    lines.append("- 表达与人设判断")
    lines.append("- 内容判断与题库")
    if output_payload.get("confidence_notes"):
        lines.extend(["", "## 置信度说明"])
        for item in output_payload["confidence_notes"]:
            lines.append(f"- {item}")
    return "\n".join(lines).strip() + "\n"


def build_output_payload(input_payload: dict) -> dict:
    topic_pool = input_payload.get("topic_pool", [])
    representative_topics = input_payload.get("representative_topics")
    if not representative_topics:
        representative_topics = [
            normalize_topic(item)
            for item in pick_representative_topics(topic_pool, None)
        ]

    output_payload = {
        "report_mode": input_payload.get("report_mode", "stage_report"),
        "report_title": input_payload.get("report_title", "RTA 调研报告"),
        "client_name": input_payload.get("client_name", ""),
        "project_stage": input_payload.get("project_stage", ""),
        "key_findings": input_payload.get("summary", []),
        "page_structure": load_outline(),
        "user_segments": input_payload.get("user_segments", []),
        "lifecycle_summary": infer_lifecycle_summary(input_payload),
        "persona_summary": {
            "persona_core": input_payload.get("persona_summary", {}).get("core_sentence", ""),
            "trust_role": input_payload.get("persona_summary", {}).get("trust_role", ""),
            "expression_style": " / ".join(input_payload.get("persona_summary", {}).get("expression_advantages", [])),
            "red_lines": input_payload.get("persona_summary", {}).get("not_fit", []),
        },
        "content_summary": infer_content_summary(input_payload),
        "not_recommended": infer_not_recommended(input_payload),
        "next_actions_30d": input_payload.get("next_actions_30d", []),
        "next_actions_90d": input_payload.get("next_actions_90d", []),
        "confidence_notes": input_payload.get("confidence_notes", []),
        "topic_pool": topic_pool,
        "representative_topics": representative_topics,
        "source_payload": input_payload,
    }
    return output_payload


def write_markdown_and_json(output_payload: dict, output_dir: Path, prefix: str) -> dict[str, Path]:
    files = {
        "summary_md": output_dir / f"{prefix}-report-summary.md",
        "speaker_notes_md": output_dir / f"{prefix}-report-speaker-notes.md",
        "evidence_map_md": output_dir / f"{prefix}-report-evidence-map.md",
        "structure_json": output_dir / f"{prefix}-report-structure.json",
        "output_json": output_dir / f"{prefix}-report-output.json",
    }
    files["summary_md"].write_text(render_summary_md(output_payload), encoding="utf-8")
    files["speaker_notes_md"].write_text(render_speaker_notes_md(output_payload), encoding="utf-8")
    files["evidence_map_md"].write_text(render_evidence_map_md(output_payload), encoding="utf-8")
    files["structure_json"].write_text(json.dumps(output_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    files["output_json"].write_text(json.dumps(output_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return files


def build_package_from_payload(input_payload: dict, output_dir: Path, prefix: str) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_payload = build_output_payload(input_payload)
    files = write_markdown_and_json(output_payload, output_dir, prefix)
    html_files = write_package(input_payload, output_dir, prefix)
    html_files.pop("json", None)
    return {**files, **html_files}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a fixed-structure RTA report package from normalized report input JSON.")
    parser.add_argument("--input", required=True, help="Path to report-input JSON.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    parser.add_argument("--prefix", default="report", help="Filename prefix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    payload = load_payload(input_path)
    files = build_package_from_payload(payload, Path(args.output_dir), args.prefix)
    print("generated:")
    for path in files.values():
        print(path)


if __name__ == "__main__":
    main()
