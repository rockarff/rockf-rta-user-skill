# Output Structure

The report package should include two layers.

## Client-facing layer

- report title
- report mode
- page structure
- key findings
- next-step actions
- research-report html
- representative topic sample

## Internal layer

- speaker notes
- evidence map
- confidence notes
- topic appendix html

Top-level JSON keys:

- `report_mode`
- `report_title`
- `client_name`
- `project_stage`
- `key_findings`
- `user_segments`
- `lifecycle_summary`
- `persona_summary`
- `content_summary`
- `not_recommended`
- `next_actions_30d`
- `next_actions_90d`
- `page_structure`
- `confidence_notes`
- `topic_pool`
- `representative_topics`

Preferred source order:

1. workflow-generated `report-input.json`
2. manually normalized report input
3. known case rebuild scripts
