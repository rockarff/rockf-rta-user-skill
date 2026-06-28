# Output Schema

Always generate human-readable Markdown and machine-readable JSON.

## JSON Root

```json
{
  "meta": {},
  "business_context": {},
  "interview_source": {},
  "user_profiles": {},
  "user_lifecycle": [],
  "follow_up_questions": [],
  "source_evidence": [],
  "confidence_notes": []
}
```

## Meta

```json
{
  "skill_name": "rta-user-skill",
  "version": "0.1.0",
  "mode": "live_interview_or_transcript_analysis",
  "created_at": "",
  "language": "zh-CN"
}
```

## Business Context

```json
{
  "client_name": "",
  "industry": "",
  "business_type": "",
  "main_offer": "",
  "target_service": "",
  "current_customer_source": "",
  "analysis_scope": ""
}
```

## Interview Source

```json
{
  "source_type": "live_interview_or_transcript",
  "raw_transcript_available": false,
  "summary": "",
  "information_quality": "high_medium_low",
  "missing_information": []
}
```

## User Profiles

```json
{
  "potential_users": [],
  "core_users": [],
  "high_value_users": [],
  "unfit_users": []
}
```

Each user profile object:

```json
{
  "name": "",
  "description": "",
  "identity": "",
  "current_situation": "",
  "typical_needs": [],
  "surface_problems": [],
  "deep_pains": [],
  "trigger_scenarios": [],
  "decision_barriers": [],
  "trust_sources": [],
  "payment_willingness": "",
  "fit_reason": "",
  "identification_signals": [],
  "source_evidence": []
}
```

## User Lifecycle

Use the fixed ten stages:

```text
无意识 -> 有意识 -> 记住你 -> 关注你 -> 了解你 -> 接触你 -> 好朋友 -> 选择你 -> 有收获 -> 转介绍
```

Each stage object:

```json
{
  "stage": "无意识",
  "stage_goal": "",
  "typical_scenarios": [],
  "touchpoints": [],
  "user_thoughts": [],
  "user_behaviors": [],
  "core_pains": [],
  "trust_barriers": [],
  "progress_actions": [],
  "signals": []
}
```

`core_pains` must contain at least 3 items per stage. Prefer 3-5.

