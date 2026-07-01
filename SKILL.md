---
name: rta-skill
description: Use this skill when the user wants one coherent RTA workflow instead of separate skills. It covers client classification, interview design, user portraits, user lifecycle, persona, content planning, workflow gating, and client-facing report packaging. Use it when the user is starting a new client, continuing an RTA delivery, or wants a unified handoff from discovery to report.
---

# RTA Skill

This is the unified RTA skill.

Use it when the user does not want to manually switch between Discovery, User, Persona, Content, and Report as separate skills.

It covers one continuous workflow:

`Discovery -> User -> Persona -> Content -> Workflow -> Report`

Read first:

- `references/usage-guide.md`
- `references/workflow-why.md`
- `references/workflow/workflow-map.md`
- `references/workflow/stage-gates.md`

Then load only the relevant phase references:

- Discovery phase:
  - `references/discovery/client-types.md`
  - `references/discovery/interview-paths.md`
  - `references/discovery/question-design-rules.md`
  - `references/discovery/material-checklist.md`
- User phase:
  - `references/user/interview-flow.md`
  - `references/user/question-bank.md`
  - `references/user/output-schema.md`
- Persona phase:
  - `references/persona/persona-dimensions.md`
  - `references/persona/evidence-priority.md`
  - `references/persona/expression-patterns.md`
- Content phase:
  - `references/content/content-types.md`
  - `references/content/topic-rules.md`
  - `references/content/topic-quality-rules.md`
  - `references/content/output-schema.md`
- Report phase:
  - `references/report/report-modes.md`
  - `references/report/page-structure.md`
  - `references/report/output-schema.md`

## What this skill does

This skill should help the user do five things in order:

1. judge what kind of client this is
2. collect the right material, especially near-close portraits and mother-topic seeds
3. turn the material into user portraits, lifecycle, persona, and content direction
4. stop at the right human confirmation gates
5. package the result into a client-facing delivery report

## Why this skill is structured this way

The order is fixed for a reason:

1. Discovery comes first because wrong inputs make every downstream output unstable.
2. User comes before Persona because you cannot define expression without knowing who the expression is for.
3. Persona comes before Content because content without a stable speaking identity becomes generic.
4. Workflow sits above the stages because someone has to judge readiness, blockers, and next action.
5. Report comes last because delivery should render conclusions, not replace analysis.

## Mandatory workflow rules

- Always collect three portrait directions when possible:
  - already closed
  - likely to close
  - clearly unfit
- Always start mother-topic capture in Discovery.
- Always distinguish native mother topics from assisted mother topics in Persona.
- Always mark topic source and portrait basis in Content.
- Never auto-cross the required human confirmation gates.

## Human confirmation gates

Do not auto-cross these:

1. Discovery -> User
2. User -> Persona
3. Persona -> Content
4. Topic pool -> Production draft

## Scripts

Use these scripts when packaging or rendering is needed:

- `scripts/build_workflow_bundle.py`
- `scripts/build_report_package.py`
- `scripts/build_from_workflow_bundle.py`
- `scripts/render_report.py`

## Templates

Phase templates are grouped under:

- `templates/discovery/`
- `templates/user/`
- `templates/persona/`
- `templates/content/`
- `templates/workflow/`
- `templates/report/`

## Privacy rule

This publishable skill must not include:

- real client transcripts
- real client outputs
- real topic libraries
- real report files
- any customer-identifiable working files

Only rules, templates, schemas, scripts, and neutral instructions belong here.
