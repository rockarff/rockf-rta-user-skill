#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

USER_TYPE_LABELS = {
    "potential_users": "潜在用户",
    "core_users": "核心用户",
    "high_value_users": "高价值用户",
    "unfit_users": "不合适用户",
}


def load_json(path: Path | None) -> dict:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


def stage_gate_bool(data: dict, key: str, default: bool = False) -> bool:
    return bool(data.get("handoff", {}).get("gate_status", {}).get(key, default))


def infer_current_stage(discovery: dict, user: dict, persona: dict, content: dict) -> str:
    if not discovery:
        return "discovery_missing"
    if discovery and not user:
        return "discovery_ready_for_user"
    if user and not persona:
        return "user_ready_for_persona"
    if persona and not content:
        return "persona_ready_for_content"
    if content:
        confirmed = content.get("selection_gate", {}).get("topic_confirmed", False)
        return "content_ready_for_production" if confirmed else "content_ready_for_topic_confirmation"
    return "unknown"


def build_completed(discovery: dict, user: dict, persona: dict, content: dict) -> list[str]:
    items: list[str] = []
    if discovery:
        items.append("discovery")
    if user:
        items.extend(["user_profiles", "user_lifecycle"])
    if persona:
        items.append("persona")
    if content:
        items.extend(["content_judgment", "content_map", "topic_pool"])
    return items


def build_missing(discovery: dict, user: dict, persona: dict, content: dict) -> list[str]:
    missing: list[str] = []
    if not discovery:
        return ["discovery output"]
    if not user:
        missing.append("user output")
    if user and not persona:
        missing.append("persona output")
    if persona and not content:
        missing.append("content output")
    if content:
        gate = content.get("selection_gate", {})
        if not gate.get("topic_confirmed", False):
            missing.append("人工确认本轮选题")
        if gate.get("topic_confirmed", False) and not gate.get("auxiliary_framework_requested", False):
            missing.append("确认是否继续出辅助框架")
    return dedupe(missing)


def infer_next_skill(discovery: dict, user: dict, persona: dict, content: dict) -> str:
    if not discovery:
        return "rta-discovery-skill"
    if not user:
        return "rta-user-skill"
    if not persona:
        return "rta-persona-skill"
    if not content:
        return "rta-content-skill"
    return "rta-content-skill"


def infer_confirmation_gate(discovery: dict, user: dict, persona: dict, content: dict) -> str:
    if not discovery:
        return "Discovery -> User"
    if not user:
        return "Discovery -> User"
    if not persona:
        return "User -> Persona"
    if not content:
        return "Persona -> Content"
    if not content.get("selection_gate", {}).get("topic_confirmed", False):
        return "Topic Pool -> Production Draft"
    return "Production Draft Ready"


def build_stage_gates(discovery: dict, user: dict, persona: dict, content: dict) -> dict:
    discovery_passed = stage_gate_bool(discovery, "discovery_gate_passed", bool(discovery))
    user_passed = bool(user)
    persona_passed = bool(persona)
    content_passed = bool(content and content.get("selection_gate", {}).get("topic_confirmed", False))

    blocked_by: list[str] = []
    if not discovery_passed:
        blocked_by.append("Discovery 闸门未通过")
    if discovery and not user:
        blocked_by.append("缺少 USER 输出")
    if user and not persona:
        blocked_by.append("缺少 PERSONA 输出")
    if persona and not content:
        blocked_by.append("缺少 CONTENT 输出")
    if content and not content.get("selection_gate", {}).get("topic_confirmed", False):
        blocked_by.append("选题尚未人工确认")

    return {
        "discovery_gate_passed": discovery_passed,
        "user_gate_passed": user_passed,
        "persona_gate_passed": persona_passed,
        "content_gate_passed": content_passed,
        "blocked_by": dedupe(blocked_by),
    }


def short_list(items: list[str], limit: int = 3) -> list[str]:
    return [x for x in items if x][:limit]


def flatten_profile(profile: dict, label: str) -> dict:
    return {
        "name": label,
        "tag": profile.get("name", ""),
        "one_line": profile.get("description", ""),
        "identity": short_list([profile.get("identity", "")] + profile.get("identification_signals", []), 4),
        "scenes": short_list(profile.get("trigger_scenarios", []), 4),
        "surface": short_list(profile.get("surface_problems", []), 4),
        "deep": short_list(profile.get("deep_pains", []), 4),
        "trust": short_list(profile.get("trust_sources", []), 4),
        "signals": short_list(profile.get("identification_signals", []), 4),
        "judgment": profile.get("fit_reason", ""),
    }


def build_user_segments(user: dict) -> list[dict]:
    if not user:
        return []
    mapping = [
        ("potential_users", "潜在用户"),
        ("core_users", "核心用户"),
        ("high_value_users", "高价值用户"),
        ("unfit_users", "不合适用户"),
    ]
    profiles = user.get("user_profiles", {})
    result: list[dict] = []
    for key, label in mapping:
        group = profiles.get(key, [])
        if group:
            result.append(flatten_profile(group[0], label))
    return result


def build_lifecycle_notes(user: dict, content: dict) -> list[str]:
    notes = [
        "阶段 1-6 优先用于公域内容判断与选题。",
        "阶段 7-10 更偏咨询、服务、复购与转介绍，不作为短视频主选题区。",
    ]
    if content:
        notes.append("选题应优先绑定当前最值得打的画像与阶段，而不是只按业务知识堆内容。")
    return dedupe(notes)


def build_lifecycle_focus(user: dict) -> dict:
    lifecycle = user.get("user_lifecycle", [])
    if not lifecycle:
        return {}
    rows = []
    for item in lifecycle[:6]:
        rows.append({
            "stage": item.get("stage", ""),
            "scene": " / ".join(short_list(item.get("typical_scenarios", []), 2)),
            "thought": " / ".join(short_list(item.get("user_thoughts", []), 2)),
            "pain": " / ".join(short_list(item.get("core_pains", []), 2)),
            "signal": " / ".join(short_list(item.get("signals", []), 2)),
        })
    return {"核心阶段": rows}


def build_persona_summary(persona: dict) -> dict:
    if not persona:
        return {}
    return {
        "core_sentence": persona.get("persona_core", ""),
        "trust_role": persona.get("trust_role", {}).get("primary", "") if isinstance(persona.get("trust_role"), dict) else persona.get("trust_role", ""),
        "expression_advantages": dedupe([
            persona.get("expression_style", {}).get("tone", "") if isinstance(persona.get("expression_style"), dict) else "",
            persona.get("expression_style", {}).get("sentence_pattern", "") if isinstance(persona.get("expression_style"), dict) else "",
            persona.get("expression_style", {}).get("advantage_pattern", "") if isinstance(persona.get("expression_style"), dict) else "",
        ]),
        "not_fit": dedupe(persona.get("expression_red_lines", []) + persona.get("red_lines", [])),
    }


def build_content_judgment(content: dict) -> dict:
    if not content:
        return {}
    content_map = content.get("content_map", {})
    mapped = []
    for content_type in ["broad_traffic", "semi_vertical_traffic", "trust", "conversion"]:
        for item in content_map.get(content_type, [])[:1]:
            mapped.append({
                "type": content_type,
                "users": USER_TYPE_LABELS.get(item.get("user_type", ""), item.get("user_type", "")),
                "focus": item.get("message_direction", "") or item.get("content_goal", ""),
            })
    ratio_obj = content.get("generation_record", {}).get("content_ratio", {})
    ratio = []
    for key in ["broad_traffic", "semi_vertical_traffic", "trust", "conversion"]:
        if ratio_obj.get(key):
            ratio.append(f"{key}:{ratio_obj[key]}")
    judgment = content.get("content_judgment", {})
    return {
        "public_focus": dedupe(judgment.get("public_domain_focus", [])),
        "private_domain": "当前未开启" if not judgment.get("private_domain_focus") else "已包含私域",
        "ratio": ratio,
        "style": dedupe(judgment.get("mother_topic_pool", [])),
        "avoid": [],
        "map": mapped,
    }


def build_topic_pool(content: dict) -> list[dict]:
    if not content:
        return []
    rows = []
    for item in content.get("topic_pool", []):
        rows.append({
            "topic_id": item.get("topic_id", ""),
            "topic_title": item.get("topic_title", ""),
            "user_type": item.get("user_type", ""),
            "lifecycle_stage": item.get("lifecycle_stage", ""),
            "content_type": item.get("content_type", ""),
            "interview_question": item.get("interview_question", ""),
            "open_question": item.get("hook", "") or item.get("interview_question", ""),
            "followup_question": item.get("comment_prompt", "") or item.get("interview_question", ""),
            "judgment_question": item.get("goal_action", "") or item.get("topic_direction", ""),
        })
    return rows


def infer_project_stage(completed: list[str], stage_gates: dict) -> str:
    if stage_gates.get("content_gate_passed"):
        return "已完成内容判断、题库确认，可进入脚本生产"
    if "topic_pool" in completed:
        return "已完成内容判断与题库，待人工确认选题"
    if "persona" in completed:
        return "已完成人设，可进入内容阶段"
    if "user_lifecycle" in completed:
        return "已完成用户理解，可进入人设阶段"
    if "discovery" in completed:
        return "已完成 Discovery，可进入 USER"
    return "准备开始"


def build_summary(discovery: dict, user: dict, persona: dict, content: dict) -> list[str]:
    lines: list[str] = []
    if user:
        core = user.get("user_profiles", {}).get("core_users", [])
        if core:
            lines.append(f"当前最值得优先服务的是：{core[0].get('name', '核心用户')}。")
    if user:
        lines.append("公域内容优先围绕前 6 个用户阶段展开。")
    if persona:
        lines.append(f"当前最稳的人设表达是：{persona.get('persona_core', '')}")
    if content:
        pool = content.get("content_judgment", {}).get("mother_topic_pool", [])
        if pool:
            lines.append(f"当前内容应优先围绕这些母题展开：{' / '.join(pool[:3])}。")
    if discovery:
        near_close = discovery.get("portrait_snapshot", {}).get("likely_to_close", [])
        if near_close:
            lines.append(f"准成交画像已经出现方向：{near_close[0]}。")
    return dedupe(lines)[:5]


def build_next_actions_30d(content: dict) -> list[str]:
    actions = [
        "补齐准成交画像的真实语料，尤其是最后成交触发点与常见犹豫点。",
        "围绕前 6 阶段持续输出内容，先验证广流量与半垂直切口。",
        "人工确认首轮选题后，再进入辅助框架或脚本生产。"
    ]
    if content and content.get("selection_gate", {}).get("topic_confirmed"):
        actions[2] = "已确认选题，直接进入辅助框架或脚本生产。"
    return actions


def build_next_actions_90d() -> list[str]:
    return [
        "持续迭代已成交、准成交、不适合三类画像，避免内容越做越泛。",
        "把原生母题和表达红线固定下来，减少后续脚本跑偏。",
        "逐步沉淀成阶段报告与标准交付包，方便复用到新客户。"
    ]


def build_report_input(discovery: dict, user: dict, persona: dict, content: dict, workflow_handoff: dict) -> dict:
    completed = workflow_handoff["completed"]
    stage_gates = workflow_handoff["stage_gates"]
    return {
        "report_mode": "full_report" if all([discovery, user, persona, content]) else "stage_report",
        "report_title": f"{user.get('business_context', {}).get('client_name') or discovery.get('input_snapshot', {}).get('client_name', '客户')}｜RTA阶段调研报告",
        "client_name": user.get("business_context", {}).get("client_name") or discovery.get("input_snapshot", {}).get("client_name", ""),
        "project_stage": infer_project_stage(completed, stage_gates),
        "summary": build_summary(discovery, user, persona, content),
        "user_segments": build_user_segments(user),
        "lifecycle_notes": build_lifecycle_notes(user, content),
        "lifecycle_stage_axis": [item.get("stage", "") for item in user.get("user_lifecycle", [])],
        "lifecycle_focus": build_lifecycle_focus(user),
        "content_judgment": build_content_judgment(content),
        "topic_pool": build_topic_pool(content),
        "persona_summary": build_persona_summary(persona),
        "next_actions_30d": build_next_actions_30d(content),
        "next_actions_90d": build_next_actions_90d(),
        "workflow_summary": workflow_handoff,
        "discovery_snapshot": {
            "portrait_snapshot": discovery.get("portrait_snapshot", {}),
            "mother_topic_capture": discovery.get("mother_topic_capture", {}),
        },
    }


def render_status_md(workflow_handoff: dict) -> str:
    gates = workflow_handoff["stage_gates"]
    blocked = workflow_handoff["stage_gates"].get("blocked_by", [])
    done = workflow_handoff.get("completed", [])
    missing = workflow_handoff.get("missing_inputs", [])
    lines = [
        "# RTA 当前阶段判断",
        "",
        "## 当前阶段",
        workflow_handoff.get("current_stage", ""),
        "",
        "## 已完成",
    ]
    lines.extend([f"- {item}" for item in done] or ["- 暂无"])
    lines.extend(["", "## 缺失输入"])
    lines.extend([f"- {item}" for item in missing] or ["- 暂无"])
    lines.extend(["", "## 下一步调用", workflow_handoff.get("next_skill", ""), "", "## 人工确认点", workflow_handoff.get("confirmation_gate", ""), "", "## 闸门状态"])
    lines.extend([
        f"- Discovery: {'passed' if gates.get('discovery_gate_passed') else 'blocked'}",
        f"- User: {'passed' if gates.get('user_gate_passed') else 'blocked'}",
        f"- Persona: {'passed' if gates.get('persona_gate_passed') else 'blocked'}",
        f"- Content: {'passed' if gates.get('content_gate_passed') else 'blocked'}",
        "",
        "## 阻塞项",
    ])
    lines.extend([f"- {item}" for item in blocked] or ["- 暂无"])
    return "\n".join(lines).strip() + "\n"


def build_bundle(discovery: dict, user: dict, persona: dict, content: dict) -> tuple[dict, dict]:
    workflow_handoff = {
        "current_stage": infer_current_stage(discovery, user, persona, content),
        "completed": build_completed(discovery, user, persona, content),
        "missing_inputs": build_missing(discovery, user, persona, content),
        "next_skill": infer_next_skill(discovery, user, persona, content),
        "confirmation_gate": infer_confirmation_gate(discovery, user, persona, content),
        "stage_gates": build_stage_gates(discovery, user, persona, content),
        "recommended_report_mode": "full_report" if all([discovery, user, persona, content]) else "stage_report",
        "report_ready": bool(user),
        "artifacts": {
            "has_discovery": bool(discovery),
            "has_user": bool(user),
            "has_persona": bool(persona),
            "has_content": bool(content),
        },
    }
    report_input = build_report_input(discovery, user, persona, content, workflow_handoff)
    return workflow_handoff, report_input


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build unified workflow bundle and report input from RTA upstream outputs.")
    parser.add_argument("--discovery", help="Path to discovery output JSON.")
    parser.add_argument("--user", help="Path to user output JSON.")
    parser.add_argument("--persona", help="Path to persona output JSON.")
    parser.add_argument("--content", help="Path to content output JSON.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    parser.add_argument("--prefix", default="workflow", help="Filename prefix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    discovery = load_json(Path(args.discovery) if args.discovery else None)
    user = load_json(Path(args.user) if args.user else None)
    persona = load_json(Path(args.persona) if args.persona else None)
    content = load_json(Path(args.content) if args.content else None)
    workflow_handoff, report_input = build_bundle(discovery, user, persona, content)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix

    (output_dir / f"{prefix}-workflow-status.md").write_text(render_status_md(workflow_handoff), encoding="utf-8")
    (output_dir / f"{prefix}-workflow-handoff.json").write_text(json.dumps(workflow_handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output_dir / f"{prefix}-report-input.json").write_text(json.dumps(report_input, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output_dir / f"{prefix}-workflow-status.md")
    print(output_dir / f"{prefix}-workflow-handoff.json")
    print(output_dir / f"{prefix}-report-input.json")


if __name__ == "__main__":
    main()
