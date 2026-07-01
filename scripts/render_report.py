from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_SCHEMA_PATH = ROOT / "templates" / "report-input.schema.json"

CONTENT_TYPE_LABELS = {
    "traffic": "流量",
    "broad_traffic": "广流量",
    "semi_vertical_traffic": "半垂直流量",
    "trust": "信任",
    "conversion": "转化",
    "private_domain": "私域",
}

USER_TYPE_LABELS = {
    "potential_users": "潜在用户",
    "core_users": "核心用户",
    "high_value_users": "高价值用户",
    "unfit_users": "不合适用户",
}


def load_payload(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_payload(payload)
    return payload


def load_input_schema() -> dict:
    if INPUT_SCHEMA_PATH.exists():
        return json.loads(INPUT_SCHEMA_PATH.read_text(encoding="utf-8"))
    return {}


def require_keys(obj: dict, keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise ValueError(f"{label} 缺少字段: {', '.join(missing)}")


def validate_payload(payload: dict) -> None:
    if not isinstance(payload, dict):
        raise ValueError("report input 必须是 JSON object")
    schema = load_input_schema()
    required = schema.get("required", [])
    require_keys(payload, required, "report input")
    list_fields = [
        "summary",
        "user_segments",
        "lifecycle_notes",
        "lifecycle_stage_axis",
        "topic_pool",
    ]
    for field in list_fields:
        if field in payload and not isinstance(payload[field], list):
            raise ValueError(f"{field} 必须是 array")
    if "lifecycle_focus" in payload and not isinstance(payload["lifecycle_focus"], dict):
        raise ValueError("lifecycle_focus 必须是 object")
    if "content_judgment" in payload and not isinstance(payload["content_judgment"], dict):
        raise ValueError("content_judgment 必须是 object")
    for i, segment in enumerate(payload.get("user_segments", []), start=1):
        if not isinstance(segment, dict):
            raise ValueError(f"user_segments[{i}] 必须是 object")
        require_keys(segment, ["name", "tag", "one_line", "identity", "scenes", "surface", "deep", "trust", "signals", "judgment"], f"user_segments[{i}]")
    for key, rows in payload.get("lifecycle_focus", {}).items():
        if not isinstance(rows, list):
            raise ValueError(f"lifecycle_focus.{key} 必须是 array")
        for j, row in enumerate(rows, start=1):
            require_keys(row, ["stage", "scene", "thought", "pain", "signal"], f"lifecycle_focus.{key}[{j}]")
    for i, topic in enumerate(payload.get("topic_pool", []), start=1):
        require_keys(
            topic,
            ["topic_id", "topic_title", "user_type", "lifecycle_stage", "content_type", "interview_question", "open_question", "followup_question", "judgment_question"],
            f"topic_pool[{i}]",
        )


def list_block(items: list[str]) -> str:
    return "".join(f"<li>{item}</li>" for item in items)


def chips(items: list[str], cls: str = "") -> str:
    return "".join(f'<span class="chip {cls}">{item}</span>' for item in items)


def lifecycle_rows(items: list[dict[str, str]]) -> str:
    rows = []
    for item in items:
        rows.append(
            f"""
            <tr>
              <td>{item.get('stage', '')}</td>
              <td>{item.get('scene', '')}</td>
              <td>{item.get('thought', '')}</td>
              <td>{item.get('pain', '')}</td>
              <td>{item.get('signal', '')}</td>
            </tr>
            """
        )
    return "".join(rows)


def pick_representative_topics(topic_pool: list[dict], custom: list[dict] | None) -> list[dict]:
    if custom:
        return custom
    plan = [
        ("broad_traffic", 8),
        ("semi_vertical_traffic", 4),
        ("trust", 2),
        ("conversion", 1),
    ]
    picked: list[dict] = []
    for content_type, limit in plan:
        group = [item for item in topic_pool if item.get("content_type") == content_type]
        picked.extend(group[:limit])
    return picked


def normalize_topic(topic: dict) -> dict:
    topic = dict(topic)
    topic["content_type_label"] = CONTENT_TYPE_LABELS.get(topic.get("content_type"), topic.get("content_type", ""))
    topic["user_type_label"] = USER_TYPE_LABELS.get(topic.get("user_type"), topic.get("user_type", ""))
    return topic


def render_main_report(payload: dict) -> str:
    report = {
        "report_title": payload.get("report_title", "RTA 调研报告"),
        "summary": payload.get("summary", []),
        "client_name": payload.get("client_name", ""),
    }
    user_segments = payload.get("user_segments", [])
    lifecycle_notes = payload.get("lifecycle_notes", [])
    lifecycle_stage_axis = payload.get("lifecycle_stage_axis", [])
    lifecycle_focus = payload.get("lifecycle_focus", {})
    content_judgment = payload.get("content_judgment", {})
    topic_pool = [normalize_topic(item) for item in payload.get("topic_pool", [])]
    representative_topics = [normalize_topic(item) for item in pick_representative_topics(topic_pool, payload.get("representative_topics"))]

    overview_meta = {
        "潜在用户": ("前置教育", "公域流量 / 公域信任", "中"),
        "核心用户": ("当前主转化", "公域信任 / 公域转化", "高"),
        "高价值用户": ("长期价值", "线下关系 / 转介绍 / 私域信任", "中"),
        "不合适用户": ("低优先级", "不作为当前内容主目标", "低"),
    }

    segment_overview_rows = "".join(
        f"""
        <tr>
          <td>{segment.get('name', '')}</td>
          <td>{overview_meta.get(segment.get('name', ''), ('', '', ''))[0]}</td>
          <td>{segment.get('one_line', '')}</td>
          <td>{overview_meta.get(segment.get('name', ''), ('', '', ''))[1]}</td>
          <td>{overview_meta.get(segment.get('name', ''), ('', '', ''))[2]}</td>
        </tr>
        """
        for segment in user_segments
    )

    segment_cards = "".join(
        f"""
        <section class="segment-card">
          <div class="segment-head">
            <div class="segment-name">{segment.get('name', '')}</div>
            <div class="segment-tag">{segment.get('tag', '')}</div>
          </div>
          <div class="segment-line">{segment.get('one_line', '')}</div>
          <div class="segment-grid">
            <div><div class="label">身份</div><ul>{list_block(segment.get('identity', []))}</ul></div>
            <div><div class="label">触发场景</div><ul>{list_block(segment.get('scenes', []))}</ul></div>
            <div><div class="label">表层问题</div><ul>{list_block(segment.get('surface', []))}</ul></div>
            <div><div class="label">深层痛点</div><ul>{list_block(segment.get('deep', []))}</ul></div>
            <div><div class="label">信任来源</div><ul>{list_block(segment.get('trust', []))}</ul></div>
            <div><div class="label">识别信号</div><ul>{list_block(segment.get('signals', []))}</ul></div>
          </div>
          <div class="segment-judgment">{segment.get('judgment', '')}</div>
        </section>
        """
        for segment in user_segments
    )

    lifecycle_sections = "".join(
        f"""
        <section class="panel lifecycle-panel">
          <div class="section-kicker">{name}</div>
          <table class="data-table">
            <thead>
              <tr>
                <th>阶段</th>
                <th>典型场景</th>
                <th>用户想法</th>
                <th>核心痛点</th>
                <th>判断信号</th>
              </tr>
            </thead>
            <tbody>{lifecycle_rows(rows)}</tbody>
          </table>
        </section>
        """
        for name, rows in lifecycle_focus.items()
    )

    content_rows = "".join(
        f"""
        <tr>
          <td>{item.get('type', '')}</td>
          <td>{item.get('users', '')}</td>
          <td>{item.get('focus', '')}</td>
        </tr>
        """
        for item in content_judgment.get("map", [])
    )

    topic_cards = "".join(
        f"""
        <article class="topic-card">
          <div class="topic-card-head">
            <div class="topic-id">{item.get('topic_id', '')}</div>
            <div class="topic-meta">
              <span>{item.get('content_type_label', '')}</span>
              <span>{item.get('user_type_label', '')}</span>
              <span>{item.get('lifecycle_stage', '')}</span>
            </div>
          </div>
          <div class="topic-title">{item.get('topic_title', '')}</div>
          <div class="topic-grid">
            <div class="topic-q"><div class="topic-label">主问题</div><div class="topic-text">{item.get('interview_question', '')}</div></div>
            <div class="topic-q"><div class="topic-label">开放追问</div><div class="topic-text">{item.get('open_question', '')}</div></div>
            <div class="topic-q"><div class="topic-label">深入追问</div><div class="topic-text">{item.get('followup_question', '')}</div></div>
            <div class="topic-q"><div class="topic-label">判断追问</div><div class="topic-text">{item.get('judgment_question', '')}</div></div>
          </div>
        </article>
        """
        for item in representative_topics
    )

    persona_summary = payload.get("persona_summary", {})
    persona_line = persona_summary.get("core_sentence", "一个不先空谈输赢、而是先把局面讲清楚、把错误动作拦住的判断型从业者。")
    trust_role = persona_summary.get("trust_role", "高压场景里的判断者与顺序给定者。")
    expression_advantages = persona_summary.get("expression_advantages", content_judgment.get("style", []))
    not_fit = persona_summary.get("not_fit", content_judgment.get("avoid", []))
    next_30 = payload.get("next_actions_30d", [
        "确定主表达：判断型、顺序型、高压场景型。",
        "围绕潜在用户与核心用户前 6 阶段连续生产内容。",
    ])
    next_90 = payload.get("next_actions_90d", [
        "持续验证流量 / 信任 / 转化三类内容的真实咨询转化效果。",
        "核心用户线跑顺后，再设计高价值节点动作。",
    ])

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{report['report_title']}</title>
<style>
:root{{--paper:#fff;--ink:#171717;--muted:#585858;--line:#dfe2e8;--blue:#1a38d8;--blackbar:#151515;--highlight:#d7f03d;}}
*{{box-sizing:border-box}} body{{margin:0;background:linear-gradient(rgba(26,56,216,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(26,56,216,.05) 1px,transparent 1px),linear-gradient(180deg,#f7f6f1,#efeee8);background-size:72px 72px,72px 72px,100% 100%;font-family:Helvetica,Arial,"PingFang SC","Noto Sans SC",sans-serif;color:var(--ink);line-height:1.55}}
.report{{width:1380px;margin:0 auto;padding:36px 34px 60px}} .hero,.panel{{background:var(--paper);border:1px solid var(--line);padding:34px 34px 38px;margin-bottom:18px}} .hero{{padding:56px 58px 48px}}
.eyebrow,.section-kicker,.label,.topic-label{{font-size:13px;font-weight:700;letter-spacing:.08em;color:var(--blue);text-transform:uppercase}}
h1{{font-size:84px;line-height:.95;letter-spacing:-.07em;font-weight:300;margin:18px 0 22px;max-width:920px}} h2{{font-size:56px;line-height:.98;letter-spacing:-.06em;font-weight:300;margin:0 0 14px;max-width:1000px}}
.hero-sub,.lede{{font-size:22px;color:var(--muted);max-width:1020px}} .meta-tag{{display:inline-block;margin-top:28px;padding:12px 16px;background:var(--highlight);font-size:14px;font-weight:700}}
.summary-band{{margin-top:54px;display:grid;grid-template-columns:1.1fr .9fr;gap:24px}} .statement{{border-top:2px solid var(--blackbar);padding-top:18px;font-size:56px;line-height:1.04;letter-spacing:-.05em;font-weight:300}}
.summary-list{{border-top:2px solid var(--blackbar)}} .summary-item{{display:grid;grid-template-columns:54px 1fr;gap:16px;padding:20px 0;border-bottom:1px solid var(--line)}} .summary-no{{color:var(--blue);font-size:13px;font-weight:700;letter-spacing:.06em;padding-top:4px}} .summary-text{{font-size:21px;line-height:1.55}}
.chip-row,.topic-meta{{display:flex;flex-wrap:wrap;gap:10px}} .chip,.topic-meta span{{display:inline-block;padding:10px 14px;border:1px solid var(--line);font-size:14px;font-weight:700;background:#fbfbfb}} .chip.green{{border-color:#cfdbab;background:#f3f8e5;color:#58720b}} .chip.dark{{background:#151515;border-color:#151515;color:#fff}}
.segment-card,.block,.topic-card{{border-top:2px solid var(--blackbar);padding-top:14px}} .segment-head,.topic-card-head{{display:flex;align-items:center;gap:18px;justify-content:space-between;margin-bottom:12px}} .segment-name{{font-size:34px;font-weight:300;letter-spacing:-.04em}} .segment-tag{{font-size:13px;font-weight:700;color:var(--blue);letter-spacing:.08em;text-transform:uppercase}} .segment-line{{font-size:23px;margin-bottom:18px}}
.segment-grid,.topic-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 18px}} .segment-grid{{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px 24px}} ul{{margin:0;padding-left:20px;font-size:17px;line-height:1.6}} li{{margin-bottom:8px}} .segment-judgment{{margin-top:20px;padding-top:16px;border-top:1px solid var(--line);font-size:18px;font-weight:700}}
.overview-table,.matrix-table,.data-table,.topic-table{{width:100%;border-collapse:collapse;table-layout:fixed}} .overview-table th,.overview-table td,.matrix-table th,.matrix-table td,.data-table th,.data-table td,.topic-table th,.topic-table td{{border-top:1px solid var(--line);padding:12px 10px;vertical-align:top;text-align:left;word-break:break-word}} .overview-table th,.matrix-table th,.data-table th,.topic-table th{{color:var(--blue);font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}
.axis{{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:10px;margin-top:24px}} .axis-step{{min-height:90px;border:1px solid var(--line);padding:12px 10px;display:flex;flex-direction:column;justify-content:space-between;background:#fafafa}} .axis-step.active{{background:#f2f5ff;border-color:#cbd5ff}} .axis-step .num{{font-size:12px;font-weight:700;color:var(--blue)}} .axis-step .txt{{font-size:18px;line-height:1.2;font-weight:500}}
.two-col,.roadmap{{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:22px}} .big-stat-row{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:22px}} .big-stat{{border-top:4px solid var(--blue);padding-top:14px}} .big-stat .n{{font-size:64px;line-height:.95;font-weight:200;margin-bottom:8px}} .big-stat .t{{font-size:18px;line-height:1.45}}
.topic-id{{font-size:22px;font-weight:300;color:var(--blue);min-width:52px}} .topic-title{{font-size:26px;line-height:1.25;font-weight:500;margin-bottom:14px;max-width:980px}} .topic-q{{border-top:1px solid var(--line);padding-top:10px}} .topic-label{{font-size:11px;margin-bottom:6px}} .topic-text{{font-size:16px;line-height:1.55}} .small-note{{margin-top:14px;font-size:14px;color:var(--muted)}}
</style></head><body><main class="report">
<section class="hero"><div class="eyebrow">RTA 调研报告</div><h1>{report['report_title']}</h1><div class="hero-sub">基于访谈语料、用户画像、用户生命旅程与内容判断结果，整理本阶段最值得执行的用户与内容方向。</div><div class="meta-tag">阶段性调研报告</div><div class="summary-band"><div class="statement">本次交付聚焦三件事：先抓谁、怎么说、先做什么内容。</div><div class="summary-list">{"".join(f'<div class="summary-item"><div class="summary-no">{i:02d}</div><div class="summary-text">{text}</div></div>' for i, text in enumerate(report['summary'], start=1))}</div></div></section>
<section class="panel"><div class="section-kicker">用户画像</div><h2>用户画像总表</h2><div class="lede">按照当前业务实际，将用户拆为潜在用户、核心用户、高价值用户与不合适用户四类，并完整呈现每类用户的触发场景、问题与识别信号。</div><table class="overview-table"><thead><tr><th>用户类型</th><th>当前角色</th><th>一句话定义</th><th>主要用途</th><th>优先级</th></tr></thead><tbody>{segment_overview_rows}</tbody></table>{segment_cards}</section>
<section class="panel"><div class="section-kicker">用户生命旅程</div><h2>用户生命旅程使用规则</h2><div class="chip-row">{chips(lifecycle_notes, "green")}</div><div class="axis">{"".join(f'<div class="axis-step {"active" if i < 6 else ""}"><div class="num">{i+1:02d}</div><div class="txt">{name}</div></div>' for i, name in enumerate(lifecycle_stage_axis))}</div><div class="small-note">前 6 个阶段用于公域内容判断与选题；7-10 更偏咨询、委托、服务与转介绍判断。</div></section>
{lifecycle_sections}
<section class="panel"><div class="section-kicker">表达判断</div><h2>表达与人设判断</h2><div class="two-col"><div class="block"><div class="label">核心人设句</div><div class="summary-text">{persona_line}</div></div><div class="block"><div class="label">信任角色</div><div class="summary-text">{trust_role}</div></div></div><div class="big-stat-row">{"".join(f'<div class="big-stat"><div class="n">{i+1:02d}</div><div class="t">表达优势：{text}</div></div>' for i, text in enumerate(expression_advantages[:3]))}<div class="big-stat"><div class="n">04</div><div class="t">不适合：{not_fit[0] if not_fit else ""}</div></div></div><div class="chip-row">{chips(not_fit, "dark")}</div></section>
<section class="panel"><div class="section-kicker">内容判断</div><h2>内容判断总表</h2><div class="chip-row">{chips(content_judgment.get("public_focus", []), "green")}{chips(content_judgment.get("ratio", []))}<span class="chip dark">{content_judgment.get("private_domain", "")}</span></div><table class="matrix-table"><thead><tr><th>内容类型</th><th>对应用户</th><th>当前重点</th></tr></thead><tbody>{content_rows}</tbody></table></section>
<section class="panel"><div class="section-kicker">代表选题</div><h2>首轮题库代表样本</h2><div class="lede">正文保留代表样本，按“短视频选题 + 主问题 + 追问”方式展示，方便直接进入访谈或脚本设计。完整题库已单独整理为附录版本。</div><div class="topic-showcase">{topic_cards}</div><div class="small-note">完整题库版本见独立附录文件。</div></section>
<section class="panel"><div class="section-kicker">后续动作</div><h2>下一步动作</h2><div class="roadmap"><div class="block"><div class="label">未来 30 天</div><ul>{list_block(next_30)}</ul></div><div class="block"><div class="label">未来 90 天</div><ul>{list_block(next_90)}</ul></div></div></section>
</main></body></html>"""


def render_topic_appendix(payload: dict) -> str:
    topic_pool = [normalize_topic(item) for item in payload.get("topic_pool", [])]
    appendix_rows = "".join(
        f"""
        <tr>
          <td>{item.get('topic_id', '')}</td>
          <td>{item.get('content_type_label', '')}</td>
          <td>{item.get('user_type_label', '')}</td>
          <td>{item.get('lifecycle_stage', '')}</td>
          <td>{item.get('topic_title', '')}</td>
          <td>{item.get('interview_question', '')}</td>
        </tr>
        """
        for item in topic_pool
    )
    client_name = payload.get("client_name", "客户")
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{client_name}｜选题附录</title><style>:root{{--paper:#fff;--ink:#171717;--muted:#585858;--line:#dfe2e8;--blue:#1a38d8;--highlight:#d7f03d;}}*{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(180deg,#f7f6f1,#efeee8);font-family:Helvetica,Arial,"PingFang SC","Noto Sans SC",sans-serif;color:var(--ink)}}.wrap{{width:1380px;margin:0 auto;padding:36px 34px 60px}}.panel{{background:var(--paper);border:1px solid var(--line);padding:34px}}.eyebrow{{font-size:13px;font-weight:700;letter-spacing:.08em;color:var(--blue);text-transform:uppercase;margin-bottom:12px}}h1{{font-size:56px;line-height:1;letter-spacing:-.05em;font-weight:300;margin:0 0 12px}}.lede{{font-size:20px;line-height:1.5;color:var(--muted);margin-bottom:20px}}.meta{{display:inline-block;padding:10px 14px;background:var(--highlight);font-size:13px;font-weight:700;margin-bottom:18px}}table{{width:100%;border-collapse:collapse;table-layout:fixed;font-size:14px}}th,td{{border-top:1px solid var(--line);padding:12px 10px;vertical-align:top;text-align:left;word-break:break-word}}th{{color:var(--blue);font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}td:nth-child(1),th:nth-child(1){{width:60px}}td:nth-child(2),th:nth-child(2){{width:90px}}td:nth-child(3),th:nth-child(3){{width:110px}}td:nth-child(4),th:nth-child(4){{width:90px}}td:nth-child(5),th:nth-child(5){{width:300px}}</style></head><body><main class="wrap"><section class="panel"><div class="eyebrow">选题附录</div><h1>{client_name}｜全量公域选题附录</h1><div class="lede">本附录保留完整题库，用于内部筛选、迭代、复盘和脚本生产。主报告仅展示代表样本。</div><div class="meta">全量题库 / {len(topic_pool)} 条</div><table><thead><tr><th>ID</th><th>内容类型</th><th>对应用户</th><th>阶段</th><th>短视频选题</th><th>访谈提问</th></tr></thead><tbody>{appendix_rows}</tbody></table></section></main></body></html>"""


def write_package(payload: dict, output_dir: Path, prefix: str) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "json": output_dir / f"{prefix}-report-output.json",
        "main_html": output_dir / f"{prefix}-research-report.html",
        "appendix_html": output_dir / f"{prefix}-topic-appendix.html",
    }
    files["json"].write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    files["main_html"].write_text(render_main_report(payload), encoding="utf-8")
    files["appendix_html"].write_text(render_topic_appendix(payload), encoding="utf-8")
    return files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render fixed RTA report template from a normalized JSON payload.")
    parser.add_argument("--input", required=True, help="Path to normalized report input JSON.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated files.")
    parser.add_argument("--prefix", default="report", help="Output filename prefix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = load_payload(Path(args.input))
    files = write_package(payload, Path(args.output_dir), args.prefix)
    print("generated:")
    for path in files.values():
        print(path)


if __name__ == "__main__":
    main()
